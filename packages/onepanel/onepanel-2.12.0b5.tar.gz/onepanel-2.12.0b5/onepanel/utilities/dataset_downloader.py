import os
import threading
import time

import click
from threading import Thread, Event
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from onepanel.utilities.timer import Timer
from onepanel.utilities.original_connection import Connection
from onepanel.utilities.s3_authenticator import S3Authenticator
from onepanel.utilities.aws_utility import AWSUtility
from onepanel.utilities.dataset_api import DatasetAPI


class DatasetDownloadStatus:
    """Watches a directory for files downloaded and keeps track of how many were downloaded
        and their statistics, like size.
    """
    def __init__(self, path):
        self.files = 0
        self.bytes = 0
        self.path = path

    def add_files(self, files):
        lock = threading.Lock()
        with lock:
            self.files += files

    def add_bytes(self, bytes_to_add):
        lock = threading.Lock()
        with lock:
            self.bytes += bytes_to_add

    def set_files(self, value):
        lock = threading.Lock()
        with lock:
            self.files = value

    def set_bytes(self, value):
        lock = threading.Lock()
        with lock:
            self.bytes = value

    def get_files(self):
        return self.files

    def get_bytes(self):
        return self.bytes


class DatasetMountIdentifier:
    def __init__(self, account_uid, project_uid, resource_type, resource_uid):
        self.account_uid = account_uid
        self.project_uid = project_uid
        self.resource_type = resource_type
        self.resource_uid = resource_uid
        self.dataset_uid = ''
        self.dataset_version = 0
        self.dataset_mount_uuid = ''


class DatasetMountProgressUpdater:
    def __init__(self, api, stats, account_uid, project_uid, dataset_mount_uuid):
        self.stats = stats
        self.api = api
        self.account_uid = account_uid
        self.project_uid = project_uid
        self.dataset_mount_uuid = dataset_mount_uuid

    def update(self):
        self.api.update_dataset_mount_downloader(
            account_uid=self.account_uid,
            project_uid=self.project_uid,
            dataset_mount_uuid=self.dataset_mount_uuid,
            files_downloaded=self.stats.get_files(),
            bytes_downloaded=self.stats.get_bytes())


class DatasetDownloadStatusPrinter:
    def __init__(self, stats):
        self.stats = stats

    def print_stats(self):
        stats_string = 'Files: {files} Bytes: {bytes}'.format(files=self.stats.get_files(), bytes=self.stats.get_bytes())
        print(stats_string)


class AWSDownloadFileTracker(FileSystemEventHandler):

    def __init__(self, stats):
        self.stats = stats

    def on_created(self, event):
        if event.is_directory:
            return

        # Is it a temporary file?
        # With AWS S3 CLI last dot has 8 hexadecimal characters after it.
        if event.src_path.count('.') > 1:
            last_dot_index = event.src_path.rfind('.')
            if len(event.src_path[last_dot_index + 1:]) == 8:
                return

        # Otherwise, we have a full fledged downloaded file
        self.update_statistic(event.src_path)

    def on_moved(self, event):
        """For AWS, the file is downloaded as a temporary file if it's big.
           When it finishes, it renames it.
        """
        if event.is_directory:
            return

        print('moved', event.src_path, ' to ', event.dest_path)

        self.update_statistic(event.dest_path)

    def update_statistic(self, file_path):
        print('Updating statistics with file', file_path)

        self.stats.add_files(1)

        try:
            self.stats.add_bytes(os.stat(file_path).st_size)
            print(file_path, 'is ', os.stat(file_path).st_size, 'bytes')
        except Exception:
            # Don't do anything
            pass


class DatasetDownloader(Thread):
    def __init__(self, dataset_mount, path, heartbeat=6.0, timer_delay=5.0):
        Thread.__init__(self)

        self.path = path
        self.stop_flag = Event()
        self.heartbeat = heartbeat
        self.timer_delay = timer_delay
        self.timer = None
        self.dataset_mount = dataset_mount

        # TODO - we don't need to watch the entire path, but a subpath where the dataset will go
        # Need to figure out a name for the path and update the file watcher as well as aws download util
        self.file_stats = None
        self.observer = None

        self.started = False

        self.api = None
        self.downloader_process = None

    def start(self):
        Thread.start(self)

        conn = Connection()
        conn.load_credentials()

        self.api = DatasetAPI(conn)

        if not os.path.exists(self.path):
            os.makedirs(self.path)

        self.file_stats = DatasetDownloadStatus(self.path)
        self.observer = Observer()
        self.observer.schedule(AWSDownloadFileTracker(self.file_stats), self.path, True)

        # Todo stop and return - make a cleanup function or something
        (exit_code, process) = self.start_downloading_dataset(conn, self.path, self.dataset_mount.account_uid,
                                                              self.dataset_mount.dataset_uid,
                                                              self.dataset_mount.dataset_version)
        if exit_code != 0:
            self.stop_flag.set()
            self.observer = None
            return None

        self.downloader_process = process
        self.start_monitoring_files()
        self.start_updating_api(self.dataset_mount.account_uid, self.dataset_mount.project_uid,
                                self.dataset_mount.dataset_mount_uuid)

        self.started = True

    def run(self):
        while not self.stop_flag.wait(self.heartbeat):
            if self.started:
                if self.downloader_process.poll() is not None:
                    print('subprocess is done downloading')
                    self.timer.fire()
                    self.stop()

    def join(self, timeout=None):
        if self.timer is not None:
            self.timer.join()

        if self.observer is not None:
            self.observer.join()

        if self.downloader_process is not None:
            self.downloader_process.wait()

        Thread.join(self, timeout)

    def stop(self):
        if self.timer is not None:
            self.timer.stop()

        if self.observer is not None:
            self.observer.stop()

        self.stop_flag.set()

    def start_monitoring_files(self):
        self.observer.start()

    def start_updating_api(self, account_uid, project_uid, dataset_mount_uuid):
        # stats_printer = DatasetDownloadStatusPrinter(self.file_stats)
        updater = DatasetMountProgressUpdater(self.api, self.file_stats, account_uid, project_uid, dataset_mount_uuid)
        # self.timer = Timer(self.timer_delay, stats_printer.print_stats)
        self.timer = Timer(self.timer_delay, updater.update)
        self.timer.start()

    def start_downloading_dataset(self, connection, path, account_uid, dataset_uid, dataset_version):
        # Authenticate for S3
        s3auth = S3Authenticator(connection)
        creds = s3auth.get_s3_credentials(account_uid, 'datasets', dataset_uid)
        if creds['data'] is None:
            print("Unable to get S3 credentials. Exiting.")
            return -1
        aws_access_key_id = creds['data']['AccessKeyID']
        aws_secret_access_key = creds['data']['SecretAccessKey']
        aws_session_token = creds['data']['SessionToken']
        aws_util = AWSUtility(aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key,
                              aws_session_token=aws_session_token)
        aws_util.suppress_output = True

        current_version = self.api.get_dataset_version(account_uid, dataset_uid, dataset_version)

        if current_version['data'] is None:
            if current_version['status_code'] == 404:
                click.echo('Dataset is without files.')
                return -1
            else:
                click.echo('Could not get information about dataset.')
                return -1

        if current_version['data']['provider']['uid'] != 'aws-s3':
            click.echo('Unsupported dataset provider')
            return -1

        s3_from_dir = current_version['data']['version']['path']
        aws_util.run_cmd_background = True

        return aws_util.download_all_background(path, s3_from_dir)


class DatasetDownloadListener(Thread):
    def __init__(self, connection, download_path,  account_uid, project_uid, resource_type, resource_uid):
        Thread.__init__(self)

        self.identifier = DatasetMountIdentifier(account_uid, project_uid, resource_type, resource_uid)
        self.api = DatasetAPI(connection)
        self.download_path = download_path

    def run(self):
        while True:
            print('Still downloading...')
            # TODO distinguish action between instance and job
            try:
                response = self.api.claim_instance_mount(
                    account_uid=self.identifier.account_uid,
                    project_uid=self.identifier.project_uid,
                    instance_uid=self.identifier.resource_uid,
                    downloader_id=os.getcwd(),
                    downloader_pid=os.getpid())
            except Exception:
                # On exception, try again in 10 seconds
                time.sleep(10)
                continue

            response_code = response['status_code']
            if response_code != 200:
                print('Error: {}'.format(response_code))
                # API says there is no more. Try back later.
                time.sleep(30)
                continue

            dataset_mount = response['data']

            download_identifier = DatasetMountIdentifier(dataset_mount['dataset']['account']['uid'],
                                                         self.identifier.project_uid,
                                                         self.identifier.resource_type,
                                                         self.identifier.resource_uid)

            download_identifier.dataset_mount_uuid = dataset_mount['uuid']
            download_identifier.dataset_uid = dataset_mount['dataset']['uid']
            download_identifier.dataset_version = dataset_mount['dataset_versioning']['version']

            path = os.path.join(self.download_path,
                                download_identifier.account_uid,
                                download_identifier.dataset_uid,
                                str(download_identifier.dataset_version))

            downloader = DatasetDownloader(download_identifier, path)
            downloader.start()
            downloader.join()

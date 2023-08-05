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
import logging

LOGGER = 'dataset-downloader'

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
        logging.getLogger(LOGGER).info('Sending Update to API files/bytes {}/{}'.format(self.stats.get_files(), self.stats.get_bytes()))
        response = self.api.update_dataset_mount_downloader(
            account_uid=self.account_uid,
            project_uid=self.project_uid,
            dataset_mount_uuid=self.dataset_mount_uuid,
            files_downloaded=self.stats.get_files(),
            bytes_downloaded=self.stats.get_bytes())

        if response['status_code'] != 200:
            logging.getLogger(LOGGER).warning('Unable to update API. Response code is {}'.format(response['status_code']))


class DatasetDownloadStatusPrinter:
    def __init__(self, stats):
        self.stats = stats

    def print_stats(self):
        stats_string = 'Files: {files} Bytes: {bytes}'.format(files=self.stats.get_files(), bytes=self.stats.get_bytes())
        click.echo(stats_string)


class AWSDownloadFileTracker(FileSystemEventHandler):

    def __init__(self, stats):
        self.stats = stats

    def on_created(self, event):
        if event.is_directory:
            return

        # Is it a temporary file?
        # With AWS S3 CLI last dot has 8 hexadecimal characters after it.
        if event.src_path.count('.') > 0:
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

        self.update_statistic(event.dest_path)

    def update_statistic(self, file_path):
        logging.getLogger(LOGGER).info('Updating statistics with file {}'.format(file_path))

        self.stats.add_files(1)

        try:
            self.stats.add_bytes(os.stat(file_path).st_size)
        except Exception as argument:
            logging.getLogger(LOGGER).warning('Exception trying to update statistics {}'.format(argument))
            # Don't do anything
            pass


class DatasetDownloader(Thread):
    def __init__(self, owner_uid, dataset_mount, path, heartbeat=6.0, timer_delay=5.0):
        Thread.__init__(self)

        self.owner_uid = owner_uid
        self.path = path
        self.stop_flag = Event()
        self.heartbeat = heartbeat
        self.timer_delay = timer_delay
        self.timer = None
        self.dataset_mount = dataset_mount

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
            logging.getLogger(LOGGER).warning('AWS CLI can not download. Stopping downloader.')
            self.stop_flag.set()
            self.observer = None
            return None

        self.downloader_process = process
        self.start_monitoring_files()
        self.start_updating_api(self.owner_uid, self.dataset_mount.project_uid,
                                self.dataset_mount.dataset_mount_uuid)

        self.started = True

    def run(self):
        while not self.stop_flag.wait(self.heartbeat):
            if self.started:
                if self.downloader_process.poll() is not None:
                    self.timer.fire()
                    self.stop()

    def join(self, timeout=None):
        if self.downloader_process is not None:
            self.downloader_process.wait()

        if self.timer is not None:
            self.timer.join()

        if self.observer is not None:
            self.observer.join()

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
        updater = DatasetMountProgressUpdater(self.api, self.file_stats, account_uid, project_uid, dataset_mount_uuid)
        self.timer = Timer(self.timer_delay, updater.update)
        self.timer.start()

    def start_downloading_dataset(self, connection, path, account_uid, dataset_uid, dataset_version):
        # Authenticate for S3
        s3auth = S3Authenticator(connection)
        creds = s3auth.get_s3_credentials(account_uid, 'datasets', dataset_uid)
        if creds['data'] is None:
            logging.getLogger(LOGGER).warning("Unable to get S3 credentials. Exiting.")
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
                logging.getLogger(LOGGER).info('Dataset is without files.')
                return -1
            else:
                logging.getLogger(LOGGER).warning('Could not get information about dataset.')
                return -1

        if current_version['data']['provider']['uid'] != 'aws-s3':
            logging.getLogger(LOGGER).warning('Unsupported dataset provider')
            return -1

        s3_from_dir = current_version['data']['version']['path']
        aws_util.run_cmd_background = True

        logging.getLogger(LOGGER).info('starting AWS download')

        return aws_util.download_all_background(path, s3_from_dir)


class DatasetDownloadListener(Thread):
    def __init__(self, connection, download_path, account_uid, project_uid,
                 resource_type, resource_uid, verbose=False):
        Thread.__init__(self)

        self.identifier = DatasetMountIdentifier(account_uid, project_uid, resource_type, resource_uid)
        self.api = DatasetAPI(connection)
        self.download_path = download_path

        if verbose:
            logger = logging.getLogger(LOGGER)
            logger.setLevel(logging.DEBUG)
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            ch.setFormatter(formatter)
            logger.addHandler(ch)

    def run(self):
        logger = logging.getLogger(LOGGER)

        while True:
            logger.info('Listening for Dataset Mounts')

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
                logger.warning('Got an exception trying to claim an instance mount. Trying again in 10 seconds')

                time.sleep(10)
                continue

            response_code = response['status_code']
            if response_code != 200:
                if response_code != 404:
                    logger.warning('Error from dataset mount: {}'.format(response_code))
                elif response_code == 404:
                    logger.info('No datasets to mount. Checking again in 30 seconds')
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

            if dataset_mount['alias']:
                path = os.path.join(self.download_path, dataset_mount['alias'])
            else:
                path = os.path.join(self.download_path,
                                    download_identifier.account_uid,
                                    download_identifier.dataset_uid,
                                    str(download_identifier.dataset_version))

            logger.info('Obtained dataset mount. Downloading to {}'.format(path))

            downloader = DatasetDownloader(self.identifier.account_uid, download_identifier, path)

            downloader.start()
            downloader.join()

            logger.info('Dataset {} Finished downloading'.format(path))


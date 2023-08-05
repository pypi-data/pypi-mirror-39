import sys
import os
import time
import threading
import json
import click
from threading import Thread, Event
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from onepanel.utilities.Timer import Timer
from onepanel.utilities.original_connection import Connection
from onepanel.utilities.s3_authenticator import S3Authenticator
from onepanel.utilities.aws_utility import AWSUtility


class DatasetAPI:
    def __init__(self, connection):
        self.connection = connection
        self.endpoint = connection.URL

    # Wrappers for HTTP requests
    def get(self, uid='', field_path='', params=None):
        """Get a JSON object from the endpoint"""

        r = self.connection.get(
            '{endpoint}{uid}{field_path}{params}'.format(endpoint=self.endpoint, uid=uid, field_path=field_path,
                                                          params=params or ''))

        c = r.status_code
        if c == 200:
            if r.headers['Content-Type'] == 'text/plain':
                item = r.text
            else:
                item = r.json()
        else:
            item = None

        response_data = {
                'data': item,
                'status_code': c
            }
        return response_data

    def put(self, uid='', field_path='', params=None,post_object=None):
        """Put a JSON object to the endpoint"""

        url = '{endpoint}{uid}{field_path}{params}'.format(endpoint=self.endpoint, uid=uid, field_path=field_path,
                                                           params=params or '')
        r = self.connection.put(url, data=json.dumps(post_object))

        c = r.status_code
        if c == 200:
            if r.headers['Content-Type'] == 'text/plain':
                item = r.text
            else:
                item = r.json()
        else:
            item = None

        response_data = {
            'data': item,
            'status_code': c
        }
        return response_data

    def claim_instance_mount(self, account_uid, project_uid, instance_uid):
        endpoint = '/accounts/{account_uid}/projects/{project_uid}/instances/{instance_uid}/claim_dataset_mount'.format(
            account_uid=account_uid,
            project_uid=project_uid,
            instance_uid=instance_uid
        )
        return self.put(params=endpoint)

    def get_dataset_version(self, account_uid, dataset_uid, version=None):
        if version is None:
            version = 'current'

        endpoint = '/accounts/{account_uid}/datasets/{dataset_uid}/version/{version}'.format(
            account_uid=account_uid,
            dataset_uid=dataset_uid,
            version=version
        )
        return self.get(params=endpoint)


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

    def add_bytes(self, bytes):
        lock = threading.Lock()
        with lock:
            self.bytes += bytes

    def get_files(self):
        return self.files

    def get_bytes(self):
        return self.bytes


class DatasetDownloadStatusPrinter:
    def __init__(self, stats):
        self.stats = stats

    def printStats(self):
        stats_string = 'Files: {files} Bytes: {bytes}'.format(files=self.stats.get_files(), bytes=self.stats.get_bytes())
        print(stats_string)


# TODO rename to AWS or something
class DownloadFileTracker(FileSystemEventHandler):

    def __init__(self, stats):
        self.stats = stats

    def on_created(self, event):
        if event.is_directory:
            return

        # Is it a temporary file?
        # With AWS S3 CLI last dot has 8 hexadecimal characters after it
        if event.src_path.count('.') > 1:
            last_dot_index = event.src_path.rfind('.')
            if len(event.src_path[last_dot_index + 1:]) == 8:
                print('temporary file - ', event.src_path)
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


# TODO need an initial check to make sure user has permissions, etc.
class DatasetDownloader(Thread):
    def __init__(self, path, heartbeat=6.0, timer_delay=5.0):
        Thread.__init__(self)

        self.path = path
        self.stop_flag = Event()
        self.heartbeat = heartbeat
        self.timer_delay = timer_delay
        self.timer = None

        self.file_stats = DatasetDownloadStatus(self.path)
        self.observer = Observer()

        self.started = False

        self.dataset_claim = None

        self.api = None

    #     Below should be an object or similar and passed in
        self.dataset_account_uid = 'vafilor2'
        self.dataset_project_uid = 'public2'
        self.instance_uid = 'test'
        self.dataset_uid = 'cats'
        self.dataset_version = '1'
        
    def start(self):
        Thread.start(self)

        conn = Connection()
        conn.load_credentials()

        self.api = DatasetAPI(conn)
        # TODO actual data
        response = self.api.claim_instance_mount(self.dataset_account_uid, self.dataset_project_uid, self.instance_uid)
        response_code = response['status_code']
        if response_code != 200:
            print('Error: {}'.format(response_code))
            self.stop_flag.set()
            self.observer = None
            return None

        self.dataset_claim = response['data']

        if not os.path.exists(self.path):
            os.makedirs(self.path)

        self.observer.schedule(DownloadFileTracker(self.file_stats), self.path, True)

        # Todo stop and return - make a cleanup function or something
        if self.start_downloading_dataset(conn) < 0:
            self.stop_flag.set()
            self.observer = None
            return None

        self.start_monitoring_files()
        self.start_updating_api()

        # TODO we need to set the function to be an API call that updates with the current status.
        # This class needs to keep track of status.
        # TODO callback

        self.started = True

    def run(self):
        while not self.stop_flag.wait(self.heartbeat):
            if self.started:
                print('thunk-thunk')

    def stop(self):
        if self.timer is not None:
            self.timer.stop()

        if self.observer is not None:
            self.observer.stop()

        self.stop_flag.set()

    def start_monitoring_files(self):
        self.observer.start()

    def start_updating_api(self):
        stats_printer = DatasetDownloadStatusPrinter(self.file_stats)
        self.timer = Timer(self.timer_delay, stats_printer.printStats)
        self.timer.start()

    def start_downloading_dataset(self, connection):
        # Authenticate for S3
        s3auth = S3Authenticator(connection)
        creds = s3auth.get_s3_credentials(self.dataset_account_uid, 'datasets', self.dataset_uid)
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

# TODO version information
        current_version = self.api.get_dataset_version(self.dataset_account_uid, self.dataset_uid, self.dataset_version)

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
        # TODO directory to download to
        exit_code = aws_util.download_all(self.path, s3_from_dir)
        if exit_code != 0:
            click.echo('\nError with downloading files.')
            return -1

        return 0

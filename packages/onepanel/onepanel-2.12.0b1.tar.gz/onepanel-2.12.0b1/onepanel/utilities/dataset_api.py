import json


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

    def claim_instance_mount(self, account_uid, project_uid, instance_uid, downloader_id, downloader_pid):
        endpoint = '/accounts/{account_uid}/projects/{project_uid}/instances/{instance_uid}/claim_dataset_mount'.format(
            account_uid=account_uid,
            project_uid=project_uid,
            instance_uid=instance_uid
        )

        post = {
            'downloaderID': downloader_id,
            'downloaderPID': downloader_pid
        }

        return self.put(params=endpoint, post_object=post)

    def get_dataset_version(self, account_uid, dataset_uid, version=None):
        if version is None:
            version = 'current'

        endpoint = '/accounts/{account_uid}/datasets/{dataset_uid}/version/{version}'.format(
            account_uid=account_uid,
            dataset_uid=dataset_uid,
            version=version
        )
        return self.get(params=endpoint)

    def update_dataset_mount_downloader(self, account_uid, project_uid, dataset_mount_uuid, files_downloaded, bytes_downloaded):
        endpoint = '/accounts/{account_uid}/projects/{project_uid}/dataset_mounts/{dataset_mount_uuid}/update'.format(
            account_uid=account_uid,
            project_uid=project_uid,
            dataset_mount_uuid=dataset_mount_uuid
        )

        post = {
            'filesDownloaded': files_downloaded,
            'bytesDownloaded': bytes_downloaded
        }

        return self.put(params=endpoint, post_object=post)
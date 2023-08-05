import sys
import threading

import boto3
import os


class Boto3Helpers:
	def __init__(self):
		pass

	def get_dataset_bucket_name(self):
		return os.getenv('DATASET_BUCKET', 'onepanel-datasets')

	def push(self, client, dataset_directory, s3_directory):
		# Upload the directory recursively
		for subdir, dirs, files in os.walk(dataset_directory):
			for file in files:
				filepath = subdir + os.sep + file
				# Make sure we don't upload .onepanel and anything under it
				if subdir.find('.onepanel') == -1:
					filepath_clean = filepath.lstrip('.')  # Get rid of current dir
					client.upload_file(file, self.get_dataset_bucket_name(),
									   s3_directory + filepath_clean,None, ProgressPercentageUpload(filepath))

	def download_dir(self, client, resource, dist, local='/tmp', bucket='your_bucket', ignore_dir_path=''):
		paginator = client.get_paginator('list_objects')
		for result in paginator.paginate(Bucket=bucket, Delimiter='/', Prefix=dist):
			if result.get('CommonPrefixes') is not None:
				for subdir in result.get('CommonPrefixes'):
					self.download_dir(client, resource, subdir.get('Prefix'), local, bucket, ignore_dir_path)
			if result.get('Contents') is not None:
				for file in result.get('Contents'):
					path_we_want = full_file_path = file.get('Key')
					if ignore_dir_path != '':
						# We don't want to recreate the entire S3 path, just everything after /output/*
						path_after_output = full_file_path.rpartition(ignore_dir_path)
						path_we_want = path_after_output[-1]
					if not os.path.exists(os.path.dirname(local + os.sep + path_we_want)):
						os.makedirs(os.path.dirname(local + os.sep + path_we_want))
					print("Downloading {file_name}".format(file_name=path_we_want))
					if path_we_want.endswith('/') is False:  # Check if this is a folder.
						# Check if os.sep is needed.
						# Some cases, we create double //<file|dir> and that causes an issue
						filename_for_dl = local + os.sep + path_we_want.lstrip('/')
						resource.meta.client.download_file(bucket, file.get('Key'),
														   filename_for_dl, None,
														   ProgressPercentageDownload(filename_for_dl))

	def download_compressed_file(self, client, resource, dist, local='/tmp', bucket='your_bucket',
								 compressed_file_name=''):
		paginator = client.get_paginator('list_objects')
		for result in paginator.paginate(Bucket=bucket, Delimiter='/', Prefix=dist):
			if result.get('Contents') is not None:
				for file in result.get('Contents'):
					full_file_path = file.get('Key')
					# We don't want to recreate the entire S3 path
					path_we_want = compressed_file_name
					if not os.path.exists(os.path.dirname(local + os.sep + path_we_want)):
						os.makedirs(os.path.dirname(local + os.sep + path_we_want))
					print("Downloading {file_name}".format(file_name=path_we_want))
					if path_we_want.endswith('/') is False:  # Check if this is a folder.
						filename_for_dl = local + os.sep + path_we_want
						resource.meta.client.download_file(bucket, file.get('Key'),
														   filename_for_dl, None,
														   ProgressPercentageDownload(filename_for_dl))


class ProgressPercentageUpload(object):
	def __init__(self, filename):
		self._filename = filename
		self._size = float(os.path.getsize(filename))
		self._seen_so_far = 0
		self._lock = threading.Lock()

	def __call__(self, bytes_amount):
		# To simplify we'll assume this is hooked up
		# to a single filename.
		with self._lock:
			self._seen_so_far += bytes_amount
			percentage = (self._seen_so_far / self._size) * 100
			sys.stdout.write(
				"\r%s  %s / %s  (%.2f%%)" % (
					self._filename, self._seen_so_far, self._size,
					percentage))
			sys.stdout.flush()


class ProgressPercentageDownload(object):
    def __init__(self, filename):
        self._filename = filename
        self._seen_so_far = 0
        self._lock = threading.Lock()
    def __call__(self, bytes_amount):
        # To simplify we'll assume this is hooked up
        # to a single filename.
        with self._lock:
            self._seen_so_far += bytes_amount
            sys.stdout.write(
                "\r%s --> %s bytes transferred" % (
                    self._filename, self._seen_so_far))
            sys.stdout.flush()
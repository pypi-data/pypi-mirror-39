import boto3
import os


class Boto3Helpers:
	def __init__(self):
		pass

	def download_dir(self, client, resource, dist, local='/tmp', bucket='your_bucket'):
		paginator = client.get_paginator('list_objects')
		for result in paginator.paginate(Bucket=bucket, Delimiter='/', Prefix=dist):
			if result.get('CommonPrefixes') is not None:
				for subdir in result.get('CommonPrefixes'):
					self.download_dir(client, resource, subdir.get('Prefix'), local, bucket)
			if result.get('Contents') is not None:
				for file in result.get('Contents'):
					full_file_path = file.get('Key')
					# We don't want to recreate the entire S3 path, just everything after /output/*
					path_after_output = full_file_path.rpartition('/output/')
					path_we_want = path_after_output[-1]
					if not os.path.exists(os.path.dirname(local + os.sep + path_we_want)):
						os.makedirs(os.path.dirname(local + os.sep + path_we_want))
					print("Downloading {file_name}".format(file_name=path_we_want))
					if path_we_want.endswith('/') is False: # Check if this is a folder.
						resource.meta.client.download_file(bucket, file.get('Key'), local + os.sep + path_we_want)

	def download_compressed_file(self, client, resource, dist, local='/tmp', bucket='your_bucket',compressed_file_name=''):
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
						resource.meta.client.download_file(bucket, file.get('Key'),
														   local + os.sep + path_we_want)
import string
import subprocess
import os
import sys


class AWSUtility:
	env = {} # Use for shell command environment variables

	def __init__(self,aws_access_key_id='',
				 aws_secret_access_key='',
				 aws_session_token=''):
		self.aws_access_key_id = aws_access_key_id
		self.aws_secret_access_key = aws_secret_access_key
		self.aws_session_token = aws_session_token
		self.env = {'AWS_ACCESS_KEY_ID': self.aws_access_key_id, 'AWS_SECRET_ACCESS_KEY': self.aws_secret_access_key,
			   'AWS_SESSION_TOKEN': self.aws_session_token}

	def get_dataset_bucket_name(self):
		return os.getenv('DATASET_BUCKET', 'onepanel-datasets')

	def upload_dir(self, dataset_directory, s3_directory,exclude=''):
		s3_path = 's3://{bucket}/{path}'.format(bucket=self.get_dataset_bucket_name(), path=s3_directory)
		aws_full_path = self.get_full_path_to_aws_cli()
		if "aws" in aws_full_path:
			# Need to pass the command as one long string. Passing in a list does not work when executed.
			exclude_arg = '--exclude "{ex_str}"'.format(ex_str=exclude)
			cmd = ' '.join([aws_full_path, 's3', 'sync', dataset_directory, s3_path,exclude_arg])
			# Also need to execute through the shell
			p = subprocess.Popen(args=cmd, env=self.env,stdin=subprocess.PIPE, stdout=subprocess.PIPE,
						 		stderr=subprocess.PIPE, shell=True)
			suppress_s3_info = s3_path.rsplit('/', 1)[0]
			for line in iter(p.stdout.readline, '' or b''):  # replace '' with b'' for Python 3
				line_str = line.decode()
				cleaned_line = line_str.replace(suppress_s3_info, '')
				sys.stdout.write(cleaned_line)
			return 0
		return -1

	def download_all(self, dataset_directory, s3_directory):
		s3_path = 's3://{bucket}/{path}'.format(bucket=self.get_dataset_bucket_name(), path=s3_directory)
		aws_full_path = self.get_full_path_to_aws_cli()
		if "aws" in aws_full_path:
			# Need to pass the command as one long string. Passing in a list does not work when executed.
			cmd = ' '.join([aws_full_path, 's3', 'sync', s3_path, dataset_directory])
			# Also need to execute through the shell
			p = subprocess.Popen(args=cmd, env=self.env, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
							 stderr=subprocess.PIPE, shell=True)
			suppress_s3_info = s3_path.rsplit('/', 1)[0]
			for line in iter(p.stdout.readline, '' or b''):  # replace '' with b'' for Python 3
				line_str = line.decode()
				cleaned_line = line_str.replace(suppress_s3_info, '')
				sys.stdout.write(cleaned_line)
			return 0
		return -1

	def download(self,to_dir,s3_full_path_to_file):
		s3_path = 's3://{bucket}/{path}'.format(bucket=self.get_dataset_bucket_name(), path=s3_full_path_to_file)
		aws_full_path = self.get_full_path_to_aws_cli()
		if "aws" in aws_full_path:
			# Need to pass the command as one long string. Passing in a list does not work when executed.
			cmd = ' '.join([aws_full_path,'s3', 'cp', s3_path, to_dir])
			# Also need to execute through the shell
			p = subprocess.Popen(args=cmd, env=self.env, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
							 stderr=subprocess.PIPE, shell=True)
			suppress_s3_info = s3_path.rsplit('/',1)[0]
			for line in iter(p.stdout.readline, '' or b''):  # replace '' with b'' for Python 3
				line_str = line.decode()
				cleaned_line = line_str.replace(suppress_s3_info,'')
				sys.stdout.write(cleaned_line)
			return 0
		return -1

	def check_s3_path_for_files(self,full_s3_path='',recursive=True):
		ret_val = {'data':None, 'code':-1, 'msg':''}
		if full_s3_path == '':
			ret_val = {'data': None, 'code': -1, 'msg': 'Need the full s3 path passed in.'}
			return ret_val
		aws_full_path = self.get_full_path_to_aws_cli()
		if "aws" in aws_full_path:
			recursive_arg = ''
			if recursive:
				recursive_arg = '--recursive'
			# Need to pass the command as one long string. Passing in a list does not work when executed.
			cmd = ' '.join([aws_full_path, 's3', 'ls',recursive_arg,'--summarize',full_s3_path])
			# Also need to execute through the shell
			p = subprocess.Popen(args=cmd, env=self.env,stdin=subprocess.PIPE, stdout=subprocess.PIPE,
							 stderr=subprocess.PIPE, shell=True)
			p.wait()
			raw_output = p.stdout.readlines()
			for line in raw_output:
				if 'Total Objects' in line.decode():
					objects_str = line.decode()
					str_split = objects_str.split(':')
					# Grab the string of the number
					string_num = str_split[-1].strip()
					ret_val = {'data': int(string_num), 'code': 0, 'msg': 'Total files found.'}
					break
			return ret_val
		return ret_val
	def get_full_path_to_aws_cli(self):
		# Figure out the full path to awscli
		path_to_aws_cmd = ['which', 'aws']
		p = subprocess.Popen(args=path_to_aws_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
							 stderr=subprocess.PIPE, shell=False)
		p.wait()
		line = p.stdout.readline()
		return line.decode().rstrip()

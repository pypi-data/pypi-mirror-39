import subprocess


class AwsS3Dataset:
    def __init__(self):
        pass

    def push(self, dataset_directory, s3_directory):
        s3_path = 's3://onepanel-datasets/{path}'.format(path=s3_directory)
        subprocess.run(['aws', 's3', 'cp', dataset_directory, s3_path, '--recursive'])

    def clone(self, dataset_directory, s3_directory):
        s3_path = 's3://onepanel-datasets/{path}'.format(path=s3_directory)
        subprocess.run(['aws', 's3', 'cp', s3_path, dataset_directory, '--recursive'])

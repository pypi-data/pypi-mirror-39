import boto3


class S3Downloader(object):

    def __init__(self, bucket_name):
        self.s3 = boto3.resource('s3')
        self.bucket_name = bucket_name

    def download(self, file_name, s3_object_name):

            print('Downloading file ' + s3_object_name)

            try:
                obj = self.s3.Object(self.bucket_name, s3_object_name).download_file(file_name)
            except Exception as e:
                print('!! Got an error while Downloading file {file} to the S3 bucket {bucket}. Error: {error}'.format(
                    file=s3_object_name,
                    bucket=self.bucket_name,
                    error=e
                ))
                raise e
            else:
                print('Downloaded file ' + s3_object_name )
                return obj

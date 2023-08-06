import boto3


class S3Uploader(object):

    def __init__(self, bucket_name):
        self.s3 = boto3.resource('s3')
        self.bucket_name = bucket_name

    def upload(self, file_name, s3_object_name):
        with open(file_name, 'rb') as file:

            print('Uploading file ' + file_name + ' to object ' + s3_object_name)

            try:
                self.s3.Object(self.bucket_name, s3_object_name).put(Body=file)
            except Exception as e:
                print('!! Got an error while uploading file {file} to the S3 bucket {bucket}. Error: {error}'.format(
                    file=file_name,
                    bucket=self.bucket_name,
                    error=e
                ))
            else:
                print('Uploaded file ' + file_name + ' to object ' + s3_object_name)

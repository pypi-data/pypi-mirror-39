# S3-Utils

This is a simple S3 utils package, used to upload and download file.

### Scope

* Upload file to S3
* Download file from S3

### Setup and install 

``` pip install s3utils ```

### Usage 1

``` 
from s3utils.s3_uploader import S3Uploader

S3Uploader(bucket_name='bucket_name').upload(file_name='file_name', s3_object_name='s3_object_name')

```

### Usage 2

```
from s3utils.s3_downloader import S3Downloader

S3Downloader(bucket_name='bucket_name').download(file_name='hello.txt', s3_object_name='s3_object_name')

```


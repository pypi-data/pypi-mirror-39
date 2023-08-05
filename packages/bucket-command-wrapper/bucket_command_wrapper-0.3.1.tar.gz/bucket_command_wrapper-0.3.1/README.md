# bucket_command_wrapper
Wrapper to facilitate downloading / uploading files from buckets (i.e. S3) into containers (i.e. docker) and running an arbitrary command.

This is a typical challenge when attempting to containerize software that is not bucket (s3) aware and run it on something like AWS batch.

This small script will download from a bucket store files to temporary locations within the container filesystem, invoke a command,
and then upload the results back to specified keys within buckets. 

Version 0.1 only supports s3, but the general structure can support a variety of bucket stores, including sftp eventually.

## Usage:
```
bucket_command_wrapper [-h] [--command COMMAND]
                              [--download-files DOWNLOAD_FILES]
                              [--upload-files UPLOAD_FILES]

Wrapper to pull from buckets, run a command, and push back to buckets.
example: bucket_command_wrapper.py -c 'echo hello' 
-DF s3://bucket/key/path.txt::/mnt/inputs/path.txt::rw
-DF s3://bucket/key/path2.txt::/mnt/inputs/path2.txt::ro 
-UF /mnt/outputs/path.txt::s3://bucket/key/path.txt

optional arguments:
  -h, --help            show this help message and exit
  --command COMMAND, -c COMMAND
                        Command to be run AFTER downloads BEFORE uploads.
                        Please enclose in quotes. Will be passed unaltered as
                        a shell command. Can also be provided as an
                        environmental variable bcw_command
  --download-files DOWNLOAD_FILES, -DF DOWNLOAD_FILES
                        Format is bucket_file_uri::container_path::mode Where
                        mode can be 'ro' or 'rw'. If 'rw' the file will be
                        pushed back to the bucket after the command IF 'ro,
                        the file will only be pulled from the bucket e.g:
                        s3://bucket/key/path.txt::/mnt/inputs/path.txt::ro
  --upload-files UPLOAD_FILES, -UF UPLOAD_FILES
                        Format is container_path::bucket_file_uri Mode is
                        presumed to be w. (If you want rw / a / use input in
                        mode 'rw') e.g:
                        /mnt/outputs/path.txt::s3://bucket/key/path.txt
```

import botocore
import botocore.exceptions
from Logger import Logger


class S3Controller:
    # A class for controlling interactions with amazon's S3 service
    BUCKET_DISPLAY_FORMAT = '  {0}\t <Created on:{1}>'
    OBJECT_DISPLAY_FORMAT = '\t<{0}>'
    STR_BUCKET_OBJECTS = "<Bucket '{}' Objects>"
    STR_S3_BUCKETS = "<AWS S3 Buckets>"
    MSG_PROMPT_OVERRIDE_OBJECT = "Object with key {} already exist.Do you want to override(Y/N):"
    MSG_INFO_DELETING_OBJECT = "Deleting Object '{}' from bucket '{}'"
    MSG_INFO_DOWNLOADING_OBJECT = "Downloading Object '{}' from bucket '{}'"
    MSG_INFO_UPLOADING_OBJECT = "Uploading Object '{}' in bucket '{}'"
    MSG_WARN_NO_BUCKET = "There is no S3 Bucket at this moment.."
    MSG_WARN_NO_OBJECT = "There is no Object in '{}' Bucket at this moment.."
    MSG_WARN_UPLOAD_CANCEL = "Uploading of file '{}' cancelled"
    MSG_WARN_OBJECT_OVERRIDE = "Overriding Object {}"
    MSG_ERR_WRONG_INPUT = "Wrong Input:{}"

    def __init__(self, s3res):
        # S3Controller Constructor
        self.s3 = s3res

    def list_buckets(self):
        # Print out a list of all s3 buckets your credentials have created
        count = 0
        bucket_list = []
        bucket_obj_list = []
        for bucket in self.s3.buckets.all():
            bucket_obj_list.append(bucket)
            bucket_list.append(bucket.name)
            count += 1
        if count == 0:
            Logger.warn(self.MSG_WARN_NO_BUCKET)
        else:
            Logger.header(self.STR_S3_BUCKETS)
            for bucket in bucket_obj_list:
                Logger.info(self.BUCKET_DISPLAY_FORMAT.format(bucket.name, bucket.creation_date))
        return bucket_list

    def list_bucket_objects(self, bucket_name):
        # Print all objects of the S3 bucket with name 'bucket_name'
        objects_list = []
        count = 0
        for s3_object in self.s3.Bucket(bucket_name).objects.all():
            objects_list.append(s3_object.key)
            count += 1
        if count == 0:
            Logger.warn(self.MSG_WARN_NO_OBJECT.format(bucket_name))
        else:
            Logger.header(self.STR_BUCKET_OBJECTS.format(bucket_name))
            for s3_object in objects_list:
                Logger.info(self.OBJECT_DISPLAY_FORMAT.format(s3_object))
        return objects_list

    def upload_file(self, bucket_name, file_name, key):
        # Upload the file 'file_name' to S3 storage, into the bucket 'bucket_name'. The name 'key' will
        # be used to reference the file in the S3 storage
        try:
            self.s3.Object(bucket_name, key).load()
            user_opt = input(self.MSG_PROMPT_OVERRIDE_OBJECT.format(key))
            if user_opt == 'Y' or user_opt == 'y':
                Logger.warn(self.MSG_WARN_OBJECT_OVERRIDE.format(key))
                self.s3.Bucket(bucket_name).upload_file(file_name, key)
                Logger.info(self.MSG_INFO_UPLOADING_OBJECT.format(file_name, bucket_name))
            elif user_opt == 'N' or user_opt == 'n':
                Logger.warn(self.MSG_WARN_UPLOAD_CANCEL.format(key))
            else:
                Logger.warn(self.MSG_ERR_WRONG_INPUT.format(user_opt))
        except botocore.exceptions.ClientError as error:
            if error.response['Error']['Code'] == "404":
                self.s3.Bucket(bucket_name).upload_file(file_name, key)
                Logger.info(self.MSG_INFO_UPLOADING_OBJECT.format(file_name, bucket_name))
            else:
                Logger.err(str(error))

    def download_file(self, bucket_name, key, local_file_name):
        # Download the file referenced by 'key' in the S3 bucket with
        # name 'bucket_name', to the file location 'local_file_name'
        try:
            self.s3.Bucket(bucket_name).download_file(key, local_file_name)
            Logger.info(self.MSG_INFO_DOWNLOADING_OBJECT.format(key, bucket_name))
        except botocore.exceptions.ClientError as error:
            Logger.err(str(error))

    def delete_file(self, bucket_name, key):
        # Delete the file with key 'key' from S3 storage, from the bucket 'bucket_name'
        try:
            bucket = self.s3.Bucket(bucket_name)
            bucket.delete_objects(Delete={"Objects": [{"Key": key}]})
            Logger.info(self.MSG_INFO_DELETING_OBJECT.format(key, bucket_name))
        except botocore.exceptions.ClientError as error:
            Logger.err(str(error))

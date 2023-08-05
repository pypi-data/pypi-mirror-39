#!/usr/bin/env python
import sys
import os
import boto3
import time
import vmtools
from awsretry import AWSRetry
import botohelper.route53 as route53
import botohelper.botohelpermain
import botocore.exceptions
import botocore.client

vm_root_path = vmtools.vm_root_grabber()
sys.path.append(vm_root_path)
from local_settings import *

class S3(botohelper.botohelpermain.Main):
    """Class to manipulate aws ec2 resources

    public methods:

    instance variables:
    self.aws_profile
    self.aws_region
    self.session
    self.client_ec2
    self.ec2
    self.availability_zones_list
    self.route53
    """

    def __init__(self, aws_profile, aws_region):
        """set instance variables, set instance aws connections

        keyword arguments:
        :type aws_profile: string
        :param aws_profile: the profile to use from ~/.aws/credentials to connect to aws
        :type aws_region: string
        :param aws_region: the region to use for the aws connection object (all resources will be created in this region)
        """
        super().__init__(aws_profile=aws_profile, aws_region=aws_region)
        self.client_s3 = self.session.client('s3', region_name=self.aws_region)
        self.resource_s3 = self.session.resource('s3', region_name=self.aws_region)


    def get_matching_s3_objects(self, bucket, prefix='', suffix=''):
        """
        Return a generator of matching objects from an S3 bucket.
    
        :type bucket: string
        :param bucket: Name of the S3 bucket.
        :type prefix: string or tuple
        :param prefix: (Optional) Only fetch objects whose key starts with
        :type suffix: string or tuple
        :param suffix: (Optional) Only fetch objects whose keys end with
        """
        kwargs = {'Bucket': bucket}
    
        # If the prefix is a single string (not a tuple of strings), we can
        # do the filtering directly in the S3 API.
        if isinstance(prefix, str):
            kwargs['Prefix'] = prefix
    
        while True:
    
            # The S3 API response is a large blob of metadata.
            # 'Contents' contains information about the listed objects.
            resp = self.client_s3.list_objects_v2(**kwargs)
    
            try:
                contents = resp['Contents']
            except KeyError:
                return
    
            for obj in contents:
                key = obj['Key']
                if key.startswith(prefix) and key.endswith(suffix):
                    yield obj
    
            # The S3 API is paginated, returning up to 1000 keys at a time.
            # Pass the continuation token into the next response, until we
            # reach the final page (when this field is missing).
            try:
                kwargs['ContinuationToken'] = resp['NextContinuationToken']
            except KeyError:
                break
    
    
    def get_matching_s3_keys(self, bucket, prefix='', suffix=''):
        """
        Generate the keys in an S3 bucket.
    
        :type bucket: string
        :param bucket: Name of the S3 bucket.
        :type prefix: string or tuple
        :param prefix: (Optional) Only fetch objects whose key starts with
        :type suffix: string or tuple
        :param suffix: (Optional) Only fetch objects whose keys end with
        """
        for obj in self.get_matching_s3_objects(bucket, prefix, suffix):
            yield obj['Key']

    def is_s3_bucket_encrypted(self, bucket):
        """
        Check if the S3 bucket is has encryption set, if so return the 'Rules' list, if not return None
    
        :type bucket: string
        :param bucket: Name of the S3 bucket.
        """
        try:
            response = self.client_s3.get_bucket_encryption(Bucket=bucket)
        except botocore.exceptions.ClientError as e:
            return None
        return response['ServerSideEncryptionConfiguration']['Rules']

    def is_s3_object_encrypted(self, bucket, key):
        """
        Check if the S3 object is encrypted, if so return True, if not return False
    
        :type bucket: string
        :param bucket: Name of the S3 bucket.
        :type key: string
        :param key: The S3 key
        """
        s3_object = self.resource_s3.Object(bucket, key)
        if s3_object.server_side_encryption:
            return True
        else:
            return False

    def does_s3_bucket_exist(self, bucket):
        """
        Check if the S3 bucket exists, if so return True, otherwise return False
    
        :type bucket: string
        :param bucket: Name of the S3 bucket.
        """
        try:
            self.resource_s3.meta.client.head_bucket(Bucket=bucket)
        except botocore.client.ClientError as e:
            return False
        return True

    def enable_default_encryption_on_s3_bucket(self, bucket):
        """
        Enable the default, transparent encryption (AES256) on the given bucket
    
        :type bucket: string
        :param bucket: Name of the S3 bucket.
        """
        self.client_s3.put_bucket_encryption(Bucket=bucket, ServerSideEncryptionConfiguration={'Rules': [{'ApplyServerSideEncryptionByDefault': {'SSEAlgorithm': 'AES256'}}]})

    def disable_default_encryption_on_s3_bucket(self, bucket):
        """
        Disable encryption on the given bucket
    
        :type bucket: string
        :param bucket: Name of the S3 bucket.
        """
        self.client_s3.delete_bucket_encryption(Bucket=bucket)

    def get_list_of_all_buckets(self):
        """
        Return a list of the all the buckets for the current account
        """
        all_bucket_objects_dict = self.client_s3.list_buckets()
        all_buckets_list = [ bucket_dict['Name'] for bucket_dict in all_bucket_objects_dict['Buckets'] ]
        return all_buckets_list

    def delete_bucket(self, bucket):
        """
        Delete bucket and all key within it
        :type bucket: string
        :param bucket: Name of the S3 bucket.
        """
        bucket_object = self.resource_s3.Bucket(bucket) 
        for bucket_key in bucket_object.objects.all():
            bucket_key.delete()
        bucket_object.delete()

    def copy_s3_object_between_buckets(self, src_bucket, s3_object_key, dest_bucket, verbose=False):
        """
        Copy a single S3 object from one S3 bucket to another
        :type src_bucket: string
        :param src_bucket: Name of the source S3 bucket.
        :type s3_object_key: string
        :param s3_object_key: The key of the object to be copied
        :type dest_bucket: string
        :param dest_bucket: Name of the destination S3 bucket.
        :type verbose: boolean
        :param verbose: if True prints out the source and destination for each object copied
        """
        if verbose:
            copy_message = 'copying s3://{}/{} to s3://{}/{}'.format(src_bucket, s3_object_key, dest_bucket, s3_object_key)
            print(copy_message)
        response = self.client_s3.copy_object(Bucket=dest_bucket, Key=s3_object_key, CopySource={'Bucket': src_bucket, 'Key': s3_object_key})

    def create_copy_of_s3_bucket(self, src_bucket, dest_bucket, copy_only_mising_objects=False, copy_only_unencrypted_objects=False, dest_bucket_tags=False, verbose=False):
        """
        Copy all keys from src_bucket to dest_bucket
    
        :type src_bucket: string
        :param src_bucket: Name of the source S3 bucket.
        :type dest_bucket: string
        :param dest_bucket: Name of the destination S3 bucket.
        :type copy_only_mising_objects: boolean
        :param copy_only_mising_objects: If True only the files not already in dest_bucket will be copied
        :type copy_only_unencrypted_objects: boolean
        :param copy_only_unencrypted_objects: If True only the unencrypted files src_bucket will be copied
        :type dest_bucket_tags: list of dicts
        :param dest_bucket_tags: a list of tag dicts (if False no tags are created) ex: [{'Key': 'Name','Value': 'mybucket'}, {'Key': 'environment','Value': 'prod'}] 
        :type verbose: boolean
        :param verbose: if True prints out the source and destination for each object copied
        """
        # make sure dest_bucket exists
        dest_bucket_object = self.resource_s3.create_bucket(Bucket=dest_bucket)
        if dest_bucket_tags:
            self.client_s3.put_bucket_tagging(Bucket=dest_bucket,Tagging={'TagSet': dest_bucket_tags } )
        src_bucket_object = self.resource_s3.Bucket(src_bucket)
        # create objects_to_copy_list based on missing objects if requested
        if copy_only_mising_objects:
            src_bucket_generator = self.get_matching_s3_keys(bucket=src_bucket)
            dest_bucket_generator = self.get_matching_s3_keys(bucket=dest_bucket)
            src_bucket_generator_set = set(src_bucket_generator)
            dest_bucket_generator_set = set(dest_bucket_generator)
            objects_to_copy_list = list(src_bucket_generator_set - dest_bucket_generator_set)
        # otherwise create objects_to_copy_list based on all files
        else:
            objects_to_copy_list = [ s3_object.key for s3_object in src_bucket_object.objects.all() ]
        # filter out the already encrypted if requested
        if copy_only_unencrypted_objects:
            updated_objects_to_copy_list = []
            for s3_key in objects_to_copy_list:
                if not self.is_s3_object_encrypted(bucket=src_bucket, key=s3_key):
                    updated_objects_to_copy_list.append(s3_key)
            objects_to_copy_list = updated_objects_to_copy_list
        # copy objects
        for s3_object_key in objects_to_copy_list:
            if verbose:
                copy_message = 'copying s3://{}/{} to s3://{}/{}'.format(src_bucket, s3_object_key, dest_bucket, s3_object_key)
                print(copy_message)
            response = self.client_s3.copy_object(Bucket=dest_bucket, Key=s3_object_key, CopySource={'Bucket': src_bucket, 'Key': s3_object_key})

    def download_s3_file(self, bucket, remote_file_to_download, local_absolute_path):
        """
        download the remote_file_to_download from s3 to local_absolute_path
    
        :type bucket: string
        :param bucket: Name of the S3 bucket.
        :type remote_file_to_download: string
        :param remote_file_to_download: the key of the remote file to download from s3
        :type local_absolute_path: string
        :param local_absolute_path: the absolute path where to download remote_file_to_download
        """
        self.client_s3.download_file(bucket, remote_file_to_download, local_absolute_path)

    def request_restore_from_glacier(self, bucket, key, number_of_days):
        """
        Request a resotre from glaicer to s3 return the response
    
        :type bucket: string
        :param bucket: Name of the S3 bucket.
        :type key: string
        :param key: the key of the remote file to restore from glacier
        :type number_of_days: int
        :param number_of_days: the number of days the restore should be available for (lowest would be 1 but a higher number may incur more cost)
        """
        bucket_obj = self.resource_s3.Bucket(bucket)
        object_summary_iterator = bucket_obj.objects.filter(Prefix=key)
        object_summary_list = []
        for object_summary in object_summary_iterator:
            object_summary_list.append(object_summary)
        if len(object_summary_list) == 0:
            return None
        elif len(object_summary_list) > 1:
            raise ValueError('object_summary_list should only have 1 or 0 object, key filter must not be specific enough')
        request_response = bucket_obj.meta.client.restore_object(Bucket=bucket, Key=key, RestoreRequest={'Days': number_of_days})
        return request_response

    def get_restore_expiration_date(self, bucket, key):
        """
        Return a dict with the expiration info of a glacier restore key, Return None if not restored
    
        :type bucket: string
        :param bucket: Name of the S3 bucket.
        :type key: string
        :param key: the key of the remote file
        """

        s3_object = self.resource_s3.Object(bucket,key)
        s3_object_expiration_dict = {}
        if s3_object.restore:
            for value_key_pair in s3_object.restore.split('", '):
                s3_object_expiration_dict[value_key_pair.split('="')[0]] = value_key_pair.split('="')[1].strip('"')
        else:
            return None

        return s3_object_expiration_dict



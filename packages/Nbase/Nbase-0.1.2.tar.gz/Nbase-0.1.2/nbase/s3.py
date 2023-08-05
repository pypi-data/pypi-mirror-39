#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: 丁卫华(weihua.ding@nio.com)
#
# Created: 2018/11/15 下午7:16

import boto3


class S3Fun(object):
    """
    The S3 function object
    """
    def __init__(self, region, access_key_id, secret_access_key, bucket):
        """

        """
        self.region = region
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.bucket = bucket

    def get_s3_resource(self):
        """
        获取s3 resource
        :return:
        """
        return boto3.resource(
            service_name='s3',
            region_name=self.region,
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key
        )

    def s3_upload_file(self, local_file, s3_file, s3_resource=None):
        """
        往S3上上传文件
        :param local_file:
        :param s3_file:
        :param s3_resource:
        :return:
        """
        if not s3_resource:
            s3_resource = self.get_s3_resource()
        s3_resource.Object(self.bucket, s3_file).upload_file(local_file)

    def s3_upload_str2file(self, data_str, s3_file, s3_resource=None):
        """
        往S3上上传文件
        :param data_str:
        :param s3_file:
        :param s3_resource:
        :return:
        """
        if not s3_resource:
            s3_resource = self.get_s3_resource()
        s3_resource.Bucket(self.bucket).put_object(Key=s3_file, Body=data_str)

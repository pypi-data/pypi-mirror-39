from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from qcloud_cos import CosServiceError
from qcloud_cos import CosClientError

class CosUtil(object):

    app_id = ''
    client = False
    
    def __init__(self, app_id, secret_id, secret_key, token, region, scheme):
        config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
        self.client = CosS3Client(config)
        self.app_id = app_id

    def putFile(self, bucket, local_file_path, cos_file_path):
        response = self.client.put_object_from_local_file(
            Bucket=bucket + '-' + self.app_id,
            LocalFilePath=local_file_path,
            Key=cos_file_path,
        )
        return response['ETag']

    def listBucket(self, bucket, prefix):
        items = []
        response = self.client.list_objects(
            Bucket=bucket + '-' + self.app_id,
            Prefix=prefix 
        )

        if 'Contents' in response and response['Contents']:
            for item in response['Contents']:
                items.append(item['Key'])
        return items

    def getFile(self, bucket, cos_file_path):
        response = self.client.get_object(
            Bucket=bucket + '-' + self.app_id,
            Key=cos_file_path
        )
        return response



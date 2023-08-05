import json
import os
import snark
from snark import config
from snark.log import logger
from snark.client.base import SnarkHttpClient
from snark.exceptions import SnarkException

from subprocess import Popen, PIPE

class StoreControlClient(SnarkHttpClient):
    """
    Controlling Snark Pods through rest api
    """
    def __init__(self):
        super(StoreControlClient, self).__init__()
        self.details = self.get_config()

    def s3cmd(self, type='ls', source='', target='', recursive = False):
        snark = 'snark://'
        s3 = 's3://'+self.details['bucket']+'/'
        if 'snark://' in source:
            source = source.replace(snark, s3)

        if 'snark://' in target:
            target = target.replace(snark, s3)

        rec = ['-r'] if recursive else []
        cmd = ['s3cmd', type, source, target] + rec
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE)
        output = p.stdout.read()
        print(output.decode('utf-8').replace(s3, snark)[:-1])

    def get_credentials(self):
        r = self.request(
            'GET', config.GET_CREDENTIALS_SUFFIX,
            endpoint=config.SNARK_HYPER_ENDPOINT,
        ).json()

        details = {
            "host_base": r['endpoint'],
            "host_bucket": r['endpoint'],
            "bucket": r['bucket'],
            "bucket_location": r['bucket_location'],
            "use_https": r['use_https'],
            "access_key" : r['access_key'],
            "secret_key": r['secret_key'],
            "signature_v2": False
        }

        self.save_config(details)

    def get_config(self):
        if not os.path.isfile(config.STORE_CONFIG_PATH):
            self.get_credentials()

        with open(config.STORE_CONFIG_PATH, 'r') as file:
            details = file.readlines()
        return json.loads(''.join(details))

    def save_config(self, details):
        with open(config.STORE_CONFIG_PATH, 'w') as file:
            file.writelines(json.dumps(details))

        s3cmd_config = [str(key)+' = '+details[key] for key in details]
        with open(config.S3CMD_CONFIG_PATH, 'w') as file:
            file.writelines('\n'.join(s3cmd_config))

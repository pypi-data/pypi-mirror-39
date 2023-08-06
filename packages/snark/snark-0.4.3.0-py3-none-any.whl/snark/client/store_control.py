import json
import os
import snark
import time
from snark import config
from snark.log import logger
from snark.client.base import SnarkHttpClient
from snark.exceptions import SnarkException
import pprint
from subprocess import Popen, PIPE
import subprocess

class StoreControlClient(SnarkHttpClient):
    """
    Controlling Snark Pods through rest api
    """
    def __init__(self):
        super(StoreControlClient, self).__init__()
        self.details = self.get_config()

    def s3cmd(self, type='ls', source='', target='', recursive = False, stream_output = True):
        snark = 'snark://'
        s3 = self.details['bucket']+'/'
        if 'snark://' in source:
            source = source.replace(snark, s3)

        if 'snark://' in target:
            target = target.replace(snark, s3)

        rec = ['-r'] if recursive else []
        target = [target] if len(target)>0 else []
        cmd = ['aws', 's3', type, source] + target + rec

        details = self.get_config()
        env = os.environ.copy()
        env['AWS_ACCESS_KEY_ID'] = details['access_key']
        env['AWS_SECRET_ACCESS_KEY'] = details['secret_key']
        env['AWS_SESSION_TOKEN'] = details['access_token']

        self.run_command(cmd, env, s3, snark)

    def run_command(self, command, env, s3, snark):
        process = Popen(command, stdout=subprocess.PIPE, env=env)
        while True:
            output = process.stdout.readline()
            output = output.decode('utf-8')
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.replace(s3, snark)[:-1])
        rc = process.poll()
        return rc

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
            "access_token": r['session_token'],
            "expiration": r['expiration'],
            "signature_v2": False
        }
        self.save_config(details)
        return details

    def get_config(self):
        if not os.path.isfile(config.STORE_CONFIG_PATH):
            self.get_credentials()

        with open(config.STORE_CONFIG_PATH, 'r') as file:
            details = file.readlines()
            details = json.loads(''.join(details))
            
        if float(details['expiration'])<time.time():
            details = self.get_credentials()

        return details

    def save_config(self, details):
        with open(config.STORE_CONFIG_PATH, 'w') as file:
            file.writelines(json.dumps(details))

        #s3cmd_config = [str(key)+' = '+str(details[key]) for key in details]
        #with open(config.S3CMD_CONFIG_PATH, 'w') as file:
        #    file.writelines('\n'.join(s3cmd_config))

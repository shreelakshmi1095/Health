#!/usr/bin/env python

import requests
import argparse
import base64
from datetime import datetime

def getToken():
    req = requests.put("http://169.254.169.254/latest/api/token", headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"})
    return req.text.strip()

def getInstanceId(token):
    req = requests.get('http://169.254.169.254/latest/dynamic/instance-identity/document/', headers={"X-aws-ec2-metadata-token": token})
    details = req.json()
    instanceId = details['instanceId']
    return instanceId


def getAccountId(token):
    req = requests.get('http://169.254.169.254/latest/meta-data/identity-credentials/ec2/info/', headers={"X-aws-ec2-metadata-token": token})
    details = req.json()
    accountId = details['AccountId']
    return accountId


def encrypt(metadataStr, encryptKey):
    key_len = len(encryptKey)
    secret = []
    i = 0
    for char in metadataStr:
        if i >= key_len:
            i = i % key_len
        secret.append(chr(ord(char) ^ ord(encryptKey[i])))
        i += 1
    return base64.urlsafe_b64encode("".join(secret).encode()).decode()


def decrypt(secret, encryptKey):
    msg = base64.urlsafe_b64decode(secret.encode()).decode()
    key_len = len(encryptKey)
    decrypted = []
    i = 0
    for char in msg:
        if i >= key_len:
            i = i % key_len
        decrypted.append(chr(ord(char) ^ ord(encryptKey[i])))
        i += 1
    return "".join(decrypted)


if __name__ == "__main__":

    argParser = argparse.ArgumentParser(
            description='Get unique details for EC2 metadata service',
            usage='%(prog)s [--student-id 117454 --student-name Ola Fayomi]')
    argParser.add_argument('--student-id', dest='student_id',
                           help='Your student ID', required=True,
                           default=None)
    argParser.add_argument('--student-name', dest='student_name',
                           nargs='*',
                           help='Your student name', required=True,
                           default=None)
    args = argParser.parse_args()
    key="Peter Piper picked a peck of pickled peppers"
    name = ' '.join(args.student_name)
    token = getToken()
    inst_id = getInstanceId(token)
    acc_id = getAccountId(token)
    metadata_str = inst_id+','+args.student_id+','+name+','+str(acc_id)
    encrypted_str = encrypt(metadata_str,key)
    print(encrypted_str)
    decrypted_str = decrypt(encrypted_str, key)
    print(decrypted_str)

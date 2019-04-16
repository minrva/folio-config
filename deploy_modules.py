#!/usr/bin/env python3
"""Deploys Okapi modules."""
import os
import json
import requests
import time


DEPLOY_URL = 'http://localhost:9130/_/discovery/modules'
DEPLOYMENT_DESCR_DIR = 'folio-configs/deployment-descriptors'


def load_json(fpath):
    """Loads a JSON file."""
    with open(fpath) as fs:
        d = json.load(fs)
    return d


def deploy_module(url, payload):
    """Deploys an Okapi module."""
    headers = {'content-type': 'application/json'}
    r = requests.post(url, headers=headers, json=payload)
    if r.status_code != 201:
        print(r.text)
    return r.status_code


def deploy_all_modules(dir_path):
    """ Deploys an Okapi module for each deployment descriptor found
    in the configuration directory.
    """
    for file_name in os.listdir(dir_path):
        print('Deploying {0}...'.format(file_name))
        file_path = os.path.join(dir_path, file_name)
        json_data = load_json(file_path)
        req_status = deploy_module(DEPLOY_URL, json_data)
        print('Request returned with {0}...'.format(req_status))
        time.sleep(2)


if __name__ == '__main__':
    home_path = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(home_path, DEPLOYMENT_DESCR_DIR)
    deploy_all_modules(config_path)

# -*- coding: utf8 -*-

from __future__ import print_function
import os,sys
import yaml
import acm
from acm import files
import time
import shutil
import json
import platform

class ConfigCenter():
    def __init__(self,conf=None,confFile='config_center.yaml',accessFile='access.yaml'):
        self.system = platform.system()
        #print(self.system)
        if not conf:

            PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
            confFile = os.path.join(PROJECT_ROOT, confFile)
            config = yaml.load(open(confFile).read())
            conf = {
                "ENDPOINT": config["ENDPOINT"],
                "NAMESPACE": config["NAMESPACE"],
            }
            access = None
            if accessFile:
                accessFile = os.path.join(PROJECT_ROOT, accessFile)
                if os.path.exists(accessFile):
                    access = yaml.load(open(accessFile).read())
                    conf["AK"]= access["AK"]
                    conf["SK"]= access["SK"]
            else:
                conf["RAM_ROLE_NAME"]= config["RAM_ROLE_NAME"]


        self.get_conf_from_cc(conf)

    def get_conf_from_cc(self,conf=None):
        if not conf:
            raise Exception('conf can not be null!')
        #acm.ACMClient.set_debugging()
        if conf.get("AK") and conf.get("SK"):
            self.client = acm.ACMClient(conf['ENDPOINT'], conf['NAMESPACE'], conf['AK'], conf['SK'])
        elif conf.get("RAM_ROLE_NAME"):
            self.client = acm.ACMClient(conf['ENDPOINT'], conf['NAMESPACE'], conf['RAM_ROLE_NAME'])
            #self.client.set_options(kms_enabled=True, region_id=conf['REGION_ID'], key_id=conf['KEY_ID'])
            #self.client.set_options(kms_enabled=True, region_id=conf['REGION_ID'])
        else:
            raise Exception('access info or ram_role can not be null!')
        servers = self.client.get_server()
        #print(servers)

    def get(self,data_id,group):
        conf_set = self.client.get(data_id,group)
        if conf_set:
            return json.loads(conf_set)
        return None

    def add_watcher(self,data_id,group,cb):
        if 'Windows'== self.system:
            return
        return self.client.add_watcher(data_id,group,cb)




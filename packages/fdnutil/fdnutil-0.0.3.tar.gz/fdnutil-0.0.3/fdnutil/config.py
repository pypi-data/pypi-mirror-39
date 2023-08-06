import os, yaml
from pathlib import Path
from fdnutil.cypher import *
from fdnutil.log import *
import logging

from fdnutil.whoami import iam
logger = logging.getLogger(name=iam())

class Configurator:
    def __init__(self, KEY, cfg_dir='fd-config'):
        self.cfg_dir = '.{}'.format(cfg_dir)
        self.key = KEY

    def get_config_template(self):
        return {
            'db':{
                'driver': '',
                'host': '',
                'port': 5432,
                'db':'',
                'username':'',
                'password': ''
            },
            's3':{
                'use_awscli':True
            },
            'local':{
                'sync_s3': True,
                'purge_cache': True,
                'data_path': '.'
            }
        }

    def config_paths(self):
        home = str(Path.home())
        cfgpath = os.path.join(home, self.cfg_dir)
        cfgfile = os.path.join(cfgpath, 'config.yml')
        
        return cfgpath, cfgfile

    def init(self):
        setup_logging()

        try:
            self.config = self.read_config()
            self.dsn = self._get_dsn()
        except Exception as e:
            logger.exception("cannot read config")
    
    def get_instance(self):
        return self.config

    def write_config(self,config):
    
        cfgpath , cfgfile = self.config_paths()

        config['db']['password'] = encrypt( str.encode(config['db']['password']) , self.key)

        if not os.path.isdir(cfgpath):
            os.mkdir(cfgpath)

        with open(cfgfile,'w') as fd:
            yaml.dump(config, fd, default_flow_style=False)

        logger.info("writing config to : {}".format(cfgfile))
        self.init()

    def read_config(self):
        cfgpath, cfgfile = self.config_paths()
        
        if not os.path.isfile(cfgfile):
            raise Exception("config file not exists")

        config = None
        with open(cfgfile, 'r') as fd:
            config = yaml.load(fd)
            config['db']['password'] = decrypt(config['db']['password'], self.key).decode()
        
        return config

    def _get_dsn(self):
        config = self.config
        uname = config['db']['username']
        passwd = config['db']['password']
        host = config['db']['host']
        db = config['db']['db']
        driver = config['db']['driver']

        dsn = "{}://{}:{}@{}/{}".format(driver,uname, passwd, host, db)

        logger.debug("USING DSN : {}".format(dsn))

        return dsn
    
    def get_dsn(self):
        return self.dsn
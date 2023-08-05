import configparser
import logging
import os
import requests
from requests.packages import urllib3
from urllib.parse import quote
from xdg import XDG_CONFIG_HOME

logger = logging.getLogger(__name__)


class FreeClient:
    BASE_URL = 'https://smsapi.free-mobile.fr/sendmsg'
    
    def __init__(self, user=None, password=None):
        """Create a new Free Mobile SMS API client."""
        self._user = user
        self._password = password
        self._codes = {
            200: "Message send",
            400: "Missing parameter",
            402: "Too much messages send",
            403: "Service not enable",
            500: "Server not available",
        }

    def load_config_file(self, config_file):
        """Load a configuration file"""
        
        logger.debug("Looking for config file: {}". format(config_file))
        if not os.path.isfile(config_file):
            raise Exception("There is not configuration file at: {}".format(config_file))

        with open(config_file) as f:
            file_content = '[dummy]\n' + f.read()
            
        config = configparser.ConfigParser()
        config.read_string(file_content)
        
        cfg = config['dummy']
        self._user = cfg.get("user", None)
        self._password = cfg.get("password", None)
        
    def load_default_config_file(self):
        """Load default configuration file"""
        config_file = os.path.join(XDG_CONFIG_HOME, "send-sms-freemobile.conf")
        self.load_config_file(config_file)

    def send_sms(self, text, **kwargs):
        """Send a text with current user and password"""

        if not self._user or not self._password:
            raise AttributeError("User '{}' or password '{}' is null".format(self._user, self._password))

        params = {
            'user': self._user,
            'pass': self._password,
            'msg': text.encode('utf-8')
        }

        res = requests.get(FreeClient.BASE_URL, params=params, **kwargs)
        
        if not res.status_code in self._codes:
            return res.status_code, "Error message not found"
        else:
            return res.status_code, self._codes[res.status_code]

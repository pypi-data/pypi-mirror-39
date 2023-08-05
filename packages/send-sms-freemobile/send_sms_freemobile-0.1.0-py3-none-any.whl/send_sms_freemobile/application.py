import argparse
import logging
import sys
from .client import FreeClient

logger = logging.getLogger(__name__)

        
class Application:
    
    def run(self):
        parser = argparse.ArgumentParser(
            description="Yet another tool to send SMS through French provider FreeMobile"
        )
        parser.add_argument("message", help="Your message")
        args = parser.parse_args()
        
        if not sys.stdin.isatty():
            msg = sys.stdin.read()
        else:
            try:
                msg = args.message.decode(sys.stdin.encoding)
            except:
                msg = args.message
        
        client = FreeClient()
        client.load_default_config_file()
        status, value = client.send_sms(msg)
        
        if status != 200:
            print("SMS not sent: {}".format(value))
            sys.exit(1)
        

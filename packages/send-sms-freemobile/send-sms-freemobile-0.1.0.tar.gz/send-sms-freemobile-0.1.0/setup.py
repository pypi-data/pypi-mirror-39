# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['send_sms_freemobile']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.20,<3.0', 'xdg>=3.0,<4.0']

entry_points = \
{'console_scripts': ['send-sms = send_sms_freemobile:main']}

setup_kwargs = {
    'name': 'send-sms-freemobile',
    'version': '0.1.0',
    'description': 'Yet another tool to send SMS through French provider FreeMobile',
    'long_description': 'Yet another tool to send SMS through French provider FreeMobile!\n\n## How to use\n\nJust use the following command:\n\n    send-sms\n    \nIf the command is not on your PATH, it will be usually found on `$HOME/.local/bin`.\n\n## Configuration file\n\nConfiguration file can be found here:\n\n- Directory: XDG_CONFIG_HOME (default is `$HOME/.config`)\n- File: `send-sms-freemobile.conf`\n\nIt should look like:\n\n    user: free-user-here\n    password: free-password-here\n\n',
    'author': 'Aloha68',
    'author_email': 'dev@aloha.im',
    'url': 'https://gitlab.com/aloha68/send-sms-freemobile',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['lp_backup']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'cryptography>=2.4,<3.0',
 'fs-s3fs>=1.0,<2.0',
 'fs.webdavfs',
 'fs>=2.1,<3.0',
 'ruamel.yaml>=0.15.80,<0.16.0']

setup_kwargs = {
    'name': 'lp-backup',
    'version': '0.1.10',
    'description': 'Script to create local backups from Lastpass',
    'long_description': '# Lastpass Backup\n[![Build Status](https://travis-ci.org/rickh94/lp_backup.svg?branch=master)](https://travis-ci.org/rickh94/lp_backup)\n[![Documentation Status](https://readthedocs.org/projects/lastpass-local-backup/badge/?version=latest)](https://lastpass-local-backup.readthedocs.io/en/latest/?badge=latest)\n\nEasily backup data from lastpass to your own storage.\n\n## Installation\n\nYou first need to install the [lastpass commandline\ntool](https://github.com/lastpass/lastpass-cli) for your platform.\nIt is used internally for accessing the lastpass api.\n\n```bash\n$ pip install lp_backup\n```\n\nInstall [fs.webdavfs](https://github.com/damndam/webdavfs) for webdav support.\n\n## Usage\n\n```\nfrom lp_backup import Runner\n\n# create backup runner\nexample_backup_runner = Runner("/home/YOUR_USER/.config/lp_backup.yml")\n# run backup\nbackup_file_name = example_backup_runner.backup()\nprint(backup_file_name)\n\n# restore backup to /tmp/example-full-restore.csv (which is PLAIN TEXT, be sure to delete after use)\nbackup_file_name.restore(backup_file_name, "/tmp/test-full-restore.csv")\n\n```\n\n\n',
    'author': 'Rick Henry',
    'author_email': 'fredericmhenry@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

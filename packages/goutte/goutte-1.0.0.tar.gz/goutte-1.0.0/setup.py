# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['goutte']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'colorlog>=3.1,<4.0',
 'python-digitalocean>=1.14,<2.0',
 'toml>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['goutte = goutte.main:entrypoint']}

setup_kwargs = {
    'name': 'goutte',
    'version': '1.0.0',
    'description': 'DigitalOcean snapshot automation service',
    'long_description': '# goutte\nDigitalOcean doesn\'t propose any way of automating snapshots.\nThere are [some SaaS](https://snapshooter.io/) that can take care of it but paying to execute some API requests seemed a bit off.\n\nThat\'s why we developed a simple script which you can run with cron jobs or in CI services like Travis for free.\n\n## TODO\n- [x] Configuration from a single TOML file\n- [x] Droplets snapshots\n- [x] Droplets snapshots pruning\n- [x] Volume snapshots\n- [x] Volume snapshots pruning\n- [ ] Slack alerting\n- [ ] Add droplets and volumes by tag\n\n## Requirements\n- Python ^3.6\n- A DigitalOcean account\n\n## Installation\nInstall it directly from pip:\n```bash\npip3 install --user goutte\n```\n\n## Configuration file\nGoutte takes its configuration from a pretty straightforward toml file.\nWe provided and example in `goutte.example.toml`.\n\n```toml\nretention = 10     # Number of backups to keep per droplet/volume\n\n[droplets]\nnames = [          # Array of droplets you want to snapshot\n  \'server01\',\n  \'server02\',\n  \'server03\',\n]\n\n[volumes]\nnames = [          # Array of volumes you want to snapshot\n  \'db01\',\n  \'redis01\',\n  \'redis02\',\n]\n```\n\n## Usage\nGoutte takes two arguments which can also be set via environment variables:\n\n| # | Help     | Description                         | Environment variable |\n| - | -------- | ----------------------------------- | -------------------- |\n| 1 | CONFIG   | Path to the toml configuration file | `GOUTTE_CONFIG`      |\n| 2 | DO_TOKEN | Your DigitalOcean API token         | `GOUTTE_DO_TOKEN`    |\n\n```bash\nUsage: goutte [OPTIONS] CONFIG DO_TOKEN\n\n  DigitalOcean snapshots automation.\n\nOptions:\n  --only [snapshot|prune]  Only snapshot or only prune\n  --debug                  Enable debug logging\n  --version                Show the version and exit.\n  --help                   Show this message and exit.\n```\n\nRunning "snapshot only" for a configuration file containing one droplet and one volume:\n```bash\n$ goutte goutte.toml $do_token --only snapshot\n13:32:48 - INFO - Starting goutte v1.0.0\n13:32:52 - INFO - sgp1-website-01 - Snapshot (goutte-sgp1-website-01-20181220-56bde)\n13:32:59 - INFO - sgp1-mariadb-01 - Snapshot (goutte-sgp1-mariadb-01-20181220-3673d)\n```\n\n## Run with Docker\nWe have a Docker image ready for you to use on Docker Hub.\nIt will read by default the configuration under `/goutte/goutte.toml`\n\n```bash\ndocker run \\\n  -e GOUTTE_DO_TOKEN=${do_token} \\\n  -v $(pwd)/goutte.toml:/goutte/goutte.toml \\\n  tomochain:goutte\n```\n\n## Automating\nYou can easily automate it via cron job or by leveraging free CI tools like Travis.\nWe provided and example travis configuration in `travis.example.yml`.\n\nYou just need to set the environment variables on the Travis website and schedule it with the frequency of your backups.\n\nTODO\n',
    'author': 'etienne-napoleone',
    'author_email': 'etienne@tomochain.com',
    'url': 'https://github.com/tomochain/goutte',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)

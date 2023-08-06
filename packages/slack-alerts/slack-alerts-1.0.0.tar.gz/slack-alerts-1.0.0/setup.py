# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['slack_alerts']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.20,<3.0']

setup_kwargs = {
    'name': 'slack-alerts',
    'version': '1.0.0',
    'description': 'Simple Slack alerting python library',
    'long_description': "<h5 align='center'>SLACK-ALERTS</h5>\n<h6 align='center'>\n  SIMPLE SLACK ALERTING PYTHON LIBRARY<br/>\n  ────\n</h6>\n<div align='center'>\n  <a href='https://travis-ci.org/etienne-napoleone/slack-alerts'>\n    <img src='https://travis-ci.org/etienne-napoleone/slack-alerts.svg?branch=develop' alt='Build Status' />\n  </a>\n  <a href='https://coveralls.io/github/etienne-napoleone/slack-alerts?branch=develop'>\n    <img src='https://coveralls.io/repos/github/etienne-napoleone/slack-alerts/badge.svg?branch=develop' alt='Coverage Status' />\n  </a>\n</div>\n\n&nbsp;\n\n&nbsp;\n\n### Usage\n\n```\nimport slack_alerts\n\nalerter = slack_alerts.Alerter('https://your-slack.webhook/url')\nalerter.critical('something bad happened!!')\n```\n\n### Installation\n\nWith pip\n\n```bash\npip3 install --user slack_alerts\n```\n\nAs a dependency\n\n```bash\n# with poetry\npoetry add slack_alerts\n\n# with virtualenv\nvirtualenv -p python3 .env\nsource .env/bin/activate\npip install slack_alerts\n\n# with pipenv\npipenv install slack_alerts\n```\n\n### Tests\n\nRun pytest for unit tests\n\n```bash\n# you need a valid slack webhook url as there is no api mocking\nexport SLACK_WEBHOOK_URL='https://...'\n\npoetry run coverage run --source slack_alerts -m pytest -v\npoetry run coverage report\n```\n\nRun flake8 for code style\n\n```bash\npoetry run flake8 .\n```\n\n### Built With\n\n* [Poetry](https://github.com/sdispater/poetry) - Python dependency management made great\n* [Requests](https://github.com/requests/requests) - The famous and robust http client library\n\n<!--\n### Contributing\n\nPlease read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.\n\n### Versioning\n\nWe use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).\n\n### Authors\n\n* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)\n\nSee also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.\n\n### License\n\nThis project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details\n\n### Acknowledgments\n\n* Hat tip to anyone whose code was used\n* Inspiration\n* etc\n-->\n",
    'author': 'Etienne Napoleone',
    'author_email': 'etienne@tomochain.com',
    'url': 'https://github.com/etienne-napoleone/slack-alerts',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['tmobile_call_log']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.0,<4.0', 'numpy>=1.15,<2.0', 'pandas>=0.23.4,<0.24.0']

setup_kwargs = {
    'name': 'tmobile-call-log',
    'version': '0.1.0',
    'description': 'Creates plots from T-Mobile personal call logs.',
    'long_description': "# tmobile_call_log\nCreates bar charts and pie charts from call logs. Processes CSV files\ndownloaded directly from T-Mobile's website (customer interface). Works as of\n2017.\n\n# Installation\nTo install tmobile_call_log, use pip (or similar):\n```{.sourceCode .bash}\npip install tmobile-call-log\n```\n\n# Documentation\n\n## Create log object to compile all data\n\n* `data_dir` is the directory where all the call logs (downloaded csv files)\nare located.\n* `ignore_number` is any other number that is also yours and appears in the\nlog (e.g., Google voice number).\n\n```python\nlog = CallActivity(data_dir='./data/', ignore_number='(123) 555-1234')\n```\n\n## Plot bar charts\n\nPlots bar charts for call time and call quantity using the top `n`\nmost frequent phone numbers.\n```python\nlog.plot_bar(n=15)\n```\n\n\n## Plot pie charts\n\nPlots pie charts for call time and call quantity using the top `n`\nmost frequent phone numbers.\n```python\nlog.plot_pie(n=9)\n```\n",
    'author': 'Manny Ochoa',
    'author_email': 'dev@manuelochoa.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

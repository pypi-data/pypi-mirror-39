# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pyppeteer_pdf']

package_data = \
{'': ['*']}

install_requires = \
['Click>=7.0,<8.0', 'pyppeteer>=0.0.25,<0.0.26']

entry_points = \
{'console_scripts': ['pyppeteer-pdf = pyppeteer_pdf.cli:html2pdf_command']}

setup_kwargs = {
    'name': 'pyppeteer-pdf',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Tim Kamanin',
    'author_email': 'tim@timonweb.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

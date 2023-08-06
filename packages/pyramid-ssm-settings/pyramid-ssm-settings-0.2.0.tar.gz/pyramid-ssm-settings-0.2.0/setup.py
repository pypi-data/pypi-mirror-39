# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['pyramid_ssm_settings']
install_requires = \
['boto3>=1.9,<2.0']

setup_kwargs = {
    'name': 'pyramid-ssm-settings',
    'version': '0.2.0',
    'description': 'Pull settings into Pyramid from Amazon EC2 Parameter Store.',
    'long_description': '# pyramid-ssm-settings\n\nPull settings into Pyramid from Amazon EC2 Parameter Store.\n',
    'author': 'Theron Luhn',
    'author_email': 'theron@luhn.com',
    'url': 'https://github.com/luhn/pyramid-ssm-settings',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)

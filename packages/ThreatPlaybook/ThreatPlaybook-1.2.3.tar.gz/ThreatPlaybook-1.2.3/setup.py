from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ThreatPlaybook',
    version='1.2.3',
    packages=['threat_playbook'],
    entry_points={
        'console_scripts': [
            'threat-playbook = threat_playbook:main'
        ]
    },
    url='https://we45.gitbook.io/threatplaybook/',
    license='MIT License',
    author='we45',
    author_email='info@we45.com',
    install_requires=[
        'mongoengine==0.15.0',
        'pathlib==1.0.1',
        'PyYAML==3.12',
        'schema==0.6.8',
        'robotframework==3.0.4',
        'lxml==4.2.1',
        'docopt',
        'texttable',
        'huepy',
        'tinydb'
    ],
    description='Threat-Models-as Code, An Action-Oriented Threat Modeling and Automation Framework',
    long_description = long_description,
    long_description_content_type='text/markdown',
    include_package_data=True
)
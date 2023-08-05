from setuptools import setup

setup(
    name='snw',
    version='0.5.2',
    description='snw client tool',
    scripts = ['client/snw'],
    package_dir={'': 'nmt-wizard'},
    packages=['client'],
    install_requires=[
        'prettytable',
        'regex',
        'requests',
        'six'
    ]
)

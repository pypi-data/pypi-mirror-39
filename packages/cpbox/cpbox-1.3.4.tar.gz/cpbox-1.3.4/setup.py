from setuptools import setup, find_packages

setup(
    name = 'cpbox',
    version = '1.3.4',
    keywords = ('cpbox'),
    description = 'cp tool box',
    license = '',
    install_requires = [
        'six',
        'pyyaml',
        'Jinja2',
        'netaddr',
        'requests',
        'tzlocal',
        'docker',
        'redis'
        ],

    scripts = [],

    author = 'http://www.liaohuqiu.net',
    author_email = 'liaohuqiu@gmail.com',
    url = '',

    packages = find_packages(),
    platforms = 'any',
)

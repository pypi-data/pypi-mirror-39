# pylint: disable=C0103, C0111, C0326, W0122

from setuptools import setup

with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()


def get_version():
    version = {}
    with open("trackerjacker/version.py") as fp:
        exec(fp.read(), version)
    return version['__version__']


def get_readme():
    try:
        import pypandoc
        readme_data = pypandoc.convert('README.md', 'rst')
    except(IOError, ImportError):
        readme_data = open('README.md').read()
    return readme_data


setup(
    name = 'trackerjacker',
    packages = ['trackerjacker', 'trackerjacker/plugins'],
    url = 'https://github.com/calebmadrigal/trackerjacker',
    version = get_version(),
    description = 'Finds and tracks wifi devices through raw 802.11 monitoring',
    long_description = get_readme(),
    author = 'Caleb Madrigal',
    author_email = 'caleb.madrigal@gmail.com',
    license = 'MIT',
    keywords = ['hacking', 'network', 'wireless', 'packets', 'scapy'],
    install_requires = requirements,
    tests_require = requirements,
    test_suite='tests',
    entry_points={'console_scripts': ['trackerjacker = trackerjacker.__main__:main']},
    include_package_data = True,
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: System :: Networking',
        'Topic :: System :: Networking :: Monitoring',
        'Topic :: Security',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS'
    ],
)

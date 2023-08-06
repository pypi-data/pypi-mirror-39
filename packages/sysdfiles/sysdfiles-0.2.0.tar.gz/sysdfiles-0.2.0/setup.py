from setuptools import setup
from codecs import open

# get the long description from the README file
with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='sysdfiles',
    version='0.2.0',
    license='MIT',
    description='systemd configuration file access',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Shawn Baker',
    author_email='support@frozen.ca',
    url='https://github.com/ShawnBaker/sysdfiles',
    packages=['sysdfiles'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Operating System'
    ],
    project_urls={
        'Documentation': 'https://github.com/ShawnBaker/sysdfiles/wiki',
        'Source': 'https://github.com/ShawnBaker/sysdfiles',
    },
    keywords='systemd configuration file files automount conf device hostname hosts ini link machine-id machine-info mount network os-release path scope service slice socket swap target timer unit',
    test_suite = 'nose.collector'
)

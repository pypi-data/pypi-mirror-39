from setuptools import setup
from codecs import open

# get the long description from the README file
with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='sysdfiles',
    version='0.1.0',
    license='MIT',
    description='systemd configuration file access',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Shawn Baker',
    author_email='shawn@frozen.ca',
    url='https://github.com/ShawnBaker/sysdfiles',
    packages=['sysdfiles'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    project_urls={
        'Documentation': 'https://github.com/ShawnBaker/sysdfiles/wiki',
        'Source': 'https://github.com/ShawnBaker/sysdfiles',
    },
    keywords='systemd configuration file files automount conf device hosts ini link mount network path scope service slice socket swap target timer unit',
    test_suite = 'nose.collector'
)

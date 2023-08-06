# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='ctecLogstash',
    version='0.0.2',
    description=('A python logstash project modify package which add appname'),
    url='https://github.com/kep-w/ec-logstash',
    author='Kepner Wu',
    author_email='kepner_wu@hotmail.com',
    license='MIT',
    packages=find_packages(),
    platforms=['all'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='logstash python appname',
    install_requires = [
        'pika==0.12.0',
        'simplejson==3.16.0',
    ],
)
#!/usr/bin/env python
# Copyright (C) 2018 SignalFx, Inc. All rights reserved.
from setuptools import setup, find_packages


version = '0.0.0'

setup(name='signalfx-tracing',
      version=version,
      author='SignalFx, Inc.',
      author_email='info@signalfx.com',
      url='http://github.com/signalfx/signalfx-python-tracing',
      download_url='http://github.com/signalfx/signalfx-python-tracing/tarball/master',
      description='Provides auto-instrumentation for OpenTracing traced libraries and frameworks',
      license='Apache Software License v2',
      long_description='Provides auto-instrumentation for OpenTracing traced libraries and frameworks',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
      ],
      packages=find_packages(),
      install_requires=['opentracing>=2.0<2.1', 'wrapt'],
      extras_require={
          'tests': [
              'docker',
              'mock',
              'pytest',
              'six',
          ],
      },
      entry_points={
          'console_scripts': [
              'sfx-py-trace = scripts.sfx_py_trace:main'
          ]
      })

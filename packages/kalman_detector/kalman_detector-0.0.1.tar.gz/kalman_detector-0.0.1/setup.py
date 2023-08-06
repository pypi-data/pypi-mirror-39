#!/usr/bin/env python

from distutils.core import setup

setup(name='kalman_detector',
      version='0.0.1',
      description='Detect radio bursts with variying intensity',
      author='Barak Zackay',
      author_email='bzackay@gmail.com',
      url='https://bitbucket.org/bzackay/kalman_detector',
      packages=['kalman_detector'],
      requires=['numpy', 'scipy', 'numba', 'matplotlib'])

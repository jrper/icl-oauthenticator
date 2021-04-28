#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='Imperial OAuthenticator',
      version='1.0',
      description='Imperial compatible OAuth authenticator',
      author='James Percival',
      author_email='j.percival@imperial.ac.uk',
      packages=['iclauth'],
      entry_points={
    'jupyterhub.authenticators': [
        'icladd = iclauth:LocalICLOAuthenticator'
    ]
      }
)

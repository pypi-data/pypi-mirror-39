#!/usr/bin/env python

from distutils.core import setup

setup(name='ybc_player',
      version='1.0.1',
      description='Play audio file.',
      long_description='Play the audio file in current dictionary',
      author='lijz01',
      author_email='lijz01@fenbi.com',
      keywords=['python', 'play', 'audio'],
      url='http://pip.zhenguanyu.com/',
      packages=['ybc_player'],
      package_data={'ybc_player': ['html/*', 'test.wav', '__init__.py', 'ybc_player.py', 'ybc_player_unitest.py']},
      license='MIT',
      install_requires=['ybc_exception']
     )
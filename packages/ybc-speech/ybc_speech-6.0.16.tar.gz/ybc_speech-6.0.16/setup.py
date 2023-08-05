#!/usr/bin/env python

from distutils.core import setup

setup(name='ybc_speech',
      version='6.0.16',
      description='Speech operation api.',
      long_description='Speech Recognition,voice2text,text2voice',
      author='hurs',
      author_email='hurs@fenbi.com',
      keywords=['pip3', 'speech', 'python3', 'python', 'Speech Recognition'],
      url='http://pip.zhenguanyu.com/',
      packages=['ybc_speech'],
      package_data={'ybc_speech': ['*.wav', '__init__.py', 'ybc_speech.py', 'ybc_speech_unitest.py']},
      license='MIT',
      install_requires=['pyaudio', 'wave', 'requests', 'ybc_config', 'ybc_exception']
     )
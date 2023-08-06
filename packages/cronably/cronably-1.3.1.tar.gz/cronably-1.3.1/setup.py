from setuptools import setup

from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()


setup(
    name='cronably',
    version='1.3.1',
    description='Cronably allows you run python scripts with configured repetitions easily',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=['cronably',
              'cronably/actions',
              'cronably/actions/pre_action',
              'cronably/actions/post_action',
              'cronably/actions/main_action',
              'cronably/actions/repetition',
              'cronably/context',
              'cronably/model',
              'cronably/repositories',
              'cronably/utils'
              ],
    author='David Kotlirevsky',
    author_email='david.kotlirevsky@gmail.com',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
    ],
    keywords=['cronably', 'cron'],
    url='https://gitlab.com/Kotlirevsky/cronably'
)
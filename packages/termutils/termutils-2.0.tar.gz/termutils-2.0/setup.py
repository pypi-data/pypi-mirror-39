from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='termutils',
    version='2.0',
    packages=[''],
    url='https://github.com/tman540/termutils',
    license='MIT',
    author='Steve Tautonico',
    author_email='stautonico@gmail.com',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['requests']
)

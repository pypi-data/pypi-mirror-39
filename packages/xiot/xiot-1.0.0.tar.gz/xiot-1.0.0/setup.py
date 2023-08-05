from distutils.core import setup

import os

here = os.path.abspath(os.path.dirname(__file__))

setup(
    name='xiot',
    keywords=('xiot'),
    version='1.0.0',
    py_modules=['xiot'],
    url='https://github.com/sintrb/xiot',
    license='Apache License 2.0',
    author='Robin',
    author_email='sintrb@gmail.com',
    description='A lib for xiot.',
    requires=['requests'],
)

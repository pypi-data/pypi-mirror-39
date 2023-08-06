# -*- coding: utf-8 -*-
import os
from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'requirements.txt')) as f:
    requires = f.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='sqla_inspect',
    version='0.4.4',
    packages=['sqla_inspect'],
    include_package_data=True,
    license='GPLv3',
    description='Usefull tools for setting/getting datas from SQLAlchemy models',
    url='https://github.com/majerteam/sqla_inspect',
    author='Gaston Tjebbes - Majerti',
    author_email='tech@majerti.fr',
    install_requires=requires,
    extra_requires={'docs': ['sphinx'], 'test': ['pytest']},
    classifiers=[
        'Intended Audience :: Developers',
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 2.7',
        'Topic :: Database',
    ],
)

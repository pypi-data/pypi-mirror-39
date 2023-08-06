# -*- coding: utf-8 -*-
from collections import OrderedDict
from distutils.core import setup


setup(
    name='seo',
    version='0.0.2dev',
    project_urls=OrderedDict((
        ('Code', 'https://github.com/ceb10n/seo'),
    )),
    author='Rafael Marques',
    author_email='rafaelomarques@gmail.com',
    maintainer='Rafael Marques',
    maintainer_email='rafaelomarques@gmail.com',
    description='Simple collection of SEO utils.',
    packages=['seo'],
    license='MIT License',
    long_description=open('README.md').read(),
)

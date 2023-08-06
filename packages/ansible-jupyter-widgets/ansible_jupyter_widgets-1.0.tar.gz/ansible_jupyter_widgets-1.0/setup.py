#!/usr/bin/env python

from distutils.core import setup

setup(name='ansible_jupyter_widgets',
      version='1.0',
      description='Jupyter Widgets for Ansible Jupyter Kernel',
      author='Ben Thomasson',
      author_email='benthomasson@redhat.com',
      url='',
      packages=['ansible_jupyter_widgets'],
      install_requires = ['ipywidgets']
     )

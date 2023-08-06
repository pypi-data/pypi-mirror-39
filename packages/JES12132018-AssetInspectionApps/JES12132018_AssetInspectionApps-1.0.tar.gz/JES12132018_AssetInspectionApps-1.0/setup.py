# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 23:31:27 2018

@author: erics
"""

from setuptools import setup, find_packages 

setup(name='JES12132018_AssetInspectionApps', 
      version='1.0', 

description='JES12132018_AssetInspectionApps', 
      url='https://www.gwinnettcounty.com/web/gwinnett/departments/publicutilities', 
      author='eric swett', 
      author_email='eric.swett@gwinnettcounty.com', 
      license='BSD', 
      packages=find_packages(), 
      install_requires=['pyqt5'], 
      zip_safe=False) 
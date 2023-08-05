'''
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
'''

from setuptools import setup, find_packages
import sys

sys.path.append("./src")
import microserver


setup(name="microserver",
      version=microserver.__version__,
      description="MicroServer",
      author="Jesse Zhang",
      author_email="jesse.zhang8759@gmail.com",
      url="https://bitbucket.org/autestsuite/microserver",
      license="Apache License 2.0",
      entry_points={
          'console_scripts': ['microserver = microserver.__main__:main']
      },
      package_dir={'': 'src'},
      packages=find_packages('src'),
      install_requires=[
          "trlib",
      ],
      # see classifiers
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
      ],
      long_description=''
      )

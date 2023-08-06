#!/usr/bin/env python
try:
    from setuptools import setup
    args = {}
except ImportError:
    from distutils.core import setup
    print("""\
*** WARNING: setuptools is not found.  Using distutils...
""")
 
from setuptools import setup
try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

from os import path
setup(name='pycsoap',
      version='0.1.0',
      description='Generation of SOAP descriptors.',
      long_description= "" if not path.isfile("README.md") else read_md('README.md'),
      author='Andrew H Nguyen',
      author_email='andrewhuynguyen10@gmail.com',
      url='https://gitlab.com/andrewhuynguyen/pycsoap',
      #license='MIT',
      setup_requires=[],
      tests_require=['pytest'],
      install_requires=[
          "pyparsing",
          "argparse",
          "termcolor",
          "six",
          "numpy",
          "scipy"
      ],
      packages=['pycsoap'],
      scripts=[],
      #package_data={'src': []},
      #include_package_data=True,
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Science/Research',
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'Operating System :: MacOS',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Topic :: Scientific/Engineering',
      ],
	zip_safe=False
     )

#!/usr/bin/env python
from setuptools import setup, find_packages
name = "md_codegen"

requires = ['codegenhelper>=0.0.16', 'code-engine>=1.0.13', 'deep-mapper1>=0.0.1']

setup(
    name = name,
    version = '0.4.2',
    scripts = ["scripts/codegen"],
    author = 'Zongying Cao',
    author_email = 'zongying.cao@dxc.com',
    description = 'codegen is a library for generating the infrastructure code of microservices.',
    long_description = """codegen is a library for generating the infrastructure code of microservices.""",
    packages = [name],
    url = "https://github.com/cao5zy/codegen",
    package_dir = {'md_codegen': 'codegen'},
    package_data = {'md_codegen': ["*.py"]},
    include_package_data = True,
    install_requires = requires,
    license = 'Apache',
    classifiers = [
               'Development Status :: 4 - Beta',
               'Intended Audience :: Developers',
               'License :: OSI Approved :: Apache Software License',
               'Natural Language :: English',
               'Operating System :: OS Independent',
               'Programming Language :: Python :: 3',
               'Topic :: Software Development :: Libraries',
           ],
)

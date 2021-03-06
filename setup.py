"""`Dependency injector` setup script."""

import os
import re

from setuptools import setup, Extension


# Defining setup variables:
defined_macros = list()

# Getting description:
with open('README.rst') as readme_file:
    description = readme_file.read()

# Getting requirements:
with open('requirements.txt') as version:
    requirements = version.readlines()

# Getting version:
with open('src/dependency_injector/__init__.py') as init_file:
    version = re.search('VERSION = \'(.*?)\'', init_file.read()).group(1)

# Adding debug options:
if os.environ.get('DEPENDENCY_INJECTOR_DEBUG_MODE') == '1':
    defined_macros.append(('CYTHON_TRACE', 1))
    defined_macros.append(('CYTHON_TRACE_NOGIL', 1))


setup(name='dependency-injector',
      version=version,
      description='Dependency injection microframework for Python',
      long_description=description,
      author='ETS Labs',
      author_email='rmogilatov@gmail.com',
      maintainer='Roman Mogilatov',
      maintainer_email='rmogilatov@gmail.com',
      url='https://github.com/ets-labs/python-dependency-injector',
      download_url='https://pypi.python.org/pypi/dependency_injector',
      install_requires=requirements,
      packages=[
          'dependency_injector',
          'dependency_injector.containers',
          'dependency_injector.providers',
      ],
      package_dir={
          '': 'src',
      },
      ext_modules=[
          Extension('dependency_injector.providers.base',
                    ['src/dependency_injector/providers/base.c'],
                    define_macros=defined_macros,
                    extra_compile_args=['-O2']),
          Extension('dependency_injector.providers.callables',
                    ['src/dependency_injector/providers/callables.c'],
                    define_macros=defined_macros,
                    extra_compile_args=['-O2']),
          Extension('dependency_injector.providers.factories',
                    ['src/dependency_injector/providers/factories.c'],
                    define_macros=defined_macros,
                    extra_compile_args=['-O2']),
          Extension('dependency_injector.providers.singletons',
                    ['src/dependency_injector/providers/singletons.c'],
                    define_macros=defined_macros,
                    extra_compile_args=['-O2']),
          Extension('dependency_injector.providers.injections',
                    ['src/dependency_injector/providers/injections.c'],
                    define_macros=defined_macros,
                    extra_compile_args=['-O2']),
          Extension('dependency_injector.providers.utils',
                    ['src/dependency_injector/providers/utils.c'],
                    define_macros=defined_macros,
                    extra_compile_args=['-O2']),
      ],
      package_data={
          'dependency_injector': ['*.pxd'],
      },
      zip_safe=True,
      license='BSD New',
      platforms=['any'],
      keywords=[
          'Dependency injection',
          'DI',
          'Inversion of Control',
          'IoC',
      ],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
          'Topic :: Software Development',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ])

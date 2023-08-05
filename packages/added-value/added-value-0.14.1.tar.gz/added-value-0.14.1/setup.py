# -*- coding: utf-8 -*-
import os
import io

from setuptools import setup, find_packages

with open('README.rst', 'r') as readme:
    long_description = readme.read()


def local_file(*name):
    return os.path.join(
        os.path.dirname(__file__),
        *name)


def read(name, **kwargs):
    with io.open(
        name,
        encoding=kwargs.get("encoding", "utf8")
    ) as handle:
        return handle.read()


def read_version():
    "Read the `(version-string, version-info)` from `added_value/version.py`."
    version_file = local_file('source', 'added_value', 'version.py')
    local_vars = {}
    with open(version_file) as handle:
        exec(handle.read(), {}, local_vars)  # pylint: disable=exec-used
    return local_vars['__version__']

install_requires = [
    'docutils',
    'sphinx',
    'natsort',
    'six',
]


setup(
    name='added-value',
    packages=find_packages(where='source'),
    package_dir={'': 'source'},
    version = read_version(),
    url='https://github.com/sixty-north/added-value',
    download_url="https://pypi.python.org/pypi/added-value",
    license='BSD',
    author='Robert Smallshire',
    author_email='rob@sixty-north.com',
    description='Sphinx "added-value" extension',
    long_description=long_description,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        "Programming Language :: Python :: 3",
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    include_package_data=True,
    install_requires=install_requires,
    requires=install_requires,
    extras_require={
        'test': ['pytest', 'pytest-cov', 'coveralls', 'beautifulsoup4', 'hypothesis'],
        'docs': ['sphinx', 'sphinx_rtd_theme'],
        'deploy': ['bumpversion', 'twine', 'wheel'],
    },
    project_urls={
        "Source": "https://github.com/sixty-north/added-value",
        "Documentation": "https://added-value.readthedocs.io/en/latest/",
    }
)

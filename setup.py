# coding=utf-8

from setuptools import setup, find_packages
import multiprocessing # workaround for bug http://bugs.python.org/issue15881#msg170215


with open('README.rst') as f:
    readme = f.read()
with open('CHANGELOG.rst') as f:
    changelog = f.read()
with open('core-requirements.txt') as f:
    requirements = [line.strip() for line in f.readlines() if line[:1] != '#']


setup(
    name='devpi-cleaner',
    use_scm_version=True,
    description="""Enables batch removal of packages from a devpi server.""",
    long_description='{}\n\n{}'.format(readme, changelog),
    long_description_content_type='text/x-rst',
    author='Matthias Bach',
    author_email='matthias.bach@blue-yonder.com',
    url='https://github.com/blue-yonder/devpi-cleaner',
    license='new BSD',
    packages=find_packages(exclude=['tests']),
    install_requires=requirements,
    setup_requires=[
        'setuptools_scm',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: System :: Archiving :: Packaging',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Utilities',
    ],
    entry_points={
        'console_scripts': [
            'devpi-cleaner = devpi_cleaner.cli:main',
        ]
    },
)

# coding=utf-8

from setuptools import setup, find_packages
import multiprocessing # workaround for bug http://bugs.python.org/issue15881#msg170215


with open('README.rst') as f:
    readme = f.read()
with open('CHANGELOG.rst') as f:
    changelog = f.read()


setup(
    name='devpi-cleaner',
    use_scm_version=True,
    description="""Enables batch removal of packages from a devpi server.""",
    long_description='{}\n\n{}'.format(readme, changelog),
    author='Matthias Bach',
    author_email='matthias.bach@blue-yonder.com',
    url='https://github.com/blue-yonder/devpi-cleaner',
    license='new BSD',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'devpi-plumber>=0.2.5',
        'six',
    ],
    setup_requires=[
        'nose',
        'setuptools_scm',
    ],
    tests_require=[
        'coverage',
        'mock',
    ],
    test_suite='nose.collector',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: System :: Archiving :: Packaging',
        'Topic :: Utilities',
    ],
    entry_points={
        'console_scripts': [
            'devpi-cleaner = devpi_cleaner.cli:main',
        ]
    },
)

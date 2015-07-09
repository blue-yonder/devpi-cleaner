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
    description="""A utility to clean packages from a devpi server.""",
    long_description='{}\n\n{}'.format(readme, changelog),
    author='Blue Yonder Technology Foundation Team',
    url='http://jira.phi-tps.local',
    author_email='Blue-Yonder.TeamTechnologie@blue-yonder.com',
    packages=find_packages(exclude='tests'),
    install_requires=[
        'devpi-plumber',
    ],
    setup_requires=[
        'nose',
        'nose-progressive',
        'setuptools_scm',
    ],
    tests_require=[
        'coverage',
        'mock',
    ],
    test_suite='nose.collector',
    entry_points={
        'console_scripts': [
            'devpi-cleaner = devpi_cleaner.cli:main',
        ]
    },
)

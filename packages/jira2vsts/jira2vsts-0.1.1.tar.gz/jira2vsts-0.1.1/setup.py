import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

version = '0.1.1'

setup(
    name='jira2vsts',
    version=version,
    description="Synchronize Jira issues to VSTS (Azure Devops)",
    long_description=README,
    classifiers=[
    ],
    keywords='jira2vsts',
    author='Mohamed Cherkaoui',
    author_email='chermed@gmail.com',
    license='LGPL v3',
    py_modules=['jira2vsts'],
    include_package_data=True,
    install_requires=[
        'click',
        'vsts',
        'python-dateutil',
        'pyyaml',
        'jira',
        'validictory',
    ],
    entry_points='''
        [console_scripts]
        jira2vsts=jira2vsts:main
    ''',
)

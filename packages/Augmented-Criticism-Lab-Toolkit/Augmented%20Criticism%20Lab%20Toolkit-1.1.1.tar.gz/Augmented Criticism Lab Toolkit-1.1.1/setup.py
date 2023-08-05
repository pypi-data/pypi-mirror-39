from setuptools import setup

setup(
    name='Augmented Criticism Lab Toolkit',
    version='1.1.1',
    packages=['admin_tools', 'tools', 'connectors'],
    url='https://git.joshharkema.com/jharkema/augemented-criticism-lab-tools',
    license='https://creativecommons.org/licenses/by/2.0/ca/',
    author='Josh Harkema',
    author_email='josh@joshharkema.com',
    description='A set of tools for connecting to the Augmented Criticism Lab',
    install_requires=['requests', 'cmudict', 'pronouncing', 'oauth2_client'],
    classifiers=['Programming Language :: Python :: 3']
)

from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='Augmented Criticism Lab Toolkit',
    version='1.1.7',
    packages=['admin_tools', 'tools', 'connectors'],
    url='https://git.joshharkema.com/jharkema/augemented-criticism-lab-tools',
    license='https://creativecommons.org/licenses/by/2.0/ca/',
    author='Josh Harkema',
    author_email='josh@joshharkema.com',
    description='A set of tools for connecting to the Augmented Criticism Lab',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['requests', 'cmudict', 'pronouncing'],
    classifiers=['Programming Language :: Python :: 3'],
    include_package_data=True,
    package_data={'tools': ['*.csv', '*.txt']}
)

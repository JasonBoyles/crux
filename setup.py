from setuptools import setup

import crux

DEPENDENCYLINKS = []
REQUIRES = ['requests']

setup(
    name='crux',
    description='A client for various Adobe Experience Manager (AEM) APIs',
    keywords='AEM automation API',
    version=crux.__version__,
    author='Rackspace',
    author_email='devopsprodeng@lists.rackspace.com',
    dependency_links=DEPENDENCYLINKS,
    install_requires=REQUIRES,
    package_dir={'crux': 'crux'},
    packages=['crux'],
    include_package_data=True,
    license='Apache License (2.0)',
    classifiers=["Programming Language :: Python"],
    url='http://github.com/racker/crux'
)

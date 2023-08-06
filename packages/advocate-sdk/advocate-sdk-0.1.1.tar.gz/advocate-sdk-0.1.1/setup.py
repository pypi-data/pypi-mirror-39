import os
from setuptools import setup, find_packages

from adv import __version__

readme = os.path.join(os.path.dirname(__file__), 'README.md')

setup(
    name='advocate-sdk',
    version=__version__,
    url='https://github.com/AdvocatesInc/advocate-python-sdk',
    author='Advocates, Inc',
    author_email='admin@adv.gg',
    description='SDK for developing interactive widgets and more on the Advocate platform',
    long_description=open(readme).read(),
    long_description_content_type="text/markdown",
    license='Proprietary and confidential',
    zip_safe=False,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests>=2.9.1',
    ],
)

import os
from setuptools import setup, find_packages

__version__ = '0.0.1'

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-aristotle-pdf-downloads',
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='Aristotle PDF Downloads!',
    long_description='Aristotle PDF Downloads!',
    url='https://github.com/aristotle-mdr/aristotle-pdf-downloads',
    author='Samuel Spencer',
    author_email='sam@aristotlemetadata.com',
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: Closed Source',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        # 'aristotle-metadata-registry>=1.5.6',
        'weasyprint',
    ],
)

from distutils.core import setup
import setuptools

version = '1.0.29'

packages = ['metagenomi']

scripts = ['metagenomi/helpers.py', 'metagenomi/metadata.py', 'metagenomi/dynamo.py']

classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 3']

requirements = ['boto3', 'pandas']

setup(
    name='metagenomi',
    author='Metagenomi.co',
    author_email='info@metagenomi.co',
    version=version,
    packages=packages,
    license='MIT',
    long_description=open('README.md').read(),
    install_requires=requirements,
    classifiers=classifiers,
    url='http://metagenomi.co'
)

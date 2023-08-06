#from distutils.core import setup
import setuptools

setuptools.setup(
    name='stadistic_basic',
    version='0.1.1dev',
    packages=['stadistic_basic',],
    license='MIT',
    long_description=open('README.txt').read(),
    author='Kenyi Simons',
    author_email='kenyilpz@gmail.com',
    url = 'https://github.com/nathramk/stadistic_basic', # use the URL to the github repo
    download_url = 'https://github.com/nathramk/stadistic_basic/tarball/0.1',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
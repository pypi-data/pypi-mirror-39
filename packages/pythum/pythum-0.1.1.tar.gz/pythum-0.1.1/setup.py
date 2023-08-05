# from distutils.core import setup
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = 'pythum',
    packages = ['pythum'],
    # packages=setuptools.find_packages(),
    author = 'metadeta96',
    author_email = 'metadeta96@gmail.com',
    version = 'v0.1.1',  # Ideally should be same as your GitHub release tag varsion
    description = 'Simple minimalist quantum computing simalation for python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url = 'https://github.com/metadeta96/pythum',
    download_url = 'https://github.com/metadeta96/pythum',
    keywords = ['quantum', 'python', 'pythum', 'computing', 'simulator', 'simulation'],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
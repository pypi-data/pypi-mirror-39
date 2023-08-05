from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="count_api",
    version="3.1.8",
    author="Count Technologies LTD",
    author_email="hello@count.co",
    description="API client for count.co",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://count.co",
    packages=find_packages(),
    install_requires=[
      'requests',
      'protobuf==3.5.1',
      'future',
      'pyhamcrest',
      'six'
    ],
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="message-broker-interface",
    version="0.1",
    packages=find_packages(),
    description="Provides the basic glue for some message broker based projects",
    url="https://github.com/ihgalis/message_broker_interface",
    author="Andre Fritsche",
    author_email="github@andresilaghi.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    license="MIT",
    install_requires=[
        'argparse',
        'pika',
        'pymongo'
    ],
)

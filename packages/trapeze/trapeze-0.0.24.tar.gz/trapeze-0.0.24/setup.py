import setuptools

with open("README.md", "r") as fh :
    long_description = fh.read()

setuptools.setup(
    name = "trapeze",
    version="0.0.24",
    author="Eric Gee",
    author_email="eric@gee.farm",
    description="Store/restore configuration and credentials for applications with AWS S3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/ericgee/trapeze",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = ['boto3','click'],
    entry_points = {
        'console_scripts': [
            'trapeze=trapeze.app:main'
        ]
    }
)

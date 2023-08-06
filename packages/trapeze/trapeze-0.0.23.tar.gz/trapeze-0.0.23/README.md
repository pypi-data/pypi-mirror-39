# Trapeze

**Store/restore configuration and credentials for applications with AWS S3.**  Quickly pull and push sensitive configuration files on both development and production environments.  The goal is to provide a very quick, secure method of restoring applications without storing credentials on GIT.

## Requirements
- Python 3.6+

## Installation
run ```pip install trapeze```.

## Instructions
1. **Initialize.** Goto application folder and run ```trapeze init```. Completing this process will create a *.trapeze* configuration file.
2. **Push/Pull** You can then either **push** ```trapeze push``` or **pull** ```trapeze pull``` to send/restore config/credential files from S3.

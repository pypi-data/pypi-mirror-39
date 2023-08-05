# ElasticBeanstalk to Env

This tool simply does one thing, connects to an Elastic Beanstalk environment, pulls out any custom envrionment variables that are configured and will display them on stdout, or if given a file for output, will write a file containing the values. This is useful when a project requires a different server not running inside Elastic Beanstalk (one that should not recieve web requests, for example) but still requires the same environment configuration. Trying to keep these envrionments in sync manually does not scale, so this tool can be used as a cronjob to write out a new .env file if the configurations do not match.

## Installation

`pip install elasticbeanstalk-to-env`

## Usage

Run the eb-to-env command, the `--application` and `--environment` options are required. `--output` requires a filename in the current working directory, if none is specified, the envrionment variables from EB will be printed to stdout.

`eb-to-env --application <appname> --environment <envname> --output .env`
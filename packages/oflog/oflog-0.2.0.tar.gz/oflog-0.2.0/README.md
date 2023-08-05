# OpenFin Log Management CLI

## Overview

The OpenFin Log Management CLI allows users to interact with the Log Management service via the command line. Apps that have log management enabled will have their logs encrypted and uploaded to the log management service after the RVM closes. This CLI can be used to list logs stored by app names and/or desktops, and to download and decrypt those log files so that the app provider can read and use them for debugging purposes.

### Assumptions

The following are requirements for using the CLI tool:
* Python 2.7 must be installed.
* Run `pip install oflog` to install the CLI tool.

### Features

- List application names, and list desktop id's for a given app name.
- List logs for a given application.
- Download and decrypt zipped files from the log management service.

## Getting started

### File Structure

- openfin_log_cli.py: cli tool entry point.
- config.ini: file that contains default configuration information, including log manager url, api key, and private key file.

### Configuration
Run `oflog --configure` and answer the prompts for base-url, api-key, and private-key to configure the cli. Configuration is stored in `~/.openfin/config.ini`

### Usage

All commands return JSON responses from the log management service.
All commands require at least the base url and the api key to be configured either in config.ini or the arguments `--base-url` or `--api-key`. For downloading logs, an RSA private key file in PEM form must also be configured in either config.ini or the argument `--private-key`.
If the aforementioned configuration items are provided both in the config.ini file and as a command line argument, the command line argument will take precedence.

### Commands
* `oflog --get-app-names`: list all the application names.
* `oflog --get-app-desktops --app-name <name>`: list all the desktops for a given app name.
* `oflog --get-desktop-logs --app-name <name> --desktop-id <id>`: list all the logs for a given app name / desktop combination.
* `oflog --get-logs --app-name <name>`: get all the logs for a given app name.
* `oflog --download-log <log-id>`: download a log with the given id and decrypt it with the provided private key file.


### Other arguments

- `--start-date`: causes `--get-logs` and `--get-desktop-logs` to only show logs past that start date.
- `--end-date`: causes `--get-logs` and `--get-desktop-logs` to only show logs before that end date. Can be used in conjunction with `--start-date`.
- `--private-key`: location of RSA private key in PEM form, used to decrypt logs. This flag overrides the private key set in config.ini.
- `--base-url`: base url for api calls. This flag overrides the url set in config.ini.
- `--api-key`: api key for api calls. This flag overrides the api key set in config.ini.
- `--version`: shows the version of the CLI tool.
- `--help`: shows descriptions of commands and arguments.

## Contributing

This is an open source project and all are encouraged to contribute.

### Development
You can test any changes that you make locally by substituting `oflog` by running the `openfin_log_cli.py` file (e.g. calling the CLI like so: `python log_manager_cli\openfin_log_cli.py <args>`).

## License

This project uses the [Apache2 license](https://www.apache.org/licenses/LICENSE-2.0).
By downloading OpenFin, you agree to the terms of our [Developer License](https://openfin.co/developer-agreement/).

## Support

Please enter an issue in the repo for any questions or problems. Alternatively, please contact us at support@openfin.co

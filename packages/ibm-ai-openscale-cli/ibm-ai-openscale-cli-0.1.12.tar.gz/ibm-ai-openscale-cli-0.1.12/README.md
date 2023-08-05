# ibm-ai-openscale-cli
![Status](https://img.shields.io/badge/status-beta-yellow.svg)
[![Latest Stable Version](https://img.shields.io/pypi/v/ibm-ai-openscale-cli.svg)](https://pypi.python.org/pypi/ibm-ai-openscale-cli)

This tool allows user to get started real quick by exploring the environment to understand what user has, and then provision corresponding services needed to run AI OpenScale, then setup the models and setup monitoring conditions.

## Before you begin
* ☁️ You need an [IBM Cloud][ibm_cloud] account.
* 🔑 Create an [IBM Cloud API key](https://console.bluemix.net/docs/iam/userid_keys.html#userapikey)
* ⚠️ If you already have a Watson Machine Learning (WML) instance, ensure it's RC-enabled, learn more about this in the [migration instructions](https://console.bluemix.net/docs/resources/instance_migration.html#migrate).

## Installation

To install, use `pip` or `easy_install`:

```bash
pip install -U ibm-ai-openscale-cli
```

or

```bash
easy_install -U ibm-ai-openscale-cli
```

️️
## Usage

```
ibm-ai-openscale-cli --help
```
```
usage: ibm-ai-openscale-cli [-h] -a APIKEY [--env {ypprod,ypqa,ys1dev,icp}]
                            [--resource-group RESOURCE_GROUP]
                            [--organization ORGANIZATION] [--space SPACE]
                            [--postgres POSTGRES] [--wml WML]
                            [--username USERNAME] [--password PASSWORD]
                            [--url URL] [--datamart-name DATAMART_NAME]
                            [--history HISTORY] [--bx] [--verbose] [--version]

optional arguments:
  -h, --help            show this help message and exit
  --env {ypprod,ypqa,ys1dev,icp}
                        Environment. Default "ypprod"
  --resource-group RESOURCE_GROUP
                        Resource Group to use. If not specified, then
                        "default" group is used
  --organization ORGANIZATION
                        Cloud Foundry Organization to use
  --space SPACE         Cloud Foundry Space to use
  --postgres POSTGRES   Path to postgres credentials file. If not specified,
                        then the internal AIOS database is used
  --wml WML             Path to WML credentials file
  --username USERNAME   ICP username. Required if "icp" environment is chosen
  --password PASSWORD   ICP username. Required if "icp" environment is chosen
  --url URL             ICP url. Required if "icp" environment is chosen
  --datamart-name DATAMART_NAME
                        Specify data mart name, default is "aiosfastpath"
  --history HISTORY     Days of history to preload. Default is 7
  --bx                  Specify (without a value) to use IBM Cloud CLI (bx
                        CLI), default uses Rest API
  --verbose             verbose flag
  --version             show program's version number and exit

required arguments:
  -a APIKEY, --apikey APIKEY
                        IBM Cloud APIKey
```

## Example

```sh
export APIKEY=<PLATFORM_API_KEY>
ibm-ai-openscale-cli --apikey $APIKEY
```

## Python version

✅ Tested on Python 3.4, 3.5, and 3.6.

## Contributing

See [CONTRIBUTING.md][CONTRIBUTING].

## License

This library is licensed under the [Apache 2.0 license][license].

[ibm_cloud]: https://cloud.ibm.com
[responses]: https://github.com/getsentry/responses
[requests]: http://docs.python-requests.org/en/latest/
[CONTRIBUTING]: ./CONTRIBUTING.md
[license]: http://www.apache.org/licenses/LICENSE-2.0

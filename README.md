# Digital Marketplace API Clients

![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)


This project contains a script for using the API and Search API clients in a IPython shell

## Setup

You will need to install python which can be done using [pyenv](https://github.com/pyenv/pyenv)

You will also need to install `digitalmarketplace-developer-tools` which can be done with:
```
pip install digitalmarketplace-developer-tools
```

To install the dependencies run:
```
invoke requirements-dev
```

## API Client script

To use the scripts you will need the API and/or Search API tokens.
Speak to a developer who will be able to share these with you.

To run the API client script, first you need to enter the  virtual environment with:
```
source venv/bin/activate
```

You can then run the script with:
```
./scripts/api-clients-shell.py development --api-token=theToken
```

This will open a read only client shell with the API client which would look something like this:
```
development ro
In [1]:
```

You can then use the API client to make calls to the API, for example:
```
In [1]: data.get_framework('g-cloud-14')
Out[1]: 
{
  'frameworks': {
    'id': 17,
    'framework': 'g-cloud',
    'name': 'G-Cloud 14',
    'slug': 'g-cloud-14',
    'status': 'live'
  }
}
```

To see information about a method, you can add a '?' to the end of the method, for example:
```
In [1]: data.get_framework?
Signature: data.get_framework(slug)
Docstring: <no docstring>
File:      /dmapiclient/data.py
Type:      method
```

To get the client in the read-write mode pass in `-rw` or `--read-write`:
```
./scripts/api-clients-shell.py development --api-token=theToken -rw
```

To get the Search API client pass in the the search api token (`--search-api-token`):
```
./scripts/api-clients-shell.py development --api-token=theToken --search-api-token=theToken
```

To list all the possible API client methods and their documentation, you can run the `api-clients-shell-list.py` script:
```
./scripts/api-clients-shell-list.py data
./scripts/api-clients-shell-list.py search
```

## Updating Python dependencies

`requirements.txt` file is generated from the `requirements.in` in order to pin
versions of all nested dependencies. If `requirements.in` has been changed (or
we want to update the unpinned nested dependencies) `requirements.txt` should be
regenerated with

```
invoke freeze-requirements
```

`requirements.txt` should be committed alongside `requirements.in` changes.

## Pre-commit hooks

This project has a [pre-commit hook][pre-commit hook] to do some general file checks and check the `pyproject.toml`.
Follow the [Quick start][pre-commit quick start] to see how to set this up in your local checkout of this project.

## Licence

Unless stated otherwise, the codebase is released under [the MIT License][mit].
This covers both the codebase and any sample code in the documentation.

The documentation is [&copy; Crown copyright][copyright] and available under the terms
of the [Open Government 3.0][ogl] licence

[mit]: LICENCE
[copyright]: http://www.nationalarchives.gov.uk/information-management/re-using-public-sector-information/uk-government-licensing-framework/crown-copyright/
[ogl]: http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/

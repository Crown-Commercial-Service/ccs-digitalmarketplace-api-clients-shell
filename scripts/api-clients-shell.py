#!/usr/bin/env python3
"""
Drops you into an IPython shell with the DataAPIClient and SearchAPIClient instantiated and targetting the specified
stage as `data` and `search` respectively.

Usage:
  api-clients-shell.py [<stage>]

Optional:
  --api-url           Override the implicit API URL
  --api-token         API key (needed if wanting to use the API)
  --search-api-url    Override the implicit SearchAPI URL
  --search-api-token  SearchAPI key (needed if wanting to use the Search API)
  --cdp-api-url       Override the implicit Central Digtial Platform API URL
  --cdp-api-token     Override for the Central Digtial Platform API key
  -rw --read-write    Access to API calls that write data as well as read

Example:
  ./scripts/api-clients-shell.py
  ./scripts/api-clients-shell.py development --api-token=theToken
  ./scripts/api-clients-shell.py preview --api-token=theToken
  ./scripts/api-clients-shell.py staging --api-token=theToken
"""

import argparse
import sys

import IPython
from IPython.terminal.prompts import Prompts, Token
from traitlets.config import Config

from dmapiclient import DataAPIClient, SearchAPIClient, CentralDigitalPlatformAPIClient

sys.path.insert(0, '.')
from dmscripts.helpers.updated_by_helpers import get_user
from dmutils.env_helpers import get_api_endpoint_from_stage, get_cdp_api_endpoint_from_stage


def DMEnvironmentPrompt(stage: str, read_write: bool = False):
    """IPython prompt which shows the stage the API client is connected to"""
    _prompt = [
        (Token.Generic.Error if stage == "production" else Token.Generic, stage),
        (Token, " "),
        (Token.Generic.Strong, "rw") if read_write else (Token.Generic.Emph, "ro"),
    ]

    class DMPrompts(Prompts):
        def in_prompt_tokens(self):
            return _prompt + [(Token, "\n")] + super().in_prompt_tokens()

    return DMPrompts


def _is_read_only(item):
    return item.startswith("get") or item.startswith("find")


class ReadOnlyDataAPIClient:
    def __init__(self, data_client):
        self._data = data_client

    def __getattr__(self, item: str):
        attr = getattr(self._data, item)

        if _is_read_only(item):
            return attr
        else:
            raise AttributeError(f"'{item}' is not a read-only attribute of '{self.__class__.__name__}'")

    def __dir__(self):
        return filter(_is_read_only, dir(self._data))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('stage', default='local', help='The stage your clients should target', nargs='?',
                        choices=[
                            'local', 'development', 'preview', 'pre-production',
                        ])

    parser.add_argument(
        '--api-url',
        help='Override the implicit API URL',
        type=str
    )
    parser.add_argument(
        '--api-token',
        help='API key (needed if wanting to use the API)',
        type=str
    )

    parser.add_argument(
        '--search-api-url',
        help='Override the implicit SearchAPI URL',
        type=str
    )
    parser.add_argument(
        '--search-api-token',
        help='SearchAPI key (needed if wanting to use the Search API)',
        type=str
    )

    parser.add_argument(
        '--cdp-api-url',
        help='Override the implicit Central Digtial Platform API URL',
        type=str
    )
    parser.add_argument(
        '--cdp-api-token',
        help='Override for the Central Digtial Platform API key (don\'t decrypt from dm-credentials)',
        type=str
    )

    parser.add_argument('--read-write', '-rw',
                        help='Access to API calls that write data as well as read', action='store_true')

    args = parser.parse_args()

    stage = args.stage.lower()

    user = get_user()
    print(f"Setting user to '{user}'...")

    print('Setting API tokens...')
    api_token = 'myToken' if stage.lower() == 'local' else args.api_token
    search_api_token = 'myToken' if stage.lower() == 'local' else args.search_api_token
    cdp_api_token = args.cdp_api_token

    if not api_token and not search_api_token and not cdp_api_token:
        print("Must supply one of --api-token, --search-api-token or --cdp-api-token to access the client")
        sys.exit(1)

    print('Creating clients...')

    user_ns = {}

    if api_token:
        print('Creating Data API client...')
        data = DataAPIClient(
            base_url=args.api_url or get_api_endpoint_from_stage(stage),
            auth_token=api_token,
            user=user,
        )

        if not args.read_write:
            data = ReadOnlyDataAPIClient(data)

        user_ns["data"] = data

        print('Use \'data\' for Data API client')

    if search_api_token:
        print('Creating Search API client...')
        search = SearchAPIClient(
            base_url=args.search_api_url or get_api_endpoint_from_stage(stage, app='search-api'),
            auth_token=search_api_token,
            user=user,
        )

        user_ns["search"] = search

        print('Use \'search\' for Search API client')

    if cdp_api_token:
        print('Creating Central Digital Platform API client...')
        cdp = CentralDigitalPlatformAPIClient(
            base_url=args.cdp_api_url or get_cdp_api_endpoint_from_stage(stage),
            api_key=cdp_api_token,
        )

        user_ns["cdp"] = cdp

        print('Use \'cdp\' for Central Digital Platform API client')

    ipython_config = Config()
    ipython_config.TerminalInteractiveShell.prompts_class = DMEnvironmentPrompt(stage, args.read_write)

    print('Dropping into shell...')
    IPython.start_ipython(argv=[], config=ipython_config, user_ns=user_ns)

#!/usr/bin/env python3
"""
Lists the methods of the API Clients thay you can use

Usage:
  api-clients-shell-list.py [<client>]

Example:
  ./scripts/api-clients-shell.py
  ./scripts/api-clients-shell.py data
  ./scripts/api-clients-shell.py search
  ./scripts/api-clients-shell.py cdp
"""

import argparse
import sys
import pydoc


from dmapiclient import DataAPIClient, SearchAPIClient, CentralDigitalPlatformAPIClient

sys.path.insert(0, '.')


def get_method_names(client_class):
    return [
        method_name
        for method_name in dir(client_class)
        if not method_name.startswith('_') and callable(getattr(client_class, method_name))
    ]


def list_methods(client_class):
    documentation = []

    for method_name in get_method_names(client_class):
        method_documentation = []
        for line in pydoc.render_doc(getattr(client_class, method_name)).split('\n'):
            if line:
                method_documentation.append(line)

        documentation.append('\n'.join(method_documentation))

    seperator_line = '-' * 50

    for doc in documentation:
        print(seperator_line)
        print(doc)
        print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('client', default='data', help='The client you want to check the methods for', nargs='?',
                        choices=[
                            'data', 'search', 'cdp',
                        ])

    args = parser.parse_args()

    client = args.client.lower()

    if client == 'data':
        print('Listing DataAPIClient methods...')
        list_methods(DataAPIClient)

    if client == 'search':
        print('Listing SearchAPIClient methods...')
        list_methods(SearchAPIClient)

    if client == 'cdp':
        print('Listing CentralDigitalPlatformAPIClient methods...')
        list_methods(CentralDigitalPlatformAPIClient)

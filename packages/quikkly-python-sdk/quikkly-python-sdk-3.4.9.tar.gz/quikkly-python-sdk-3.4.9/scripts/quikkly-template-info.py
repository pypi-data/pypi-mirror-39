#!/usr/bin/env python
"""Command-line script for generating Quikkly codes."""
from __future__ import absolute_import, print_function

import argparse
import json
import logging
import sys

import os.path

log = logging.getLogger(__name__)

# Fix Python path if scripts are run without pip-installing the quikklysdk package.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from quikklysdk import quikkly


def main():
    parser = argparse.ArgumentParser(description='Generate Quikkly codes in SVG, PNG and other formats.')
    parser.add_argument('--native-libs-dir', help='Path to quikklycore native libraries. You can also use the QUIKKLY_NATIVE_DIR environment variable.')
    parser.add_argument('--blueprint-file', help='Path to quikklycore blueprint file. Defaults to --native-libs-dir/blueprint_default.json.')
    parser.add_argument('--type', help='Template ID to print info for. If omitted, prints all of them.')
    args = parser.parse_args()

    run_info(args)


def run_info(args):
    if args.native_libs_dir:
        quikkly.init(args.native_libs_dir, args.blueprint_file)

    infos = quikkly.get_template_info()
    if args.type:
        for info in infos:
            if args.type == info['identifier']:
                print(json.dumps(info, indent=2))
                return
        print(json.dumps({'error': 'Template %s not found.' % args.type}, indent=2))
        sys.exit(1)
    else:
        print(json.dumps(infos, indent=2))


if __name__ == '__main__':
    main()

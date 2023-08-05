#!/usr/bin/env python3
#
# Copyright 2017-2018 Government of Canada
# Public Services and Procurement Canada - buyandsell.gc.ca
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


import asyncio
import argparse
import json
import os
import sys
import time

import aiohttp

DEFAULT_AGENT_URL = os.environ.get('AGENT_URL', 'http://localhost:5000')

parser = argparse.ArgumentParser(
    description='Issue one or more credentials via von-x')
parser.add_argument('conn_id', help='the connection ID')
parser.add_argument('paths', nargs='+',
    help='the path to a credential JSON file')
parser.add_argument('-c', '--count', type=int, default=1,
    help='repeatedly issue claims this many times (for volume testing)')
parser.add_argument('-p', '--parallel', action='store_true',
    help='submit the credentials in parallel')
parser.add_argument('-u', '--url', default=DEFAULT_AGENT_URL,
    help='the URL of the von-x service')

args = parser.parse_args()

AGENT_URL = args.url
CONN_ID = args.conn_id
CRED_PATHS = args.paths
PARALLEL = args.parallel
REPEAT = args.count

async def issue_cred(http_client, conn_id, cred_path, ident):
    with open(cred_path) as cred_file:
        cred = json.load(cred_file)
    if not cred:
        raise ValueError('Credential could not be parsed')
    schema = cred.get('schema')
    if not schema:
        raise ValueError('No schema defined')
    version = cred.get('version', '')
    attrs = cred.get('attributes')
    if not attrs:
        raise ValueError('No schema attributes defined')

    print('Submitting credential {} {}'.format(ident, cred_path))

    start = time.time()
    try:
        response = await http_client.post(
            '{}/issue-credential'.format(AGENT_URL),
            params={'schema': schema, 'version': version, 'connection_id': conn_id},
            json=attrs
        )
        if response.status != 200:
            raise RuntimeError(
                'Credential could not be processed: {}'.format(await response.text())
            )
        result_json = await response.json()
    except Exception as exc:
        raise Exception(
            'Could not issue credential. '
            'Are von-x and TheOrgBook running?') from exc

    elapsed = time.time() - start
    print('Response to {} from von-x ({:.2f}s):\n\n{}\n'.format(ident, elapsed, result_json))

async def submit_all(conn_id, cred_paths, parallel=False, repeat=1):
    start = time.time()
    async with aiohttp.ClientSession() as http_client:
        all = []
        idx = 1
        for cred_path in cred_paths:
            for ridx in range(args.count):
                req = issue_cred(http_client, conn_id, cred_path, idx)
                if parallel:
                    all.append(req)
                else:
                    await req
                idx += 1
        if all:
            await asyncio.gather(*all)
    elapsed = time.time() - start
    print('Total time: {:.2f}s'.format(elapsed))

asyncio.get_event_loop().run_until_complete(submit_all(CONN_ID, CRED_PATHS, PARALLEL, REPEAT))

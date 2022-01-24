import http.client
import json
import os
import re
import urllib.parse
import shlex
import sys

from optparse import OptionParser

parser = OptionParser('usage: %prog [options] curl [curl_arguments]')
parser.description = 'Obtain a schema from a GraphQL endpoint.'
parser.add_option("-f", "--schema-file", dest="schema_file", default="schema.graphql", type="str",
                  help="schema file to write to or augment")

try:
    curl_index = sys.argv.index('curl')
    args = sys.argv[1:curl_index]
except ValueError as e:
    parser.error(f'Expected curl statement.')
    exit(1)
    
(main_options, remaining_args) = parser.parse_args(args=args)
if len(remaining_args) > 0:
    parser.error(f'Unexpected argument(s): {shlex.join(remaining_args)}')
    exit(1)

parser = OptionParser()
parser.add_option('-H', '--header', dest="headers", type="str", action="append")
parser.add_option('--compressed', dest="compressed", action="store_true")
parser.add_option('--data-raw', dest="data_raw")
parser.add_option('-X', '--method', dest="method", type="str", default="GET")

(curl_options, remaining_args) = parser.parse_args(args=sys.argv[curl_index+1:])

if len(remaining_args) != 1:
    parser.error(f'Expected exactly one URL. Found {len(remaining_args)}: {shlex.join(remaining_args)}')
    exit(1)

url = remaining_args[0]

if curl_options.data_raw is not None:
    curl_options.method = 'POST'

headers = {}

if curl_options.headers is not None:
    headers = {
        re.match(r'^([^:]+): .*$', header).group(1):re.match(r'^[^:]+: (.*)$', header).group(1)
        for header in (curl_options.headers)
    }



body = curl_options.data_raw
body = re.sub(r'^\$"(.*)"$', '\1', body)
# print(body)
request = json.loads(body)
# print(json.dumps(request, indent=2))
# print(request['query'])

from client import Client

client = Client(method=curl_options.method, url=url, headers=headers)

# with open('introspection_query.graphql', 'r') as f:
#     INTROSPECTION_QUERY = f.read()

if os.path.isfile(main_options.schema_file):
    with open(main_options.schema_file, 'r') as f:
        schema = f.read()
else:
    schema = client.introspect()
    
    with open(main_options.schema_file, 'w') as f:
        f.write(schema)


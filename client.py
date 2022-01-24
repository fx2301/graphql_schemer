import http.client
import json
import urllib.parse

from graphql import build_client_schema
from graphql import get_introspection_query
from graphql import print_schema

class Client:
    def __init__(self, method, url, headers):
        assert 'Content-Type' in headers and headers['Content-Type'] == 'application/json'
        assert method == 'POST'
        assert urllib.parse.urlparse(url).scheme in ['http', 'https']

        self.method = method
        self.url = url
        self.headers = headers

    def query(self, body):
        url_parse = urllib.parse.urlparse(self.url)

        if url_parse.scheme == 'https':
            conn = http.client.HTTPSConnection(url_parse.netloc)
        else:
            conn = http.client.HTTPConnection(url_parse.netloc)

        conn.request(method='POST', url=self.url, body=body, headers=self.headers)

        response = conn.getresponse()
        result_raw = response.read()
        assert response.status == 200, f'Expected 200 status. Got: {response.status}'

        result = json.loads(result_raw)
        # print(json.dumps(result, indent=2))
        
        return result

    def introspect(self):
        introspection_query = get_introspection_query(descriptions=True)
        introspection_query_result = self.query(body=json.dumps({'query': introspection_query}))
        client_schema = build_client_schema(introspection_query_result['data'])
        schema = print_schema(client_schema)

        return schema
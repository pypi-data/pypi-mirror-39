import requests
import re

class BaseClient:

    def call_api(self, method, params):
        body = {

            "method": method,
            "params": params
        }

        response = requests.post('http://localhost:2080/jsonrpc', timeout=5, json=body)

        if response.status_code != 200:
            raise Exception("Received {} calling {}".format(response.status_code, method))

        result = response.json()

        return result['result'], result.get('error', None)

    def ensure_valid_tag(self, name, value, prefix):
        if not value.startswith("{}_".format(prefix)):
            raise Exception("{} must begin with prefix {}_ found: {}".format(name, prefix, value))

        if not re.match("^[A-Z0-9\_]+$", value):
            raise Exception("{} must be upper case/alpha or underscore only".format(name))

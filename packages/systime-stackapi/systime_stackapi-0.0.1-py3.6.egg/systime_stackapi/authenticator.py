import requests
from collections import OrderedDict
import time
import hmac
import json
import hashlib
import binascii

class Authenticator(object):
    def __init__(self, client_key_id, shared_secret, **kwargs):
        self.client_key_id = client_key_id
        self.shared_secret = shared_secret
        self.requested_token_lifetime = kwargs.get('requested_token_lifetime', 1800)
        self.auth_endpoint = kwargs.get('auth_endpoint', 'https://auth.api.systime.dk/auth')
        self.algorithm = kwargs.get('algorithm', 'sha3_512')

    def getServiceBearerToken(self, service_key_id):
        json_payload = self.buildPayload(service_key_id)
        raw_token = self.authenticate(json_payload)
        formatted_token = 'Bearer %s' % (raw_token)
        return formatted_token

    def buildPayload(self, service_key_id):
        d = OrderedDict()
        d['clientKeyId'] = self.client_key_id
        d['serviceKeyId'] = service_key_id
        d['time'] = int(time.time())
        d['expiry'] = self.requested_token_lifetime

        hmac_components = ''
        for value in d.values():
            hmac_components += str(value)

        signature = hmac.new(self.shared_secret.encode('utf-8'), hmac_components.encode('utf-8'), self.algorithm)
        hex_signature = signature.hexdigest()
        d['signature'] = hex_signature

        return json.dumps(d)

    def authenticate(self, json_payload):
        r = requests.post(self.auth_endpoint, data=json_payload, headers={'Content-Type': 'application/json'})

        if r.status_code == 200:
            jsonToken = json.loads(r.text)
            token = jsonToken['JWTToken']
            return token
        else:
            raise Exception('Authentication failed')


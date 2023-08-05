from . import authenticator
import requests

class StackService(authenticator.Authenticator):
    def __init__(self, service_url, client_key_id, shared_secret, **kwargs):
        self.service_url = service_url
        self.service_token = 'StackService'
        super().__init__(client_key_id, shared_secret, **kwargs)

    def installationsList(self):
        path = '/installation-management/installations'

        bearer_token = self.getServiceBearerToken(self.service_token);
        r = requests.get(self.service_url + path, headers={'Content-Type': 'application/json', 'Authorization': bearer_token})
        return(r.text)

import requests
from annotationframeworkclient import endpoints

class ServiceClient(object):
    def __init__(self, server_address=None, dataset_name=None):
        if server_address is None:
            self._server_address = endpoints.default_server_address
        else:
            self._server_address = server_address

        self._dataset_name = dataset_name
        self.session = requests.Session()

        self._default_url_mapping = {"server_address": self._server_address}

    @property
    def dataset_name(self):
        return self._dataset_name

    @property
    def server_address(self):
        return self._server_address

    @server_address.setter
    def server_address(self, value):
        self._server_address = value
        self._default_url_mapping['server_address'] = value

    @property
    def default_url_mapping(self):
        return self._default_url_mapping.copy()
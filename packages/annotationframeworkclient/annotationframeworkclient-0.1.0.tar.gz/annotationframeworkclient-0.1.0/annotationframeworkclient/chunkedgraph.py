import requests
import os
import numpy as np
import cloudvolume
import json
import time

from annotationframeworkclient.endpoints import chunkedgraph_endpoints as cg
from annotationframeworkclient import endpoints
from annotationframeworkclient import infoservice

class PychunkedGraphClient(object):
    def __init__(self, server_address):
        if server_address is None:
            self._server_address = endpoints.default_server_address
        else:
            self._server_address = server_address
        self.session = requests.Session()
        self.infoserviceclient = None

        self._default_url_mapping = {'cg_server_address': self._cg_server_address}
 
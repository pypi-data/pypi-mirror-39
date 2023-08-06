from annotationframeworkclient.endpoints import materializationservice_endpoints as mzn
from annotationframeworkclient.base import ServiceClient

class MaterializationClient(ServiceClient):
    def __init__(self, server_address=None, dataset_name=None):
        super(MaterializationClient, self).__init__(server_address=server_address,
                                                    dataset_name=dataset_name)

    def get_materialization_versions(self, dataset_name=None):
        if dataset_name is None:
            dataset_name = self._dataset_name

        endpoint_mapping = self.default_url_mapping
        endpoint_mapping['dataset_name'] = dataset_name
        url = mzn['get_dataset_versions'].format_map(endpoint_mapping)
        response = self.session.get(url)
        assert(response.status_code==200)
        return response.json()
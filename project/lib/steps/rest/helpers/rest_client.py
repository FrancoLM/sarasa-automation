import requests

REQUESTS_METHODS = {
    "GET":      requests.get,
    "POST":     requests.post,
    "PUT":      requests.put,
    "PATCH":    requests.patch,
    "DELETE":   requests.delete,
}

class RESTClient(object):
    def __init__(self, base_urn, port, protocol="https"):
        self._base_urn = base_urn
        self._port = port
        self._protocol = protocol

        self.base_url = "%s://%s:%s" % (self._protocol, self._base_urn, self._port)
        self._api_endpoint = None
        self._auth = None
        self._username = self._password = None

    def set_api_endpoint(self, endpoint):
        """Set the endpoint for the API"""
        self._api_endpoint = "%s/%s" % (self.base_url, endpoint)

    def get_api_endpoint(self):
        return self._api_endpoint

    def set_auth_basic(self, username, password):
        self._auth = requests.auth.HTTPBasicAuth(username, password)
        self._username = username
        self._password = password

    def send_request(self, method, id=None, data=None, params=None, headers=None, json_content=None, files=None):
        url = self._api_endpoint
        if id:
            url += '/' + id
        if not headers:
            headers = {}

        check_ssl_certs = False
        requests.packages.urllib3.disable_warnings()
        response = REQUESTS_METHODS[method](url, data=data, params=params, headers=headers, json=json_content,
                                            verify=check_ssl_certs, auth=self._auth, files=files)
        return response


if __name__ == "__main__":
    """Small test to test if it works. To delete int he future"""
    my_client = RESTClient("jsonplaceholder.typicode.com", 443)
    my_client.set_api_endpoint("posts")
    response = my_client.send_request("GET")
    print(response)
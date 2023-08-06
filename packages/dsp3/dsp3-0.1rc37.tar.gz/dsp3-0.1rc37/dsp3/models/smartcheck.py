import sys
import datetime
import urllib3
import json
import requests
from typing import List


class SmartCheck:

    def __init__(self, username: str, password: str, host: str, port: int = '443', verify_ssl: bool = False,
                 ca_cert_file: str = None, proxy = None):
        """

        :param username:
        :param password:
        :param host:
        :param port:
        :param verify_ssl:
        :param ca_cert_file:
        :param proxy:
        """

        self.headers = {'Content-Type': 'application/json'}
        self._username = username
        self._password = password
        self.host = host
        self.port = port
        self.verify_ssl = verify_ssl
        self.ca_cert_file = ca_cert_file
        self.token = None
        self.token_expires = None
        self.password_change_require = False
        self.proxy = proxy
        urllib3.disable_warnings()

        try:
            self.session_id = self.__authenticate()
        except Exception as ex:
            print("Authentication error: ", ex)
            sys.exit()

    def __authenticate(self) -> str:

        credentials = json.dumps(dict(user=dict(userID=self._username, password=self._password)))
        url = "https://{}:{}/api/sessions".format(self.host, self.port)
        r = requests.post(url, data=credentials, verify=self.verify_ssl, headers=self.headers, proxies=self.proxy)
        r_json = json.loads(r.content.decode('utf-8'))
        self.token = r_json['token'] if r_json else None
        self.token_expires = datetime.datetime.strptime(r_json['expires'], '%Y-%m-%dT%H:%M:%SZ') if self.token else None
        self.password_change_require = r_json['user']['passwordChangeRequired']
        self.headers['Authorization'] = "Bearer %s" % self.token
        return r.content.decode('utf-8')

    def get_sessions(self):
        """
        Retrieve a list of sessions.

        :return: json object with sessions
        """

        url = "https://{}:{}/api/sessions".format(self.host, self.port)
        self.headers['Authorization'] = "Bearer %s" % self.token
        r = requests.get(url, verify=self.verify_ssl, headers=self.headers, proxies=self.proxy)

        return json.loads(r.content.decode('utf-8'))

    def get_users(self):
        """
        Retrieve a list of users.

        :return: json object with users
        """

        url = "https://{}:{}/api/users".format(self.host, self.port)
        self.headers['Authorization'] = "Bearer %s" % self.token
        r = requests.get(url, verify=self.verify_ssl, headers=self.headers, proxies=self.proxy)
        return json.loads(r.content.decode('utf-8'))

    def get_scans(self, id=None, registry=None, repository=None, tag=None, exact=False):
        """
        Retrieve a list of scans.

        repository: (Optional) When present, the tag query parameter will filter the list of scans to those scans where the source.repository
                    contains the provided value. If the exact query parameter is also provided (and true), the filter will do
                    an exact match on the value.
        exact: (Optional) When present (and true), any filtering done using the registry, repository, and tag query parameters will
               be done using exact matches.

        :return: json object with scans
        """

        if id is None:
            url = "https://{}:{}/api/scans".format(self.host, self.port)
        else:
            url = "https://{}:{}/api/scans/{}".format(self.host, self.port, id)

        self.headers['Authorization'] = "Bearer %s" % self.token
        if repository:
            self.headers['registry'] = registry
            self.headers['repository'] = repository
            self.headers['tag'] = tag
            self.headers['exact'] = str(exact).lower()

        r = requests.get(url, verify=self.verify_ssl, headers=self.headers, proxies=self.proxy)
        return json.loads(r.content.decode('utf-8'))

    def get_scan_malware_findings(self, scan_id, layer_id):

        url = "https://{}:{}/api/scans/{}/layers/{}/malware".format(self.host, self.port, scan_id, layer_id)
        self.headers['Authorization'] = "Bearer %s" % self.token
        params = dict(id=scan_id, layerID=layer_id)
        r = requests.get(url, params=params, verify=self.verify_ssl, headers=self.headers, proxies=self.proxy)
        return json.loads(r.content.decode('utf-8'))

    def get_scan_layer_vulnerability_findings(self, scan_id, layer_id):

        url = "https://{}:{}/api/scans/{}/layers/{}/vulnerabilities".format(self.host, self.port, scan_id, layer_id)
        self.headers['Authorization'] = "Bearer %s" % self.token
        params = dict(id=scan_id, layerID=layer_id)
        r = requests.get(url, params=params, verify=self.verify_ssl, headers=self.headers, proxies=self.proxy)
        return json.loads(r.content.decode('utf-8'))

    def initiate_scan(self, registry, repository, tag, username=None, password=None, token=None, type="docker"):

        url = "https://{}:{}/api/scans".format(self.host, self.port)
        credentials = dict(username=username, password=password, token=token)
        self.headers['Authorization'] = "Bearer %s" % self.token
        request = dict(source=dict(type=type, registry=registry, repository=repository, tag=tag, credentials=credentials,
                                   insecureSkipVerify=self.verify_ssl))
        r = requests.post(url, data=json.dumps(request), verify=self.verify_ssl, headers=self.headers, proxies=self.proxy)
        return json.loads(r.content.decode('utf-8'))

    def initiate_scan_ecr(self, registry, repository, tag, region, access_key, secret_access_key, token=None, type="docker"):
        """
        Initiate a new scan

        :param registry:
        :param repository:
        :param tag:
        :param region:
        :param access_key:
        :param secret_access_key:
        :param token: Use this if your source requires requests to be authorized using a bearer token.
                      Requests will include an Authorization: Bearer {token} header
        :param type: docker
        :return:

        """

        url = "https://{}:{}/api/scans".format(self.host, self.port)
        credentials = dict(aws=dict(region=region, accessKeyId=access_key, secretAccessKey=secret_access_key), token=token)
        self.headers['Authorization'] = "Bearer %s" % self.token
        request = dict(source=dict(type=type, registry=registry, repository=repository, tag=tag, credentials=credentials,insecureSkipVerify=self.verify_ssl))
        r = requests.post(url, data=json.dumps(request), verify=self.verify_ssl, headers=self.headers, proxies=self.proxy)
        return json.loads(r.content.decode('utf-8'))

    def get_registries(self):
        url = "https://{}:{}/api/registries".format(self.host, self.port)
        r = requests.get(url, verify=self.verify_ssl, headers=self.headers, proxies=self.proxy)
        return json.loads(r.content.decode('utf-8'))

    def get_vulnerabilities(self, id, layer_id):
        """
        Get scan vulnerability findings.

        :param id: scan id
        :param layer_id: scan layer id
        :return: python dict containing vulnerability findings.

        """
        url = "https://{}:{}/api/scans/{}/layers/{}/vulnerabilities".format(self.host, self.port, id, layer_id)
        r = requests.get(url, verify=self.verify_ssl, headers=self.headers, proxies=self.proxy)

        return json.loads(r.content.decode('utf-8'))

    def add_registry(self, name: str = None, description: str = None, host: str = None, username: str = None,
                     password: str = None, include: List[str] = None, exclude: List[str] = None, schedule: bool = False):
        """
        Do not use this call at this time. Not working.

        :param name:
        :param description:
        :param host:
        :param username:
        :param password:
        :param include:
        :param exclude:
        :param schedule:
        :return:
        """

        url = "https://{}:{}/api/registries".format(self.host, self.port)
        credentials = dict(username=username, password=password)
        sc_filter = dict(include=include, exclude=exclude)
        request = dict(name=name, description=description, host=host, credentials=credentials, insecureSkipVerify=False,
                       filter=sc_filter, schedule=schedule)
        r = requests.post(url, data=json.dumps(request), verify=self.verify_ssl, headers=self.headers, proxies=self.proxy)

        return json.loads(r.content.decode('utf-8'))



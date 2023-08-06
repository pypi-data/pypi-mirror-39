import base64
import datetime
import hashlib
import hmac
import json
import uuid

import querystring
from urllib3.util import parse_url

__all__ = ['append_alibaba_headers',
           'keep_configuration_in_RESTClientObject',
           'AppendAlibabaHeaders']

"""
Append Alibaba authentication headers based on original full HTTP request.

This Python implementation is modified from
https://github.com/aliyun/api-gateway-nodejs-sdk

---------------------------

Example Swagger Client usage:

class TestAlicloudApigateway(unittest.TestCase):
    store = 'samarkand.youzan.foreveryoung'

    @classmethod
    def setUpClass(cls):
        configuration = nomad_envoy_cli.Configuration()
        configuration.host = os.environ["ALICLOUD_APIGATEWAY_HOST"] + "/envoy"
        configuration.api_key = {
            "x-ca-key": os.environ["ALICLOUD_APIGATEWAY_APP_KEY"],
            "x-ca-stage": os.environ["ALICLOUD_STAGE"],
        }
        configuration.ALICLOUD_APIGATEWAY_APP_SECRET = os.environ[
            "ALICLOUD_APIGATEWAY_APP_SECRET"]

        cls.order_api = OrderApi(ApiClient(configuration))
        cls.product_api = ProductApi(ApiClient(configuration))

    def test_order(self):
        result = self.order_api.get_order_by_field(
            self.store, _request_timeout=60 * 1000)

        self.assertEqual(result.code, 200)
        rsp = json.loads(result.connector_response.response)['response']
        self.assertTrue(rsp['total_results'] > 0,
                        "we at least have one order.")
"""


def append_alibaba_headers(func):
    """
    A Python decorator to modify the request made by Swagger Client.

    The original method is RESTClientObject.request:

        def request(self, method, url, query_params=None, headers=None,
                body=None, post_params=None, _preload_content=True,
                _request_timeout=None):
            pass
    """

    def wrapper(*args, **kw):
        # 1. Re-organize parameters
        self = args[0]
        method = args[1]
        url = args[2]
        query_params = kw.get('query_params', {})
        headers = kw.get('headers', {})
        body = kw.get('body', {}) or {}

        # 2. Translating original Node.js code into below Python code.
        aah = AppendAlibabaHeaders(self.configuration, method, url,
                                   query_params, headers, body)
        headers = aah.result()

        # 3 .Write things back to args and kw if we changed anything.
        if 'content-type' in headers:
            headers['Content-Type'] = headers['content-type']
            del headers['content-type']
        kw["headers"] = headers

        return func(*args, **kw)

    return wrapper


def keep_configuration_in_RESTClientObject(func):
    """
    We need to access "configuration" inside of @append_alibaba_headers.
    """

    def wrapper(*args, **kw):
        self = args[0]
        configuration = args[1]
        self.configuration = configuration
        func(*args, **kw)

    return wrapper


class AppendAlibabaHeaders(object):
    sign_headers = {}
    content_type_form = 'application/x-www-form-urlencoded'

    def __init__(self,
                 configuration,  # SwaggerClient.Configuration
                 method: str,
                 url: str,
                 query_params: dict,
                 headers: dict,
                 body: dict):
        self.configuration = configuration
        self.method = method
        self.url = url
        self.query_params = query_params
        self.headers = headers
        self.body = body

        self.original_data_dict = {}
        self.original_data_dict.update(self.query_params)
        self.original_data_dict.update(self.body)

        self.x_ca_timestamp = int(datetime.datetime.now().timestamp() * 1000)
        self.x_ca_nonce = str(uuid.uuid4())

    def initial_headers(self):
        lower_key_headers = {k.lower(): self.headers[k] for k in
                             self.headers.keys()}

        d = {
            'x-ca-timestamp': self.x_ca_timestamp,
            'x-ca-key': self.configuration.api_key.get("x-ca-key", ""),
            'x-ca-nonce': self.x_ca_nonce,
            'x-ca-stage': self.configuration.api_key.get("x-ca-stage", "test"),
            'accept': 'application/json'
        }
        d.update(lower_key_headers)
        d.update(self.sign_headers)
        return d

    def get_sign_header_keys(self, headers: dict, sign_headers: dict) -> list:
        sign_keys = [h for h in headers
                     if h.startswith("x-ca-") or h in sign_headers]
        return list(sorted(sign_keys))

    def get_signed_headers_string(self, sign_headers: list, headers: dict) -> \
            str:
        return "\n".join([h + ":" + str(headers[h]) for h in sign_headers])

    def build_string_to_sign(self, method, headers, signed_headers_str, url,
                             data) -> str:  # noqa: E501
        lf = "\n"

        # TODO Node.js version var contentType = headers['content-type'] || '';
        content_type = headers.get('content-type', 'application/json')

        buffer = [
            method,
            headers.get('accept', ""),
            headers.get('content-md5', ""),
            content_type,
            headers.get('date', None),
        ]

        if signed_headers_str:
            buffer.append(signed_headers_str)

        buffer.append(self.build_url(url, content_type, data))

        return lf.join([v or "" for v in buffer])

    def build_url(self, url, content_type, data=None) -> str:
        if not content_type.startswith(self.content_type_form):
            return url

        query = []
        data = data or {}
        for k in sorted(data.keys()):
            if data[k]:
                query.append(k + "=" + data[k])
            else:
                query.append(k)
        query_str = "&".join(query)
        return url + "?" + query_str if query_str else url

    def sign(self, string_to_sign) -> str:
        assert hasattr(self.configuration, "ALICLOUD_APIGATEWAY_APP_SECRET"), \
            "Please assgin ALICLOUD_APIGATEWAY_APP_SECRET to " + \
            "configuration before use this Alibaba Swagger Client."

        m = hmac.new(self.configuration.ALICLOUD_APIGATEWAY_APP_SECRET.encode(
            "utf-8"),
            digestmod=hashlib.sha256)
        m.update(string_to_sign.encode('utf-8'))
        return base64.b64encode(m.digest()).decode('utf-8')

    @property
    def request_content_type(self):
        return self.headers.get("content-type", "")

    @property
    def is_content_type_form(self):
        return self.request_content_type.startswith(self.content_type_form)

    @property
    def content_md5(self):
        if self.is_content_type_form:
            original_data = querystring.stringify_obj(self.original_data_dict)
        else:
            # TODO could we avoid another duplicate json.dumps in rest#request
            original_data = json.dumps(self.body)
        return md5(original_data)

    def result(self) -> dict:
        auth_headers = self.initial_headers()

        if (self.method == "POST") and (not self.is_content_type_form):
            # this md5 works, verified by changing this string a bit.
            auth_headers["content-md5"] = self.content_md5

        sign_header_keys = self.get_sign_header_keys(auth_headers,
                                                     self.sign_headers)
        auth_headers['x-ca-signature-headers'] = ','.join(sign_header_keys)
        signed_headers_str = self.get_signed_headers_string(sign_header_keys,
                                                            auth_headers)

        stringToSign = self.build_string_to_sign(self.method,
                                                 auth_headers,
                                                 signed_headers_str,
                                                 parse_url(self.url).path,
                                                 self.original_data_dict)

        auth_headers['x-ca-signature'] = self.sign(stringToSign)

        return auth_headers


def md5(content: str) -> str:
    m = hashlib.md5()
    m.update(content.encode('utf-8'))
    return base64.b64encode(m.digest()).decode("utf-8")

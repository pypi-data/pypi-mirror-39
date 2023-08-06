from datetime import datetime
import urllib.parse
import hmac
import hashlib
import base64


class AmazonRequestBuilder(object):
    request_protocol = 'https'
    api_host = 'webservices.amazon.com'
    api_uri = '/onca/xml'

    def __init__(self, access_key, secret_key, associate_tag):
        self.access_key = access_key
        self.secret_key = secret_key
        self.associate_tag = associate_tag

    @property
    def current_timestamp(self):
        return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z')

    def build_request_url(self, params, override_timestamp=None, override_protocol=None):
        # Reference - https://docs.aws.amazon.com/AWSECommerceService/latest/DG/rest-signature.html
        params['Timestamp'] = override_timestamp or self.current_timestamp
        request_querystring = self._build_querystring(params)
        req_url = '{}://{}{}?{}'.format(override_protocol or self.request_protocol, self.api_host, self.api_uri, request_querystring)
        return req_url

    def _build_querystring(self, params):
        req_qs = self._encode_querystring(params)
        req_qs = self._sort_querystring(req_qs)
        req_qs = self._add_request_signature(req_qs)
        return req_qs

    def _sort_querystring(self, querystring):
        split_qs = querystring.split('&')
        split_qs.sort()
        qs = '&'.join(split_qs)
        return qs

    def _encode_querystring(self, params):
        request_querystring = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
        return request_querystring

    def _add_request_signature(self, querystring):
        string_to_sign = 'GET\n{}\n{}\n{}'.format(self.api_host, self.api_uri, querystring)
        signature = self._hash_signature(string_to_sign)
        encoded_signature = ''.join(
            [urllib.parse.quote(char) if char in ('+', '=') else char for char in signature])
        querystring_with_signature = '{}&Signature={}'.format(querystring, encoded_signature)
        return querystring_with_signature

    def _hash_signature(self, string):
        binary_key = bytes(self.secret_key, encoding='utf-8')
        hash = hmac.new(binary_key, string.encode('utf-8'), digestmod=hashlib.sha256)
        digest = hash.digest()
        encoded_digest = base64.b64encode(digest).decode()
        return encoded_digest
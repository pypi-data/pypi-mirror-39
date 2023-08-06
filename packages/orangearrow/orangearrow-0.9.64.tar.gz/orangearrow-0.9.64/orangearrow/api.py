import requests

from .builder import AmazonRequestBuilder
from .response import (
    AmazonItemSearchResponse,
    AmazonItemLookupResponse,
    AmazonSimilarityLookupResponse,
)


class AmazonProductAPI(object):
    def __init__(self, access_key, secret_key, associate_tag):
        self.access_key = access_key
        self.secret_key = secret_key
        self.associate_tag = associate_tag
        self.request_builder = AmazonRequestBuilder(access_key, secret_key, associate_tag)

    def _base_params(self, search_index=None, response_groups=None, parameters=None):
        if parameters is None:
            parameters = {}
        default_params = {
            'Service': 'AWSECommerceService',
            'AWSAccessKeyId': self.access_key,
            'AssociateTag': self.associate_tag,
            'ResponseGroup': 'Images,ItemAttributes',
            'Version': '2013-08-01'
        }
        if response_groups:
            default_params['ResponseGroup'] = ','.join(response_groups)
        if search_index:
            default_params['SearchIndex'] = search_index
        parameters.update(default_params)
        return parameters

    def item_search(self, search_index, keywords=None, page=None, response_groups=None, parameters=None):
        params = self._base_params(search_index, response_groups, parameters)
        params['Operation'] = 'ItemSearch'
        if keywords:
            params['Keywords'] = ','.join(keywords)
        if page:
            params['ItemPage'] = page
        req_url = self.request_builder.build_request_url(params)
        response = self._make_get_request(req_url, AmazonItemSearchResponse)
        return response

    def item_lookup(self, item_id, id_type='ASIN', search_index=None, response_groups=None, parameters=None):
        params = self._base_params(search_index, response_groups, parameters)
        params['Operation'] = 'ItemLookup'
        params['ItemId'] = item_id
        params['IdType'] = id_type
        req_url = self.request_builder.build_request_url(params)
        response = self._make_get_request(req_url, AmazonItemLookupResponse)
        return response

    def similarity_lookup(self, asins, response_groups=None, parameters=None):
        params = self._base_params(response_groups=response_groups, parameters=parameters)
        if not isinstance(asins, (list,)):
            asins = [asins]
        params['Operation'] = 'SimilarityLookup'
        params['ItemId'] = ','.join(asins)
        req_url = self.request_builder.build_request_url(params)
        response = self._make_get_request(req_url, AmazonSimilarityLookupResponse)
        return response

    def _make_get_request(self, req_url, response_class):
        req = requests.get(req_url)
        response = response_class(req)
        return response

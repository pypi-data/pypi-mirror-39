import json
import xmltodict


class AmazonProductAPIResponse(object):
    response_obj_name = None
    response_error_name = None

    def __init__(self, response_obj):
        self.status_code = response_obj.status_code
        self.raw_response_content = response_obj.content
        self.data = self._parse_data()
        self.headers = response_obj.headers

    def _parse_data(self):
        data_dict = json.loads(json.dumps(xmltodict.parse(self.raw_response_content, xml_attribs=False)))
        return data_dict

    @property
    def is_error(self):
        return self.status_code >= 400 or not self.data[self.response_obj_name]['Items']['Request']['IsValid'] == 'True'

    @property
    def error_msg(self):
        if self.is_error:
            return self._error_attrib('Message')

    @property
    def error_code(self):
        if self.is_error:
            return self._error_attrib('Code')

    def _error_attrib(self, attrib):
        if self.status_code >= 400:
            return self.data[self.response_error_name]['Error'][attrib]
        return self.data[self.response_obj_name]['Items']['Request']['Errors']['Error'][attrib]


class AmazonItemSearchResponse(AmazonProductAPIResponse):
    response_obj_name = 'ItemSearchResponse'
    response_error_name = 'ItemSearchErrorResponse'


class AmazonItemLookupResponse(AmazonProductAPIResponse):
    response_obj_name = 'ItemLookupResponse'
    response_error_name = 'ItemLookupErrorResponse'


class AmazonSimilarityLookupResponse(AmazonProductAPIResponse):
    response_obj_name = 'SimilarityLookupResponse'
    response_error_name = 'SimilarityLookupErrorResponse'

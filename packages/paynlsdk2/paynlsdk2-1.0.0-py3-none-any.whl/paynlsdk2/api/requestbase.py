try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

from abc import ABCMeta, abstractmethod

from paynlsdk2.api.responsebase import ResponseBase
from paynlsdk2.exceptions import SchemaException
from paynlsdk2.validators import ParamValidator


class RequestBase(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        # type: () -> None
        self._api_token = None
        self._service_id = None
        self._raw_response = None
        self._response = None

    @property
    def api_token(self):
        # type: () -> str
        return self._api_token

    @api_token.setter
    def api_token(self, api_token):
        self._api_token = api_token

    @property
    def service_id(self):
        # type: () -> str
        return self._service_id

    @service_id.setter
    def service_id(self, service_id):
        self._service_id = service_id

    @property
    def raw_response(self):
        # type: () -> str
        return self._raw_response

    @property
    @abstractmethod
    def response(self):
        # type: () -> ResponseBase
        pass

    @abstractmethod
    def requires_api_token(self):
        # type: () -> bool
        pass

    @abstractmethod
    def requires_service_id(self):
        # type: () -> bool
        pass

    @abstractmethod
    def get_version(self):
        # type: () -> int
        pass

    @abstractmethod
    def get_controller(self):
        # type: () -> str
        pass

    @abstractmethod
    def get_method(self):
        # type: () -> str
        pass

    @abstractmethod
    def get_query_string(self):
        # type: () -> str
        pass

    def get_url(self):
        # type: () -> str
        return 'v{0}/{1}/{2}/json'.format(self.get_version(), self.get_controller(), self.get_method())

    def get_std_parameters(self):
        # type: () -> dict
        rs = {}
        if self.requires_api_token():
            ParamValidator.assert_not_empty(self.api_token, 'api_token')
            rs["token"] = self.api_token
        if self.requires_service_id():
            ParamValidator.assert_not_empty(self.service_id, 'service_id')
            rs["serviceId"] = self.service_id
        return rs

    def to_query_string(self):
        # type: () -> str
        rs = self.get_parameters()
        if rs.__len__() == 0:
            return ""
        return urlencode(rs)

    @abstractmethod
    def get_parameters(self):
        # type: () -> dict
        pass

    def handle_schema_errors(self, error_dict):
        # type: () -> dict
        if error_dict:
            raise SchemaException(error_dict)


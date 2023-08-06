import json

from marshmallow import Schema, fields, post_load

from paynlsdk2.api.requestbase import RequestBase
from paynlsdk2.api.responsebase import ResponseBase
from paynlsdk2.objects import Error
from paynlsdk2.validators import ParamValidator


class Response(ResponseBase):
    """
    Request object for the Validate::payserverip API

    :param bool result: validation result. True if request was for a valid PayNL server
    """
    def __init__(self,
                 result=None,
                 *args, **kwargs):
        # type: (bool) -> None
        """
        Initialize the Response object

        :param result: Result of the API call.
                       This indicates whether or not the requested ip address is a valid PayNL IP server address
        :type result: bool
        :param args: Unused
        :type args: list
        :param kwargs: The same keyword arguments that :class:`ResponseBase` receives.
        :type kwargs: dict
        """
        self.result = result
        # The result is a pure boolean, so we'll mimic the base's request object
        kwargs['request'] = Error(result=True)  # Set result to be true to prevent an exception being raised!
        super(Response, self).__init__(**kwargs)

    def __repr__(self):
        # type: () -> str
        return self.__dict__.__str__()


class ResponseSchema(Schema):
    result = fields.Boolean()

    @post_load
    def create_response(self, data):
        # type: (dict) -> Response
        """
        create an instance of the :class:`paynlsdk2.api.validate.payserverip.Response` class

        :param data: dictionary with which the response object can be created
        :type data: dict
        :return: return generated response class
        :rtype: paynlsdk2.api.validate.payserverip.Response
        """
        return Response(**data)


class Request(RequestBase):
    """
    Request object for the Validate::payserverip API

    :param str ip_address: IP address to validate
    """
    def __init__(self, ip_address=None):
        # type: (str) -> None
        """
        Initialize the Request object
        :param ip_address: IP address to validate
        :type ip_address: str
        """
        self.ip_address = ip_address
        super(Request, self).__init__()

    def requires_api_token(self):
        # type: () -> bool
        return False

    def requires_service_id(self):
        # type: () -> bool
        return False

    def get_version(self):
        # type: () -> int
        return 1

    def get_controller(self):
        # type: () -> str
        return 'Validate'

    def get_method(self):
        # type: () -> str
        return 'isPayServerIp'

    def get_query_string(self):
        # type: () -> str
        return ''

    def get_parameters(self):
        # type: () -> dict
        # Validation
        ParamValidator.assert_not_empty(self.ip_address, 'ip_address')
        # Get default api parameters
        rs = self.get_std_parameters()
        # Add own parameters
        rs['ipAddress'] = self.ip_address
        return rs

    @RequestBase.raw_response.setter
    def raw_response(self, raw_response):
        # type: (str) -> None
        self._raw_response = raw_response
        # Do error checking.
        rs = json.loads(self.raw_response)
        schema = ResponseSchema(partial=True)
        self.response, errors = schema.load(rs)
        self.handle_schema_errors(errors)

    @property
    def response(self):
        # type: () -> Response
        """
        Return the API :class:`Response` for the validation request

        :return: The API response
        :rtype: paynlsdk2.api.validate.payserverip.Response
        """
        return self._response

    @response.setter
    def response(self, response):
        # type: (Response) -> None
        # print('{}::respone.setter'.format(self.__module__ + '.' + self.__class__.__qualname__))
        self._response = response

    def __repr__(self):
        # type: () -> str
        return self.__dict__.__str__()



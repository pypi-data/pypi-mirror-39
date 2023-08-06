import json

from marshmallow import Schema, fields, post_load

from paynlsdk2.api.requestbase import RequestBase
from paynlsdk2.api.responsebase import ResponseBase
from paynlsdk2.objects import ErrorSchema
from paynlsdk2.validators import ParamValidator


class Response(ResponseBase):
    """
    Response object for the Transaction::approve API

    :param bool result: Result of the API call
    :param str message: message related to the API call
    """
    def __init__(self,
                 result=None,
                 message=None,
                 *args, **kwargs):
        # type: (bool, str) -> None
        self.result = result
        self.message = message
        super(Response, self).__init__(**kwargs)

    def __repr__(self):
        # type: () -> str
        return self.__dict__.__str__()


class ResponseSchema(Schema):
    request = fields.Nested(ErrorSchema)
    message = fields.String(required=False)

    @post_load
    def create_response(self, data):
        # type: (dict) -> None
        #  We will map the result to a Response internal value
        data['result'] = data['request'].result
        return Response(**data)


class Request(RequestBase):
    """
    Request object for the Transaction::approve API

    :param str order_id: transaction ID (wrongly names order_id)
    :param str entrance_code: Entrance code
    """
    def __init__(self, order_id=None, entrance_code=None):
        # type: (str, str) -> None
        self.order_id = order_id
        self.entrance_code = entrance_code
        super(Request, self).__init__()

    def requires_api_token(self):
        # type: () -> bool
        return True

    def requires_service_id(self):
        # type: () -> bool
        return False

    def get_version(self):
        # type: () -> int
        return 12

    def get_controller(self):
        # type: () -> str
        return 'Transaction'

    def get_method(self):
        # type: () -> str
        return 'approve'

    def get_query_string(self):
        # type: () -> str
        return ''

    def get_parameters(self):
        # type: () -> dict
        # Validation
        ParamValidator.assert_not_empty(self.order_id, 'order_id')
        # Get default api parameters
        rs = self.get_std_parameters()
        # Add own parameters
        rs['orderId'] = self.order_id
        if ParamValidator.not_empty(self.entrance_code):
            rs['entranceCode'] = self.entrance_code
        return rs

    @RequestBase.raw_response.setter
    def raw_response(self, raw_response):
        self._raw_response = raw_response
        # Do error checking.
        rs = json.loads(self.raw_response)
        schema = ResponseSchema(partial=True)
        response, errors = schema.load(rs)
        self.handle_schema_errors(errors)
        self._response = response

    @property
    def response(self):
        # type: () -> Response
        """
        Return the API :class:`Response` for the validation request

        :return: The API response
        :rtype: paynlsdk2.api.transaction.approve.Response
        """
        return self._response

    @response.setter
    def response(self, response):
        # print('{}::respone.setter'.format(self.__module__ + '.' + self.__class__.__qualname__))
        self._response = response


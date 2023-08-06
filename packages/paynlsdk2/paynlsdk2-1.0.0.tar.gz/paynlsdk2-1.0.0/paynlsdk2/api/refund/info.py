import json

from marshmallow import Schema, fields, post_load, pre_load

from paynlsdk2.api.requestbase import RequestBase
from paynlsdk2.api.responsebase import ResponseBase
from paynlsdk2.objects import ErrorSchema, RefundInfo, RefundInfoSchema
from paynlsdk2.validators import ParamValidator


class Response(ResponseBase):
    # type: (ResponseBase)
    """
    Response object for the Refund::info API

    :param str refund_id: Refund ID
    :param RefundInfo refund: Refund information
    """
    def __init__(self,
                 refund_id=None,
                 refund=None,
                 *args, **kwargs):
        # type: (str, RefundInfo *str, **Any) -> None
        self.refund_id = refund_id
        self.refund = refund
        super(Response, self).__init__(**kwargs)

    def __repr__(self):
        return str(self.__dict__)

    def is_refunded(self):
        # type: () -> bool
        """
        Check if refund is processed
        :return: indication whether the refund has been processed or not
        :rtype: bool
        """
        return self.refund.status_name == 'Verwerkt'


class ResponseSchema(Schema):
    request = fields.Nested(ErrorSchema, required=True)
    refund_id = fields.String(required=True, load_from='refundId')
    refund = fields.Nested(RefundInfoSchema, required=True, load_from='refund', allow_none=True)

    @pre_load
    def pre_processor(self, data):
        if data['refund'] == '':
            data['refund'] = None
        return data

    @post_load
    def create_response(self, data):
        # type: (dict) -> Response
        return Response(**data)


class Request(RequestBase):
    """
    Request object for the Refund::info API

    :param str refund_id: Refund ID
    """
    def __init__(self, refund_id=None):
        # type: (str) -> None
        self.refund_id = refund_id
        super(Request, self).__init__()

    def requires_api_token(self):
        # type: () -> bool
        return True

    def requires_service_id(self):
        # type: () -> bool
        return False

    def get_version(self):
        # type: () -> int
        return 3

    def get_controller(self):
        # type: () -> str
        return 'Refund'

    def get_method(self):
        # type: () -> str
        return 'info'

    def get_query_string(self):
        # type: () -> str
        return ''

    def get_parameters(self):
        # type: () -> dict
        # Validation
        ParamValidator.assert_not_empty(self.refund_id, 'refund_id')
        # Get default api parameters
        rs = self.get_std_parameters()
        # Add own parameters
        rs['refundId'] = self.refund_id
        return rs

    @RequestBase.raw_response.setter
    def raw_response(self, raw_response):
        # type: (str) -> None
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
        :rtype: paynlsdk2.api.refund.info.Response
        """
        return self._response

    @response.setter
    def response(self, response):
        # type: (Response) -> None
        # print('{}::respone.setter'.format(self.__module__ + '.' + self.__class__.__qualname__))
        self._response = response


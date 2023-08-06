import json

from paynlsdk2.api.requestbase import RequestBase
from paynlsdk2.api.responsebase import ResponseBase
from paynlsdk2.objects import Error, BankDetails, BankDetailsSchema


class Response(ResponseBase):
    """
    Response object for the Transaction::getbanks API

    :param List[BankDetails] banks: list of banks
    """
    def __init__(self,
                 banks,
                 *args, **kwargs):
        # type: (List[BankDetails]) -> None
        self.banks = banks
        # the result is a list. We'll mimic the request object IF not yet available (should have been done though)
        if 'request' not in kwargs:
            kwargs['request'] = Error(result=True)
        super(Response, self).__init__(**kwargs)

    def __repr__(self):
        # type: () -> str
        return self.__dict__.__str__()


class Request(RequestBase):
    """
    Request object for the Transaction::getbanks API
    """
    def __init__(self):
        # type: () -> None
        super(Request, self).__init__()

    def requires_api_token(self):
        # type: () -> bool
        return False

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
        return 'getBanks'

    def get_query_string(self):
        # type: () -> str
        return ''

    def get_parameters(self):
        # type: () -> dict
        # Get default api parameters
        rs = self.get_std_parameters()
        # No further parameters
        return rs

    @RequestBase.raw_response.setter
    def raw_response(self, raw_response):
        self._raw_response = raw_response
        # Do error checking.
        rs = json.loads(self.raw_response)
        # The raw result IS a list, so we need the "many=True" argument
        schema = BankDetailsSchema(partial=True, many=True)
        # Bit of an oddball here. Result is a pure array of banks, so we'll mimic a decent response
        banks, errors = schema.load(rs)
        self.handle_schema_errors(errors)
        kwargs = {"result": Error(result=True), "banks": banks}
        self._response = Response(**kwargs)

    @property
    def response(self):
        # type: () -> Response
        """
        Return the API :class:`Response` for the validation request

        :return: The API response
        :rtype: paynlsdk2.api.transaction.getbanks.Response
        """
        return self._response

    @response.setter
    def response(self, response):
        # print('{}::respone.setter'.format(self.__module__ + '.' + self.__class__.__qualname__))
        self._response = response

    def __repr__(self):
        # type: () -> str
        return self.__dict__.__str__()


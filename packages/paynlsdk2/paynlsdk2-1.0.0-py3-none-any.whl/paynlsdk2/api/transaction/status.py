import json

from marshmallow import Schema, fields, post_load

from paynlsdk2.api.requestbase import RequestBase
from paynlsdk2.api.responsebase import ResponseBase
from paynlsdk2.objects import ErrorSchema, TransactionStatusDetails, TransactionStatusDetailsSchema
from paynlsdk2.validators import ParamValidator


class Response(ResponseBase):
    """
    Response object for the Transaction::status API

    :param TransactionStatusDetails payment_details: payment details
    """
    def __init__(self,
                 payment_details=None,
                 *args, **kwargs):
        # type: (TransactionStatusDetails) -> None
        self.payment_details = payment_details
        super(Response, self).__init__(**kwargs)

    def get_transaction_id(self):
        # type: () -> str
        """
        Get EX-code of transaction
        :return: EX-code of the transaction
        :rtype: string
        """
        return self.payment_details.transaction_id

    def get_order_id(self):
        # type: () -> str
        """
        Get order ID of transaction
        :return: the order ID
        :rtype: string
        """
        return self.payment_details.order_id

    def get_payment_profile_id(self):
        # type: () -> int
        """
        Get payment profile ID
        :return: payment profile ID
        :rtype: int
        """
        return self.payment_details.payment_profile_id

    def get_state(self):
        # type: () -> str
        """
        Get transaction status
        :return: transaction state
        :rtype: int
        """
        return self.payment_details.state

    def get_state_name(self):
        # type: () -> str
        """
        Get transaction status name
        :return: transaction status name
        :rtype: string
        """
        return self.payment_details.state_name

    def get_currency(self):
        # type: () -> str
        """
        Get currency of transaction
        :return: currency
        :rtype: string
        """
        return self.payment_details.currency

    def get_amount(self):
        # type: () -> float
        """
        Get transaction amount in EURO
        :return: transaction amount in EURO
        :rtype: float
        """
        return self.payment_details.amount / 100

    def get_currency_amount(self):
        # type: () -> float
        """
        Get transaction amount in payment currency
        :return: transaction amount in payment currency
        :rtype: float
        """
        return self.payment_details.currency_amount / 100

    def get_paid_amount(self):
        # type: () -> float
        """
        Get paid transaction amount in EURO
        :return: paid transaction amount in EURO
        :rtype: float
        """
        return self.payment_details.paid_amount / 100

    def get_paid_currency_amount(self):
        # type: () -> float
        """
        Get paid transaction amount in payment currency
        :return: paid transaction amount in payment currency
        :rtype: float
        """
        return self.payment_details.paid_currency_amount / 100

    def get_refunded_amount(self):
        # type: () -> float
        """
        Get refunded transaction amount in EURO
        :return: refunded transaction amount in EURO
        :rtype: float
        """
        return self.payment_details.refund_amount / 100

    def get_refunded_currency_amount(self):
        # type: () -> float
        """
        Get refunded transaction amount in payment currency
        :return: refunded transaction amount in payment currency
        :rtype: float
        """
        return self.payment_details.refund_currency_amount / 100

    def __repr__(self):
        # type: () -> str
        return str(self.__dict__)


class ResponseSchema(Schema):
    request = fields.Nested(ErrorSchema)
    payment_details = fields.Nested(TransactionStatusDetailsSchema, load_from='paymentDetails')

    @post_load
    def create_response(self, data):
        # type: (dict) -> Response
        return Response(**data)


class Request(RequestBase):
    """
    Response object for the Transaction::status API

    :param str transaction_id: transaction ID
    """
    def __init__(self, transaction_id=None):
        # type: (str) -> None
        self.transaction_id = transaction_id
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
        return 'status'

    def get_query_string(self):
        # type: () -> str
        return ''

    def get_parameters(self):
        # type: () -> dict
        # Validation
        ParamValidator.assert_not_empty(self.transaction_id, 'transaction_id')
        # Get default api parameters
        rs = self.get_std_parameters()
        # Add own parameters
        rs['transactionId'] = self.transaction_id
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
        :rtype: paynlsdk2.api.transaction.status.Response
        """
        return self._response

    @response.setter
    def response(self, response):
        # print('{}::respone.setter'.format(self.__module__ + '.' + self.__class__.__qualname__))
        self._response = response


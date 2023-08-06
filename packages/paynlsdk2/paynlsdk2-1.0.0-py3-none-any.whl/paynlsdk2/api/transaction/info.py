import json

from marshmallow import Schema, fields, post_load, pre_load

from paynlsdk2.api.requestbase import RequestBase
from paynlsdk2.api.responsebase import ResponseBase
from paynlsdk2.objects import ErrorSchema, Connection, ConnectionSchema, EndUser, EndUserSchema,\
    PaymentDetails, PaymentDetailsSchema, StornoDetails, StornoDetailsSchema,\
    SalesData, SalesDataSchema, StatsDetails, StatsDetailsSchema
from paynlsdk2.validators import ParamValidator
from paynlsdk2.exceptions import TransactionStatusException, TransactionNotAuthorizedException


class Response(ResponseBase):
    """
    Response object for the Transaction::info API

    :param Connection connection: connection details
    :param EndUser enduser: enduser details
    :param PaymentDetails payment_details: payment details
    :param StornoDetails storno_details: storno details
    :param StatsDetails stats_details: stats details
    :param str transaction_id: transaction ID
    """
    def __init__(self,
                 connection=None,
                 enduser=None,
                 sale_data=None,
                 payment_details=None,
                 storno_details=None,
                 stats_details=None,
                 transaction_id=None,
                 *args, **kwargs):
        self.connection = connection
        self.enduser = enduser
        self.sale_data = sale_data
        self.payment_details = payment_details
        self.storno_details = storno_details
        self.stats_details = stats_details
        self.transaction_id = transaction_id
        super(Response, self).__init__(**kwargs)

    def get_status(self):
        """
        Get transaction status
        :return: Response object if transaction.status API
        :rtype: paynlsdk2.api.transaction.status.Response
        """
        from paynlsdk2.api.transaction.status import Request
        from paynlsdk2.api.client import APIClient
        client = APIClient()
        request = Request(self.transaction_id)
        client.perform_request(request)
        return request.response

    def is_paid(self):
        """
        Check if the transaction has been PAID
        :return: True of transaction is PAID, False otherwise
        :rtype: bool
        """
        return self.payment_details.state_name == 'PAID'

    def is_pending(self):
        """
        Check if the transaction is in PENDING state
        :return: True of transaction is PENDING, False otherwise
        :rtype: bool
        """
        return self.payment_details.state_name == 'PENDING' or self.payment_details.state_name == 'VERIFY'

    def is_cancelled(self):
        """
        Check if the transaction has been CANCELLED
        :return: True of transaction is CANCELLED, False otherwise
        :rtype: bool
        """
        return self.payment_details.state <= 0

    def is_authorized(self):
        """
        Check if the transaction has been AUTHORIZED
        :return: True of transaction is AUTHORIZED, False otherwise
        :rtype: bool
        """
        return self.payment_details.state == 95

    def is_being_verified(self):
        """
        Check if the transaction has been VERIFIED
        :return: True of transaction is VERIFIED, False otherwise
        :rtype: bool
        """
        return self.payment_details.state_name == 'VERIFY'

    def is_refunded(self, allow_partial_refunds=True):
        """
        Check if the transaction has been (partially) REFUNDED

        :param allow_partial_refunds: True to allow checking for partial refunds
        :type allow_partial_refunds: bool
        :return: True of transaction is (partially) REFUNDED, False otherwise
        :rtype: bool
        """
        if self.payment_details.state_name == 'REFUND':
            return True
        elif allow_partial_refunds and self.payment_details.state_name == 'PARTIAL_REFUND':
            return True
        else:
            return False

    def is_partially_refunded(self):
        """
        Check if the transaction has been partially REFUNDED

        :return: True of transaction is partially REFUNDED, False otherwise
        :rtype: bool
        """
        return self.payment_details.state_name == 'PARTIAL_REFUND'

    def get_id(self):
        """
        Get transaction ID

        :return: transaction ID
        :rtype: str
        """
        return self.transaction_id

    def get_amount(self):
        """
        Get transaction amount in EURO
        :return: transaction amount in EURO
        :rtype: float
        """
        return self.payment_details.amount / 100

    def get_paid_amount(self):
        """
        Get paid transaction amount in EURO
        :return: paid transaction amount in EURO
        :rtype: float
        """
        return self.payment_details.paid_amount / 100

    def get_currency_amount(self):
        """
        Get transaction amount in payment currency
        :return: transaction amount in payment currency
        :rtype: float
        """
        return self.payment_details.currency_amount / 100

    def get_paid_currency(self):
        """
        Get currency of transaction
        :return: currency
        :rtype: string
        """
        return self.payment_details.paid_currency

    def get_paid_currency_amount(self):
        """
        Get paid transaction amount in payment currency
        :return: paid transaction amount in payment currency
        :rtype: float
        """
        return self.payment_details.paid_currency_amount / 100

    def get_refunded_amount(self):
        """
        Get refunded transaction amount in EURO
        :return: refunded transaction amount in EURO
        :rtype: float
        """
        self._get_status().get_refunded_amount()

    def get_refunded_currency_amount(self):
        """
        Get refunded transaction amount in payment currency
        :return: refunded transaction amount in payment currency
        :rtype: float
        """
        self._get_status().get_refunded_currency_amount()

    def get_account_holder_name(self):
        """
        Get account holder name for transaction
        :return: transaction account holder name
        :rtype: str
        """
        return self.payment_details.identifier_name

    def get_account_number(self):
        """
        Get account number or masked creditcard number for transaction
        :return: transaction account number
        :rtype: str
        """
        return self.payment_details.identifier_public

    def get_account_hash(self):
        """
        Get account hash for transaction (account number or masked creditcard number)
        :return: transaction account hash
        :rtype: str
        """
        return self.payment_details.identifier_hash

    def get_payment_method_name(self):
        """
        Get payment method name for transaction
        :return: transaction payment method name
        :rtype: str
        """
        return self.payment_details.payment_profile_name

    def get_description(self):
        """
        Get description for transaction
        :return: transaction description
        :rtype: str
        """
        return self.payment_details.description

    def get_extra1(self):
        """
        Get extra1 field for transaction (statsdetails)
        :return: transaction extra1 field value
        :rtype: str
        """
        return self.stats_details.extra1

    def get_extra2(self):
        """
        Get extra2 field for transaction (statsdetails)
        :return: transaction extra2 field value
        :rtype: str
        """
        return self.stats_details.extra2

    def get_extra3(self):
        """
        Get extra3 field for transaction (statsdetails)
        :return: transaction extra3 field value
        :rtype: str
        """
        return self.stats_details.extra3

    def approve(self):
        """
        Approve transaction that needs verification

        :return: Result of the approval: True is successful
        :rtype:  bool
        :raise: TransactionStatusException if not current status is not VERIFY
        """
        if not self.is_being_verified():
            raise TransactionStatusException('Cannot decline transaction because it does not have the status VERIFY')
        from paynlsdk2.api.transaction.approve import Request
        from paynlsdk2.api.client import APIClient
        client = APIClient()
        request = Request(self.transaction_id)
        client.perform_request(request)
        return request.response.result

    def decline(self):
        """
        Decline transaction that needs verification

        :return: Result of the decline: True is successful
        :rtype:  bool
        :raise: TransactionStatusException if not current status is not VERIFY
        """
        if not self.is_being_verified():
            raise TransactionStatusException('Cannot decline transaction because it does not have the status VERIFY')
        from paynlsdk2.api.transaction.decline import Request
        from paynlsdk2.api.client import APIClient
        client = APIClient()
        request = Request(self.transaction_id)
        client.perform_request(request)
        return request.response.result

    def void(self):
        """
        Void authorized transaction

        :return: Result of the void: True is successful
        :rtype:  bool
        :raise: TransactionNotAuthorizedException if not yet authorized
        """
        if not self.is_authorized():
            raise TransactionNotAuthorizedException('Cannot capture transaction, status is not authorized')
        # We will NOT use the "utility" methds here but the full API implementation
        from paynlsdk2.api.transaction.voidauthorization import Request
        from paynlsdk2.api.client import APIClient
        client = APIClient()
        request = Request(self.transaction_id)
        client.perform_request(request)
        return request.response.result

    def capture(self):
        """
        Capture authorized transaction

        :return: Result of the capture: True is successful
        :rtype:  bool
        :raise: TransactionNotAuthorizedException if not yet authorized
        """
        if not self.is_authorized():
            raise TransactionNotAuthorizedException('Cannot capture transaction, status is not authorized')
        # We will NOT use the "utility" methds here but the full API implementation
        from paynlsdk2.api.transaction.capture import Request
        from paynlsdk2.api.client import APIClient
        client = APIClient()
        request = Request(self.transaction_id)
        client.perform_request(request)
        return request.response.result

    def __repr__(self):
        # type: () -> str
        return str(self.__dict__)


class ResponseSchema(Schema):
    request = fields.Nested(ErrorSchema, required=True)
    connection = fields.Nested(ConnectionSchema, required=True)
    enduser = fields.Nested(EndUserSchema, required=True)
    sale_data = fields.Nested(SalesDataSchema, required=False, load_from='saleData')
    payment_details = fields.Nested(PaymentDetailsSchema, required=True, load_from='paymentDetails')
    storno_details = fields.Nested(StornoDetailsSchema, required=False, load_from='stornoDetails')
    stats_details = fields.Nested(StatsDetailsSchema, required=False, load_from='statsDetails')

    @pre_load
    def pre_processor(self, data):
        # No-op yet (see complex subtypes)
        return data

    @post_load
    def create_response(self, data):
        # type: (dict) -> Response
        return Response(**data)


class Request(RequestBase):
    """
    Request object for the Transaction::info API

    :param str transaction_id: transaction ID
    :param str entrance_code: entrance code
    """
    def __init__(self, transaction_id=None, entrance_code=None):
        self.transaction_id = transaction_id
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
        return 'info'

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
        if ParamValidator.not_empty(self.entrance_code):
            rs['entranceCode'] = self.entrance_code
        return rs

    @RequestBase.raw_response.setter
    def raw_response(self, raw_response):
        self._raw_response = raw_response
        rs = json.loads(self.raw_response)
        schema = ResponseSchema(partial=True)
        response, errors = schema.load(rs)
        self.handle_schema_errors(errors)
        self._response = response
        #  Map transaction ID on response
        self._response.transaction_id = self.transaction_id

    @property
    def response(self):
        # type: () -> Response
        """
        Return the API :class:`Response` for the validation request

        :return: The API response
        :rtype: paynlsdk2.api.transaction.info.Response
        """
        return self._response

    @response.setter
    def response(self, response):
        # print('{}::respone.setter'.format(self.__module__ + '.' + self.__class__.__qualname__))
        self._response = response


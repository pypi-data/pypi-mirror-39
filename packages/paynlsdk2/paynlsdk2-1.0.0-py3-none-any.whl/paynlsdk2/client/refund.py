from paynlsdk2.api.client import APIClient


class Refund(object):
    @staticmethod
    def info(refund_id):
        # type: (str) -> paynlsdk2.api.refund.info.Response
        """
        Return refund info

        :param refund_id: Refund ID (starts wih "RF-")
        :type refund_id: str
        :return: Info Response
        :rtype: paynlsdk2.api.refund.info.Response
        """
        from paynlsdk2.api.refund.info import Request
        client = APIClient()
        request = Request(refund_id)
        client.perform_request(request)
        return request.response

    @staticmethod
    def transaction(transaction_id,
                    amount=None,
                    description=None,
                    process_date=None,
                    products={},
                    vat_percentage=None,
                    exchange_url=None):
        # type: (str, int, str, str, dict, float, str) -> paynlsdk2.api.refund.transaction.Response
        """
        Refund a transaction

        :param transaction_id: Transaction ID
        :type transaction_id: str
        :param amount: transaction amount to refund
        :type amount: int
        :param description: refund description
        :type description: str
        :param process_date: date at which refund needs to be processed
                TODO: this *should* be a datetime
        :type process_date: str
        :param products: dictionary of products to refund (keys: product ID, value: quantity)
        :type products: dict
        :param vat_percentage: VAT percentage
        :type vat_percentage: float
        :param exchange_url: URL for the exchange call
        :type exchange_url: str
        :return: Transaction refund response
        :rtype: paynlsdk2.api.refund.transaction.Response
        """
        from paynlsdk2.api.refund.transaction import Request
        client = APIClient()
        request = Request(transaction_id, amount, description, process_date, products, vat_percentage, exchange_url)
        client.perform_request(request)
        return request.response

    @staticmethod
    def info_request():
        # type: () -> paynlsdk2.api.refund.info.Request
        """
        Get a refund info request instance

        :return: The request object that can be configured
        :rtype: paynlsdk2.api.refund.info.Request
        """
        from paynlsdk2.api.refund.info import Request
        return Request()

    @staticmethod
    def transaction_request():
        # type: () -> paynlsdk2.api.refund.info.Request
        """
        Get a refund transaction request instance

        :return: The request object that can be configured
        :rtype: paynlsdk2.api.refund.transaction.Request
        """
        from paynlsdk2.api.transaction.info import Request
        return Request()

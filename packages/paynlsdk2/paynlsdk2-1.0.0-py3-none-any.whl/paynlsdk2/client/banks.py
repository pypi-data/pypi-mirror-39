from paynlsdk2.api.transaction.getbanks import Response
from paynlsdk2.objects import BankDetails
from typing import List


class Banks(object):
    @staticmethod
    def get_list():
        # type: () -> List[BankDetails]
        """
        Gets the list of banks.

        Please note this method is a mapping from the paynlsdk2.client.transaction.Transaction.get_banks() method,
        that returns the internal List object of banks.
        :return: List of banks
        :rtype: List[BankDetails]
        """
        from paynlsdk2.client.transaction import Transaction
        return Transaction.get_banks()

    @staticmethod
    def get_list_response():
        # type: () -> Response
        """
        Get a get_banks :class:`paynlsdk2.api.transaction.getbanks.Response` instance

        Please note this method is a mapping from the paynlsdk2.client.transaction.Transaction.get_banks() method,
        that returns the internal List object of banks.
        :return: Response object
        :rtype: paynlsdk2.api.transaction.getbanks.Response
        """
        from paynlsdk2.client.transaction import Transaction
        return Transaction.get_banks_response()


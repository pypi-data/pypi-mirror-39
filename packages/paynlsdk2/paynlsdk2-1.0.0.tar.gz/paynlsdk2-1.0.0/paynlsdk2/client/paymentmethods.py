from paynlsdk2.api.client import APIClient
from paynlsdk2.objects import ServicePaymentProfile


class PaymentMethods(object):
    @staticmethod
    def get_list(payment_method_id=None):
        # type: (int) -> Dict[int, ServicePaymentProfile]
        """
        Gets the list of payment methods.

        :param payment_method_id: payment method ID (defaults to 10, or iDeal)
        :type payment_method_id: int
        :return: List of banks
        :rtype: List[ServicePaymentProfile]
        """
        from paynlsdk2.api.transaction.getservicepaymentoptions import Request
        client = APIClient()
        request = Request()
        client.perform_request(request)
        profiles = request.response.payment_profiles
        if payment_method_id is None:
            return profiles
        elif payment_method_id in profiles:
            return {payment_method_id: profiles[payment_method_id]}
        raise KeyError('Payment method ID "{}" is not found in the result dictionary'.format(payment_method_id))



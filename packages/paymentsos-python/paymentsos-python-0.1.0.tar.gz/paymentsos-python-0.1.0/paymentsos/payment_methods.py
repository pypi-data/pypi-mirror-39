class PaymentMethod(object):

    def __init__(self, client):
        self.client = client

    def create_payment_method(self, *, customer_id, token):
        headers = self.client._get_private_headers()
        fmt = '/customers/{}/payment-methods/{}'
        return self.client._post(self.client.URL_BASE + fmt.format(customer_id, token), headers=headers)

    def retrieve_payment_method(self):
        raise NotImplementedError

    def delete_payment_method(self):
        raise NotImplementedError

    def retrieve_all_payment_methods(self):
        raise NotImplementedError

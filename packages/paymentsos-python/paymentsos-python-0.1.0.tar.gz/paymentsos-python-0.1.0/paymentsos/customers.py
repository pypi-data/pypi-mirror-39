class Customer(object):

    def __init__(self, client):
        self.client = client

    def create_customer(self, *, customer_reference, email):
        headers = self.client._get_private_headers()
        payload = {
            "customer_reference": customer_reference,
            "email": email
        }
        fmt = '/customers'
        return self.client._post(self.client.URL_BASE + fmt, json=payload, headers=headers)

    def retrieve_customer_by_reference(self):
        raise NotImplementedError

    def retrieve_customer_by_id(self, customer_id):
        headers = self.client._get_private_headers()
        fmt = '/customers/{}'
        return self.client._get(self.client.URL_BASE + fmt.format(customer_id), headers=headers)

    def update_customer(self):
        raise NotImplementedError

    def delete_customer(self):
        raise NotImplementedError

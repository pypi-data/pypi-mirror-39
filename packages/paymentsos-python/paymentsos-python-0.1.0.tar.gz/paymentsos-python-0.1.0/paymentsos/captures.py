class Capture(object):

    def __init__(self, client):
        self.client = client

    def create_capture(self, payment_id):
        headers = self.client._get_private_headers()
        fmt = '/payments/{}/captures'
        return self.client._post(self.client.URL_BASE + fmt.format(payment_id), headers=headers)

    def retrieve_all_captures(self):
        raise NotImplementedError

    def retrieve_capture(self):
        raise NotImplementedError

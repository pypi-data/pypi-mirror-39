class Refund(object):

    def __init__(self, client):
        self.client = client

    def create_refund(self):
        raise NotImplementedError

    def retrieve_all_refunds(self):
        raise NotImplementedError

    def retrieve_refund(self):
        raise NotImplementedError

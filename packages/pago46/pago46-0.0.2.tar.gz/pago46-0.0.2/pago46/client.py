import os

import requests

from pago46.utils import sign_request


class Pago46(object):
    """Pago46 Client"""
    url_merchant_order = "/merchant/order"
    url_merchant_orders = "/merchant/orders"
    url_merchant_complete = "/merchant/complete/"
    url_merchant_notification = "/merchant/notification"

    def __init__(self):
        """PARAMS to inicialize the client of PAGO46"""
        self.merchant_key = self.__get_merchant_key()
        self.merchant_secret = self.__get_merchant_secret()
        self.pago46_api_host = self.__get_pago46_api_host()

    def __get_merchant_key(self):
        if not "PAGO46_MERCHANT_KEY" in os.environ:
            raise KeyError("needs a environment variable called PAGO46_MERCHANT_KEY")
        return os.environ['PAGO46_MERCHANT_KEY']

    def __get_merchant_secret(self):
        if not "PAGO46_MERCHANT_SECRET" in os.environ:
            raise KeyError("needs a environment variable called PAGO46_MERCHANT_SECRET")
        return os.environ['PAGO46_MERCHANT_SECRET']

    def __get_pago46_api_host(self):
        if not "PAGO46_API_HOST" in os.environ:
            raise KeyError("needs a environment variable called PAGO46_API_HOST")
        return os.environ['PAGO46_API_HOST']

    def get_all_orders(self):
        """ Get all orders from a e-merchant"""
        method = "GET"
        message_hash, date = sign_request(method=method, path=self.url_merchant_orders, merchant_key=self.merchant_key,
                                          merchant_secret=self.merchant_secret)
        headers = {
            "merchant-key": self.merchant_key,
            "message-hash": message_hash,
            "message-date": date
        }
        url = "{}{}".format(self.pago46_api_host, self.url_merchant_orders)
        response = requests.get(url, headers=headers)
        return response

    def create_order(self, payload):
        """Create a order on Pago46
            params:
             -merchant_order_id
             -currency
             -price
             -timeout
             -notify_url
             -return_url
             -description (opcional)
        """
        method = "POST"
        message_hash, date = sign_request(method=method, path=self.url_merchant_orders, payload=payload,
                                          merchant_key=self.merchant_key, merchant_secret=self.merchant_secret)
        headers = {
            "merchant-key": self.merchant_key,
            "message-hash": message_hash,
            "message-date": date
        }
        url = "{}{}".format(self.pago46_api_host, self.url_merchant_orders)
        response = requests.post(url, data=payload, headers=headers)
        return response

    def mark_order_as_complete(self, payload):
        method = "POST"
        message_hash, date = sign_request(method=method, path=self.url_merchant_complete, payload=payload,
                                          merchant_key=self.merchant_key, merchant_secret=self.merchant_secret)
        headers = {
            "merchant-key": self.merchant_key,
            "message-hash": message_hash,
            "message-date": date
        }
        url = "{}{}".format(self.pago46_api_host, self.url_merchant_complete)
        response = requests.post(url, data=payload, headers=headers)
        return response

    def get_order_by_id(self, order_id):
        method = "GET"
        path = "{}/{}".format( self.url_merchant_order, order_id)
        message_hash, date = sign_request(method=method, path=path, merchant_key=self.merchant_key,
                                          merchant_secret=self.merchant_secret)
        headers = {
            "merchant-key": self.merchant_key,
            "message-hash": message_hash,
            "message-date": date
        }
        url = "{}{}/{}".format(self.pago46_api_host, self.url_merchant_order, order_id)

        response = requests.get(url, headers=headers)
        return response

    def get_order_by_notification_id(self, notification_id):
        method = "GET"
        path = "{}/{}".format(self.url_merchant_notification, notification_id)
        message_hash, date = sign_request(method=method, path=path, merchant_key=self.merchant_key,
                                          merchant_secret=self.merchant_secret)
        headers = {
            "merchant-key": self.merchant_key,
            "message-hash": message_hash,
            "message-date": date
        }

        url = "{}{}/{}".format(self.pago46_api_host, self.url_merchant_notification, notification_id)

        response = requests.get(url, headers=headers)
        return response

    def get_order_details_by_order_id(self, order_id):
        method = "GET"
        path = "{}/{}/detail".format(self.url_merchant_order, order_id)
        message_hash, date = sign_request(method=method, path=path, merchant_key=self.merchant_key,
                                          merchant_secret=self.merchant_secret)
        headers = {
            "merchant-key": self.merchant_key,
            "message-hash": message_hash,
            "message-date": date
        }
        url = "{}{}/{}/detail".format(self.pago46_api_host, self.url_merchant_order, order_id)
        response = requests.get(url, headers=headers)
        return response

    def update_merchant_order_id(self, id, new_merchant_order_id):
        method = "PATCH"
        payload = {'merchant_order_id': new_merchant_order_id}

        path = "{}/{}/update/".format(self.url_merchant_order, id)
        message_hash, date = sign_request(method=method, path=path, payload=payload, merchant_key=self.merchant_key,
                                          merchant_secret=self.merchant_secret)
        headers = {
            "merchant-key": self.merchant_key,
            "message-hash": message_hash,
            "message-date": date,
            "Content-type": "application/x-www-form-urlencoded"

        }

        url = "{}{}".format(self.pago46_api_host, path)
        response = requests.patch(url, data=payload, headers=headers)
        return response

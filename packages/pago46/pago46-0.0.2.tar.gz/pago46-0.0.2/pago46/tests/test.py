import json
import os
from unittest import TestCase
from unittest import mock
import six

from pago46.client import Pago46


class Pago46TestCase(TestCase):
    def setUp(self):
        """
        Set all enviroment variables to init Pago46 Class
        """
        os.environ["PAGO46_MERCHANT_KEY"] = "secret_merchant_key"
        os.environ["PAGO46_MERCHANT_SECRET"] = "secret_merchant_secret"
        os.environ["PAGO46_API_HOST"] = "https://sandboxapi.pago46.com"

    def test_called_with_all_arguments(self):
        """
        init Pago46 can be done with all it's arguments
        """
        client = Pago46()
        self.assertEqual(client.merchant_key, "secret_merchant_key")
        self.assertEqual(client.merchant_secret, "secret_merchant_secret")
        self.assertEqual(client.pago46_api_host, "https://sandboxapi.pago46.com")

    def test_no_merchant_key_given(self):
        """
        init Pago46 raises an exception if no merchant_key is given
        """
        del os.environ['PAGO46_MERCHANT_KEY']

        six.assertRaisesRegex(self, KeyError, "needs a environment variable called PAGO46_MERCHANT_KEY", Pago46)

    def test_no_merchant_secret_given(self):
        """
        init Pago46 raises an exception if no merchant_secret is given
        """
        del os.environ['PAGO46_MERCHANT_SECRET']

        six.assertRaisesRegex(self, KeyError, "needs a environment variable called PAGO46_MERCHANT_SECRET", Pago46)

    def test_no_pago46_api_host_given(self):
        """
        init Pago46 raises an exception if no pago46_api_host is given
        """
        del os.environ['PAGO46_API_HOST']

        six.assertRaisesRegex(self, KeyError, "needs a environment variable called PAGO46_API_HOST", Pago46)

    @mock.patch('pago46.client.requests.post')
    def test_create_a_new_order(self, mock_post):
        """
        Create a new order on Pago46
        """
        client = Pago46()

        response = {
            "id": "d9125b94-275d-49c9-8a99-ea3511302c9d",
            "price": "4500.00",
            "description": "description",
            "merchant_order_id": "000006",
            "creation_date": "2018-06-27T22:36:56.415643Z",
            "return_url": "http://final.merchant.com",
            "redirect_url": "https://novatest.pago46.com/#UID=d9125b94-275d-49c9-8a99-ea3511302c9d",
            "status": "expired",
            "timeout": 60,
            "notify_url": "http://notification.merchant.com"
        }

        mock_post.return_value = mock.MagicMock(
            headers={'content-type': 'application/json'}, status_code=200, response=json.dumps(response))

        payload = {
            "currency": "CLP",
            "description": "description testing from python librari",
            "merchant_order_id": 'testpythonlibrary1',
            "notify_url": "http://merchant.com/app/response",
            "price": 1000,
            "return_url": "http://final.merchant.com",
            "timeout": 60
        }

        response = client.create_order(payload)
        self.assertEqual(response.status_code, 200)

    @mock.patch('pago46.client.requests.get')
    def test_get_order_by_id(self, mock_get):
        client = Pago46()
        response = {
                    "id": "a6a47f03-d0d3-446b-962d-caf3a7cebb30",
                    "price": "1500.00",
                    "description": "description",
                    "merchant_order_id": "000001",
                    "creation_date": "2018-05-29T20:42:48.853959Z",
                    "return_url": "http://final.merchant.com",
                    "redirect_url": "https://novatest.pago46.com/#UID=a6a47f03-d0d3-446b-962d-caf3a7cebb30",
                    "status": "expired",
                    "timeout": 60,
                    "notify_url": "http://notification.merchant.com"
                }
        mock_get.return_value = mock.MagicMock(
            headers={'content-type': 'application/json'}, status_code=200, response=json.dumps(response))

        order_id = 'a6a47f03-d0d3-446b-962d-caf3a7cebb30'
        response = client.get_order_by_id(order_id)

        self.assertEqual(response.status_code, 200)

    @mock.patch('pago46.client.requests.post')
    def test_mark_order_as_complete(self, mock_post):
        client = Pago46()
        mock_post.return_value = mock.MagicMock(
            headers={'content-type': 'application/json'}, status_code=200, response=json.dumps({'response': 'ok'}))

        payload = {"order_id": "a6a47f03-d0d3-446b-962d-caf3a7cebb30"}
        response = client.mark_order_as_complete(payload)

        self.assertEqual(response.status_code, 200)

    @mock.patch('pago46.client.requests.get')
    def test_get_all_orders(self, mock_get):
        client = Pago46()
        mock_get.return_value = mock.MagicMock(
            headers={'content-type': 'application/json'}, status_code=200, response=json.dumps({'response': 'ok'}))

        response = client.get_all_orders()

        self.assertEqual(response.status_code, 200)

    @mock.patch('pago46.client.requests.get')
    def test_get_order_by_notification_id(self, mock_get):
        client = Pago46()
        mock_get.return_value = mock.MagicMock(
            headers={'content-type': 'application/json'}, status_code=200, response=json.dumps({'response': 'ok'}))
        order_id = 'a6a47f03-d0d3-446b-962d-caf3a7cebb30'
        response = client.get_order_by_notification_id(order_id)

        self.assertEqual(response.status_code, 200)

    @mock.patch('pago46.client.requests.get')
    def test_get_order_details_by_order_id(self, mock_get):
        client = Pago46()
        mock_get.return_value = mock.MagicMock(
            headers={'content-type': 'application/json'}, status_code=200, response=json.dumps({'response': 'ok'}))
        order_id = 'a6a47f03-d0d3-446b-962d-caf3a7cebb30'
        response = client.get_order_details_by_order_id(order_id)

        self.assertEqual(response.status_code, 200)

    @mock.patch('pago46.client.requests.patch')
    def test_update_merchant_order_id(self, mock_patch):
        client = Pago46()
        mock_patch.return_value = mock.MagicMock(
            headers={'content-type': 'application/json'}, status_code=200, response=json.dumps({'response': 'ok'}))
        id = 'a6a47f03-d0d3-446b-962d-caf3a7cebb30'
        new_merchant_order_id = 'merchant_order_edited'
        response = client.update_merchant_order_id(id, new_merchant_order_id)

        self.assertEqual(response.status_code, 200)

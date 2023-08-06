import json
import unittest
import os
from unittest.mock import Mock, patch

from pyaxonaut import Customers


class TestCustomers(unittest.TestCase):

    def setUp(self):
        self._customers = Customers()
        with open(f"{os.path.dirname(os.path.realpath(__file__))}/fixtures/customers.json",
                  mode="r") as json_customers_fixture:
            self.json_customers = json.load(json_customers_fixture)
        with open(f"{os.path.dirname(os.path.realpath(__file__))}/fixtures/customer.json",
                  mode="r") as json_customer_fixture:
            self.json_customer = json.load(json_customer_fixture)

    def _mock_response(
            self,
            status=200,
            content="CONTENT",
            json_data=None,
            raise_for_status=None):
        mock_resp = Mock()
        # mock raise_for_status call w/optional error
        mock_resp.raise_for_status = Mock()
        if raise_for_status:
            mock_resp.raise_for_status.side_effect = raise_for_status
        # set status code and content
        mock_resp.status_code = status
        mock_resp.content = content
        # add json data if provided
        if json_data:
            mock_resp.json = Mock(
                return_value=json_data
            )
        return mock_resp

    @patch('pyaxonaut.customers.requests.post')
    def test_get_customers(self, mock_post):
        mock_resp = self._mock_response(json_data=self.json_customers)
        mock_post.return_value = mock_resp

        response = self._customers.get_customers()
        self.assertTrue(len(response) > 0)
        self.assertEqual(987654, response[0].company_id)
        self.assertEqual(987655, response[1].company_id)

    @patch('pyaxonaut.customers.requests.post')
    def test_get_customer_from_id(self, mock_post):
        mock_resp = self._mock_response(json_data=self.json_customer)
        mock_post.return_value = mock_resp

        customer = self._customers.get_customer(company_id="987654")
        self.assertEqual(987654, customer.company_id)

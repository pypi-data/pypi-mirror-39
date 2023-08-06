import requests

from pyaxonaut.constants import AXONAUT_API_CUSTOMERS_LIST, AXONAUT_API_BASE_URL, AXONAUT_API_CUSTOMER
from pyaxonaut.models.customer import Customer


class Customers:
    CUSTOMERS_URL = f"{AXONAUT_API_BASE_URL}/{AXONAUT_API_CUSTOMERS_LIST}"
    CUSTOMER_URL = f"{AXONAUT_API_BASE_URL}/{AXONAUT_API_CUSTOMER}"

    def __init__(self, api_key=None):
        self.api_key = api_key

    def get_customers(self):
        return list(map(Customer, self.request_customers_json()))

    def get_customer(self, company_id):
        return Customer(self.request_customer_json(company_id=company_id))

    def request_customers_json(self):
        resp = requests.post(self.CUSTOMERS_URL, data={
            "accountApiKey": self.api_key
        })
        return resp.json().get('arrayCompanies')

    def request_customer_json(self, company_id):
        resp = requests.post(self.CUSTOMER_URL, data={
            "accountApiKey": self.api_key,
            "companyId": company_id
        })
        return resp.json().get('arrayCompanies')[0]

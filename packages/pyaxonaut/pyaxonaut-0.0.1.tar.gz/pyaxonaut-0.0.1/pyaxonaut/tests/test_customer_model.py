import unittest

from ..models.customer import Customer


class TestCustomerModel(unittest.TestCase):

    def test_get_customer_from_json(self):
        json_customer = {
            "companyId": 123456,
            "name": "Test Company",
            "addressStreet": "3 Rabbit street",
            "addressZipCode": "1234",
            "addressTown": "Rabbit Town",
            "addressCountry": "Wonderland",
            "nbOpportunities": 12,
            "isProspect": True,
            "isCustomer": False,
            "isSupplier": False
        }
        customer = Customer(json_customer)
        self.assertEqual(json_customer.get("companyId"), customer.company_id)
        self.assertEqual(json_customer.get("name"), customer.company_name)
        self.assertEqual(json_customer.get("addressStreet"), customer.company_address_street)
        self.assertEqual(json_customer.get("addressZipCode"), customer.company_address_zip_code)
        self.assertEqual(json_customer.get("addressTown"), customer.company_address_town)
        self.assertEqual(json_customer.get("addressCountry"), customer.company_address_country)
        self.assertEqual(json_customer.get("nbOpportunities"), customer.nb_opportunities)
        self.assertEqual(json_customer.get("isProspect"), customer.is_prospect)
        self.assertEqual(json_customer.get("isCustomer"), customer.is_customer)
        self.assertEqual(json_customer.get("isSupplier"), customer.is_supplier)
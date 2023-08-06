class Customer:
    company_id = ""
    company_name = ""
    company_address_street = ""
    company_address_zip_code = ""
    company_address_town = ""
    company_address_country = ""
    nb_opportunities = 0
    is_prospect = False
    is_customer = False
    is_supplier = False

    def __init__(self, json_customer):
        self.company_id = json_customer.get('companyId')
        self.company_name = json_customer.get('name')
        self.company_address_street = json_customer.get('addressStreet')
        self.company_address_zip_code = json_customer.get('addressZipCode')
        self.company_address_town = json_customer.get('addressTown')
        self.company_address_country = json_customer.get('addressCountry')
        self.nb_opportunities = json_customer.get('nbOpportunities')
        self.is_prospect = json_customer.get('isProspect')
        self.is_customer = json_customer.get('isCustomer')
        self.is_supplier = json_customer.get('isSupplier')

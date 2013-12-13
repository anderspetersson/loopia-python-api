# -*- coding: utf-8 -*-
try:
    from xmlrpc import client as xmlclient # Python 3
except ImportError:
    import xmlrpclib as xmlclient # Python 2

from loopia.exceptions import DomainOccupiedError


class API(object):

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def call(self, method=None, args=[]):
        """
        Makes the call to the Loopia RPC Server.
        """

        client = xmlclient.ServerProxy(uri='https://test-api.loopia.se/RPCSERV', encoding='utf-8', allow_none=True)
        response = getattr(client, method)(self.username, self.password, *args)

        if response == 'OK':
            return True
        elif response == 'DOMAIN_OCCUPIED':
            raise DomainOccupiedError()
        else:
            return response

    def get_domains(self):
        """
        Get all domains for the current account.
        """

        return self.call(method='getDomains')

    def get_unpaid_invoices(self, with_vat=True):
        """
        Get all unpaid invoices.
        """

        return self.call(method='getUnpaidInvoices', args=[with_vat])


    def domain(self, domain=None):
        """
        Calls the Domain class with an instance of the API.

        Usage Example:
        >>> loopia = loopia.API('username', 'password')
        >>> domain = loopia.domain('google.com')
        >>> domain.is_free()
        False
        """

        return Domain(apiobj=self, domainname=domain)

    def invoice(self, reference_no=None, with_vat=True):
        """
        Calls the Invoice class with an instance of the API.
        """

        return Invoice(apiobj=self, reference_no=reference_no)


class Domain(API):
    """
    Base domain class, do stuff with domains.
    """

    def __init__(self, apiobj, domainname=None):
        self.domainname = domainname
        self.username = apiobj.username
        self.password = apiobj.password

    def is_free(self):
        """
        Check if a domain is availble to register.
        """

        try:
            return self.call(method='domainIsFree', args=[self.domainname])
        except DomainOccupiedError:
            return False


    def order(self, customer_number='', has_accepted_terms_and_conditions=0):
        """
        Order a domain.

        customer_number is optional and only used for resellers to
        set a customer for the domain.
        """

        return self.call(method='orderDomain', args=[customer_number, self.domainname, has_accepted_terms_and_conditions])


    def info(self):
        """
        Get info such as expiration date and registration status for a domain.
        """

        return self.call(method='getDomain', args=[self.domainname])


    def get_subdomains(self):
        """
        Get all subdomains for a domain.
        """

        return self.call(method='getSubdomains', args=[self.domainname])


    def get_zonerecords(self, subdomain=None):
        """
        Get zone records for a subdomain
        """

        return self.call(method='getZoneRecords', args=[self.domainname, subdomain])

    def add_zonerecord(self, subdomain=None, record_type=None, record_ttl=3600,
        record_priority=0, record_data=None):
        """
        Add a DNS record to a subdomain.
        """

        return self.call(method='addZoneRecord', args=[self.domainname, subdomain,
            {'type': record_type, 'ttl': record_ttl, 'priority': record_priority, 'rdata': record_data}])

class Invoice(API):
    """
    Handle invoices
    """

    def __init__(self, apiobj, reference_no=None, with_vat=True):
        self.reference_no = reference_no
        self.with_vat = with_vat
        self.username = apiobj.username
        self.password = apiobj.password

    def info(self):
        """
        Get info about an invoice, such as total to pay and expiry date.
        """

        self.call(method='getInvoice', args=[self.reference_no, self.with_vat])

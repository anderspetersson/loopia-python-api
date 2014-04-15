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

        client = xmlclient.ServerProxy(uri='https://api.loopia.se/RPCSERV', encoding='utf-8', allow_none=True)
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

        response = self.call(method='getDomains')
        domains = []
        for d in response:
            domain = self.domain(domain=d['domain'])
            domains.append(domain)
        return domains

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

    def subdomain(self, domain=None, subdomain=None):
        """
        Calls the Subdomain class with an instance of the API
        """

        return Subdomain(apiobj=self, domainname=domain, subdomain=subdomain)

    def zonerecord(self, domain=None, subdomain=None, record_type='A', \
        ttl=3600, priority=None, rdata=None):

        return ZoneRecord(apiobj=self, domainname=domain, subdomain=subdomain, record_type=record_type, \
            ttl=ttl, priority=priority, rdata=rdata)

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

    def __str__(self):
        return self.domainname

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
        Can only be used on domains in account.
        """

        return self.call(method='getDomain', args=[self.domainname])


    def get_subdomains(self):
        """
        Get all subdomains for a domain.
        """

        response = self.call(method='getSubdomains', args=[self.domainname])
        subdomains = []
        for s in response:
            subdomain = self.subdomain(domain=self.domainname, subdomain=s)
            subdomains.append(subdomain)
        return subdomains

    def add_subdomain(self, subdomain):
        """
        Add a subdomain to a domain.
        """

        self.subdomain(self.domainname, subdomain).create()

    def add_zonerecord(self, subdomain=None, record_type=None, record_ttl=3600,
        record_priority=0, record_data=None):
        """
        Add a DNS record to a subdomain.
        """

        return self.call(method='addZoneRecord', args=[self.domainname, subdomain,
            {'type': record_type, 'ttl': record_ttl, 'priority': record_priority, 'rdata': record_data}])

    def remove(self, deactivate=False):
        """
        Remove a domain from account, if deactivate is True, wait until the deactivation-date.
        """

        return self.call(method='removeDomain', args=[self.domainname, deactivate])


class Subdomain(API):
    """
    Handle subdomains.
    """

    def __init__(self, apiobj, domainname=None, subdomain=None):
        self.domainname = domainname
        self.subdomain = subdomain
        self.username = apiobj.username
        self.password = apiobj.password

    def __str__(self):
        return '%s.%s' % (self.subdomain, self.domainname)

    def create(self):
        """
        Add a subdomain to a domain.
        """

        return self.call(method='addSubdomain', args=[self.domainname, self.subdomain])

    def remove(self):
        """
        Remove a subdomain from a domain.
        """

        return self.call(method='removeSubdomain', args=[self.domainname, self.subdomain])

    def get_zonerecords(self):
        """
        Get all DNS records for a domain.
        """

        return self.call(method='getZoneRecords', args=[self.domainname, self.subdomain])

    def add_zonerecord(self, record_type='A', ttl=3600, priority=None, rdata=None):
        """
        Add a subdomain to a domain.
        """

        self.zonerecord(self.domainname, self.subdomain, record_type, ttl, priority, rdata).create()


class ZoneRecord(API):
    """
    Handle DNS records.
    """

    def __init__(self, apiobj, domainname, subdomain, record_id=None, record_type='A', \
                 ttl=3600, priority=None, rdata=None):
        self.domainname = domainname
        self.subdomain = subdomain
        self.record_id = record_id
        self.type = record_type
        self.ttl = ttl
        self.priority = priority
        self.rdata = rdata
        self.username = apiobj.username
        self.password = apiobj.password

    def __str__(self):
        return self.record_id

    def create(self):
        """
        Add a DNS entry to a (sub)domain.
        """

        record = {
                    'type': self.type,
                    'ttl': self.ttl,
                    'priority': self.priority,
                    'rdata': self.rdata
                 }

        self.call(method='addZoneRecord', args=[self.domainname, self.subdomain, record])


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

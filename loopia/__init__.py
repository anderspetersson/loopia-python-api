# -*- coding: utf-8 -*-
try:
    from xmlrpc import client as xmlclient  # Python 3
except ImportError:
    import xmlrpclib as xmlclient  # Python 2

from loopia.exceptions import DomainOccupiedError, UnknownError, AuthError, BadInDataError, RateLimitedError


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
        elif response == 'AUTH_ERROR':
            raise AuthError()
        elif response == 'DOMAIN_OCCUPIED':
            raise DomainOccupiedError()
        elif response == 'RATE_LIMITED':
            raise RateLimitedError()
        elif response == 'BAD_INDATA':
            raise BadInDataError()
        elif response == 'UNKNOWN_ERROR':
            raise UnknownError()
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

    def zonerecord(self, domain=None, subdomain=None, record_id=None, type='A',
                   ttl=3600, priority=None, rdata=None):

        return ZoneRecord(apiobj=self, domainname=domain, subdomain=subdomain,
                          record_id=record_id, type=type, ttl=ttl,
                          priority=priority, rdata=rdata)

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
        return str(self.domainname)

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

        return self.subdomain(self.domainname, subdomain).create()

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

        if self.call(method='addSubdomain', args=[self.domainname, self.subdomain]):
            return self

    def remove(self):
        """
        Remove a subdomain from a domain.
        """

        return self.call(method='removeSubdomain', args=[self.domainname, self.subdomain])

    def get_zonerecords(self):
        """
        Get all DNS records for a domain.
        """

        response = self.call(method='getZoneRecords', args=[self.domainname, self.subdomain])
        records = []
        for r in response:
            record = self.zonerecord(
                domain=self.domainname,
                subdomain=self.subdomain,
                record_id=r['record_id'],
                type=r['type'],
                ttl=r['ttl'],
                priority=r['priority'],
                rdata=r['rdata']
            )
            records.append(record)
        return records

    def add_zonerecord(self, type='A', ttl=3600, priority=None, rdata=None):
        """
        Add a DNS record to a subdomain.
        """

        return self.zonerecord(self.domainname, self.subdomain, type, ttl, priority, rdata).create()

    def remove_zonerecord(self, record_id=None, remove_all=False):
        """
        Remove all DNS entries for a subdomain or the one specified with record_id
        """

        if record_id:
            r = ZoneRecord(domainname=self.domainname, subdomain=self.subdomain, record_id=record_id)
            r.remove()
        elif remove_all:
            for r in self.get_zonerecords():
                r.remove()


class ZoneRecord(API):
    """
    Handle DNS records.
    """

    def __init__(self, apiobj, domainname, subdomain, record_id=None, type='A',
                 ttl=3600, priority=None, rdata=None):
        self.domainname = domainname
        self.subdomain = subdomain
        self.record_id = record_id
        self.type = type
        self.ttl = ttl
        self.priority = priority
        self.rdata = rdata
        self.username = apiobj.username
        self.password = apiobj.password

    def __str__(self):
        return '%s %s %s %s %s %d %d' % (
            str(self.record_id), self.subdomain, self.domainname, self.type,
            str(self.rdata), self.ttl, self.priority
        )

    def create(self):
        """
        Add a DNS entry to a subdomain.
        """

        record = {
            'type': self.type,
            'ttl': self.ttl,
            'priority': self.priority,
            'rdata': self.rdata,
        }

        if self.call(method='addZoneRecord', args=[self.domainname, self.subdomain, record]):
            return self

    def remove(self):
        """
        Remove a DNS entry from a subdomain.
        """

        self.call(method='removeZoneRecord', args=[self.domainname, self.subdomain, self.record_id])


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

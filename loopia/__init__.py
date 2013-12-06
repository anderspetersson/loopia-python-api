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

    def call(self, method=None, args=None):
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
            raise ValueError('Something whent wrong: %s' % response)


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


    def order(self, customer_number=None, has_accepted_terms_and_conditions=0):
        """
        Order a domain.

        customer_number is optional and only used for resellers to
        set a customer for the domain.
        """

        return self.call(method='orderDomain', args=[customer_number, self.domainname, has_accepted_terms_and_conditions])

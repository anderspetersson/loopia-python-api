# -*- coding: utf-8 -*-
try:
    from xmlrpc import client # Python 3
except ImportError:
    import xmlrpclib as client # Python 2


class API(object):

    def __init__(self, username, password, url='https://api.loopia.se/RPCSERV'):
        self.username = username
        self.password = password
        self.client = client.ServerProxy(uri=url, encoding='utf-8')

    def domain(self, domain=None):
        """
        Calls the Domain class with an instance of the API.

        Usage Example:
        loopia = loopia.API('username', 'password')
        domain = loopia.domain('google.com')
        domain.is_free()
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
        self.client = apiobj.client

    def is_free(self):
        """
        Check if a domain is availble to register.
        """

        response = self.client.domainIsFree(
            self.username,
            self.password,
            self.domainname
        )

        return response

    def order(self, customer_number=None, has_accepted_terms_and_conditions=0):
        """
        Order a domain.

        customer_number is optional and only used for resellers to
        set a customer for the domain.
        """

        response = self.client.orderDomain(
            self.username,
            self.password,
            self.domainname,
            customer_number,
            has_accepted_terms_and_conditions
        )

        return response


    def subdomains(self, customer_number=None):
        """
        List a domains subdomains.

        customer_number is optional and only used for resellers to
        set a customer for the domain.
        """

        response = self.client.getSubdomains(
            self.username,
            self.password,
            customer_number,
            self.domainname
        )

        return response

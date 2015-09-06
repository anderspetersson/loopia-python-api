import functools
import loopia
import pytest

TestAPI = functools.partial(loopia.API,
                            api_endpoint='https://api.loopia.se/RPCSERV')


def test_auth_error():
    api = TestAPI('abc', '123')
    with pytest.raises(loopia.exceptions.AuthError):
        api.get_domains()


def test_subclass_overrides():

    class MyDomain(loopia.Domain):
        pass

    class MySubdomain(loopia.Subdomain):
        pass

    class MyZoneRecord(loopia.ZoneRecord):
        pass

    class MyInvoice(loopia.Invoice):
        pass

    class MyAPI(loopia.API):
        domain_class = MyDomain
        subdomain_class = MySubdomain
        zonerecord_class = MyZoneRecord
        invoice_class = MyInvoice

    api = MyAPI('abc', '123')

    assert isinstance(api.domain(), MyDomain)
    assert isinstance(api.subdomain(), MySubdomain)
    assert isinstance(api.zonerecord(), MyZoneRecord)
    assert isinstance(api.invoice(), MyInvoice)

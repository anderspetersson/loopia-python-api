import functools
import loopia
import pytest

TEST_API_ENDPOINT = 'https://test-api.loopia.se/RPCSERV'
TestAPI = functools.partial(loopia.API, api_endpoint=TEST_API_ENDPOINT)


def test_api_endpoint_attribute():
    api = TestAPI('abc', '123')
    domain = api.domain()
    subdomain = api.subdomain()
    zonerecord = api.zonerecord()
    invoice = api.invoice()
    for obj in (api, domain, subdomain, zonerecord, invoice):
        obj.api_endpoint == TEST_API_ENDPOINT


def test_auth_error():
    api = TestAPI('abc', '123')
    domain = api.domain()
    subdomain = api.subdomain()
    zonerecord = api.zonerecord()
    invoice = api.invoice()
    for obj in (api, domain, subdomain, zonerecord, invoice):
        with pytest.raises(loopia.exceptions.AuthError):
            obj.get_domains()


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

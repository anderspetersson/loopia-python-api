import loopia


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

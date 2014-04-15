# -*- coding: utf-8 -*-


class DomainOccupiedError(Exception):
    """
    Error for when the domain is already registered.
    """

    def __str__(self):
        return 'The domain is already occupied.'

class UnknownError(Exception):
    """
    This get raised when the API dsnt know what went wrong.
    """

    def __str__(self):
        return 'Loopia returned an unknown response code.'
# -*- coding: utf-8 -*-


class DomainOccupiedError(Exception):
    """
    Error for when the domain is already registered.
    """

    def __str__(self):
        return 'The domain is already occupied.'
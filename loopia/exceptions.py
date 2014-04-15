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


class BadInDataError(Exception):
    """
    This gets raised when incorrect parameters gets sent to Loopia
    """

    def __str__(self):
        return 'Bad indata'


class AuthError(Exception):
    """
    This error gets raised when the username or password is incorrect.
    """

    def __str__(self):
        return 'Incorrect username or password.'


class RateLimitedError(Exception):
    """
    This exception raises when the user exceeds the maximum call rate limit from Loopia.
    """

    def __str__(self):
        return 'Rate Limit exceeded.'
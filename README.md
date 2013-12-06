Loopia
=================

A Python interface to loopia.se's API

Usage
================

        >>> import loopia
        >>> loopia = loopia.API('username', 'password')
        >>> domain = loopia.domain('google.com')
        >>> domain.is_free()
        False

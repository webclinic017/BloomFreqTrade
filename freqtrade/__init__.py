""" FreqTrade bot """
<<<<<<< HEAD
__version__ = '0.17.3'
=======
__version__ = '0.18.1-dev'
>>>>>>> 401de778114f0089eb0d394541efc5c3ea0eda82


class DependencyException(BaseException):
    """
    Indicates that a assumed dependency is not met.
    This could happen when there is currently not enough money on the account.
    """


class OperationalException(BaseException):
    """
    Requires manual intervention.
    This happens when an exchange returns an unexpected error during runtime
    or given configuration is invalid.
    """


class TemporaryError(BaseException):
    """
    Temporary network or exchange related error.
    This could happen when an exchange is congested, unavailable, or the user
    has networking problems. Usually resolves itself after a time.
    """

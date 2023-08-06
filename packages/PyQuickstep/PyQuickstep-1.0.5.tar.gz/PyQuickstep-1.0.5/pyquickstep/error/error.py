from pyquickstep.error.quicksteperror import QuickstepError


class Error(QuickstepError):
    """Exception that is the base class of all other error exceptions.
    You can use this to catch all errors with one single except statement.
    Warnings are not considered errors and thus should not use this class as base.
    It must be a subclass of the Python StandardError (defined in the module exceptions)."""
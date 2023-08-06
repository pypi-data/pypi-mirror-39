from pyquickstep.error.error import Error

class InterfaceError(Error):
    """Exception raised for errors that are related to the database interface rather
    than the database itself. It must be a subclass of Error."""

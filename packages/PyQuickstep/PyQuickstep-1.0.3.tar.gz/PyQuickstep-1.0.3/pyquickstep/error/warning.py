
from pyquickstep.error.quicksteperror import QuickstepError

class Warning(Warning, QuickstepError):
    """Exception raised for important warnings like data truncations
    while inserting, etc. It must be a subclass of the Python StandardError
    (defined in the module exceptions)."""
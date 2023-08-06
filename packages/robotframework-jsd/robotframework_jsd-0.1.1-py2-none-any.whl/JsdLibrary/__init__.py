from .jsd import JsdKeywords
from .version import VERSION

_version_ = VERSION


class JsdLibrary(JsdKeywords):
    """
    JsdLibrary is a JSD keyword library that uses to validate JSON
    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

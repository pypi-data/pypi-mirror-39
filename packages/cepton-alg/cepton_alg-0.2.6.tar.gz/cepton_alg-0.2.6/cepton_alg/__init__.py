from cepton_sdk import __author__  # noqa isort:skip
__version__ = "0.2.6"

import cepton_sdk.common

_all_builder = cepton_sdk.common.AllBuilder(__name__)


def __check_version():
    c_version = cepton_alg.c.get_version_string().split(".")[:2]
    version = __version__.split(".")[:2]
    if c_version != version:
        raise RuntimeError("Library versions do not match!")


try:
    import cepton_alg.c
    from cepton_alg.c import C_ErrorCode, C_Error, C_Warning
except:
    # Allow loading common
    pass
else:
    from cepton_alg.api import *
    from cepton_alg.core import *
    from cepton_alg.frame import *

    __check_version()

__all__ = _all_builder.get()

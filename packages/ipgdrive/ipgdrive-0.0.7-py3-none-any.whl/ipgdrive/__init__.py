"""ipgdrive code."""

from .core import (  # noqa: F401
    setup_job,
)

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

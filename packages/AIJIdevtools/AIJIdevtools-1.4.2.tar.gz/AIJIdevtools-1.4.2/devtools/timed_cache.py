# Compatibility for version < 1.1
from devtools.cache import timed_cache
from devtools.cli import warn

warn('module timed_cache is deprecated, use module cache instead.')

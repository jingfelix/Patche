import sys

if sys.version_info >= (3, 10):
    import importlib.metadata as importlib_metadata
else:
    import importlib_metadata


__version__ = importlib_metadata.version("Patche")

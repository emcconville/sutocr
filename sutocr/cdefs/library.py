from os import getenv
from abc import abstractmethod
import ctypes

__all__ = ('Library',)

class Library(object):
    def __init__(self, key=None, default=None):
        self.resource = None
        if key:
            self.find_lib(key, default)
        if self.resource:
            self.cdefs()

    def find_lib(self, key, default=None):
        candidates = getenv(key, default).strip()
        for candidate in candidates.split(';'):
            try:
                self.resource = ctypes.cdll.LoadLibrary(candidate.strip())
            except (IOError, OSError):
                continue
            return self.resource
        message = 'Unable to find {0} in {1} paths.'.format(key, candidates)
        raise IOError(message)

    @abstractmethod
    def cdefs(self):
        pass
from ctypes import POINTER, byref, cast, c_char_p, c_void_p
from .library import Library

DEFAULT_LEPT = """
liblept.so;
liblept.dylib;
/usr/local/lib/liblept.dylib
"""


class Leptonica(Library):
    def __init__(self,
                 key='SUTOCR_LEPTONICA',
                 default=DEFAULT_LEPT):
        Library.__init__(self, key, default)

    def pixRead(self, filename):
        return self.resource.pixRead(filename.encode())

    def pixDestroy(self, instance):
        self.resource.pixDestroy(byref(cast(instance, c_void_p)))

    def cdefs(self):
        self.resource.pixRead.argtypes = (c_char_p, )
        self.resource.pixRead.restype = c_void_p
        self.resource.pixDestroy.argtypes = (POINTER(c_void_p),)

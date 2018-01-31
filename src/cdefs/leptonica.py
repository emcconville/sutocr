from ctypes import c_char_p, c_void_p
from .library import Library

class Leptronica(Library):
    def __init__(self,
                 key='SUTOCR_LEPTONICA',
                 default='liblept.so'):
        Library.__init__(self, key, default)

    def cdefs(self):
        self.resource.pixRead.argtypes = (c_char_p, )
        self.resource.pixRead.restype = c_void_p
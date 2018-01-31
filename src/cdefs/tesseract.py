from ctypes import c_char_p, c_int, c_void_p
from .library import Library

class Tesseract(Library):
    def __init__(self,
                 key='SUTOCR_TESSERACT',
                 default='libtesseract.so'):
        Library.__init__(self, key, default)

    def cdefs(self):
        self.resource.TessBaseAPICreate.restype = c_void_p
        self.resource.TessBaseAPIDelete.argtypes = (c_void_p, )
        self.resource.TessBaseAPIInit3.argtypes = (c_void_p,
                                                   c_char_p,
                                                   c_char_p) 
        self.resource.TessBaseAPIInit3.restype = c_int
        self.resource.TessBaseAPISetImage2.argtypes = (c_void_p,
                                                       c_void_p) 
        self.resource.TessBaseAPIGetUTF8Text.argtypes = (c_void_p, )
        self.resource.TessBaseAPIGetUTF8Text.restype = c_char_p
        self.resource.TessBaseAPIEnd.argtypes = (c_void_p, ) 
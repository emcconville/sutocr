from ctypes import c_char_p, c_int, c_void_p
from .library import Library

DEFAULT_TESSERACT="""
libtesseract.so;
liblibtesseract.dylib;
/usr/local/lib/liblibtesseract.dylib;
"""

class TessBaseAPI(Library):
    def __init__(self,
                 key='SUTOCR_TESSERACT',
                 default=DEFAULT_TESSERACT):
        Library.__init__(self, key, default)
        if self.resource:
            self.api = self.resource.TessBaseAPICreate()

    def __del__(self):
        if self.resource:
            self.resource.TessBaseAPIDelete(self.api)

    def init(self, prop=None, lang='eng'):
        state = self.resource.TessBaseAPIInit3(self.api,
                                               prop,
                                               lang.encode())
        return state

    @property
    def image(self):
        return None # TODO
    @image.setter
    def image(self, pix):
        self.resource.TessBaseAPISetImage2(self.api, pix)

    @property
    def utf8_text(self):
        return self.resource.TessBaseAPIGetUTF8Text(self.api)

    def end(self):
        self.resource.TessBaseAPIEnd(self.api)

    def cdefs(self):
        self.resource.TessDeleteText.argtypes = (c_char_p, )
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
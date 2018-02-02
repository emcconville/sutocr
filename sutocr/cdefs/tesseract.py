from ctypes import cast, c_char_p, c_int, c_void_p
from os import getenv
from .library import Library

DEFAULT_TESSERACT = """
libtesseract.so;
liblibtesseract.dylib;
/usr/local/lib/liblibtesseract.dylib;
"""

DEFAULT_TESSERACT_LANG = getenv('SUTOCR_TESSERACT_LANG', 'eng')


class c_tess_char_p(c_void_p):
    """
    Char pointers allocated by library should be return to Tesseract Base API
    for deallocation. Failure to do so will result in memory leaks until
    Python's shutdown routine.
    """
    pass


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

    def init(self, prop=None, lang=DEFAULT_TESSERACT_LANG):
        state = self.resource.TessBaseAPIInit3(self.api,
                                               prop,
                                               lang.encode())
        return state

    def image(self, pix):
        self.resource.TessBaseAPISetImage2(self.api, pix)

    def utf8_text(self):
        response = self.resource.TessBaseAPIGetUTF8Text(self.api)
        result = None
        if response:
            result = cast(response, c_char_p).value
            self.resource.TessDeleteText(response)
        return result

    def end(self):
        self.resource.TessBaseAPIEnd(self.api)

    def cdefs(self):
        self.resource.TessDeleteText.argtypes = (c_tess_char_p, )
        self.resource.TessBaseAPICreate.restype = c_void_p
        self.resource.TessBaseAPIDelete.argtypes = (c_void_p, )
        self.resource.TessBaseAPIInit3.argtypes = (c_void_p,
                                                   c_char_p,
                                                   c_char_p)
        self.resource.TessBaseAPIInit3.restype = c_int
        self.resource.TessBaseAPISetImage2.argtypes = (c_void_p,
                                                       c_void_p)
        self.resource.TessBaseAPIGetUTF8Text.argtypes = (c_void_p, )
        self.resource.TessBaseAPIGetUTF8Text.restype = c_tess_char_p
        self.resource.TessBaseAPIEnd.argtypes = (c_void_p, )

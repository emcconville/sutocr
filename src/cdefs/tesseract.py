from ctypes import c_char_p, c_int, c_void_p
from .library import Library

class TessBaseAPI(Library):
    def __init__(self,
                 key='SUTOCR_TESSERACT',
                 default='libtesseract.so'):
        Library.__init__(self, key, default)
        self.api = self.resource.TessBaseAPICreate()

    def __del__(self):
        self.resource.TessBaseAPIDelete(self.api)

    def init(self, prop=None, lang='eng'):
        state = self.resource.TessBaseAPIInit3(self.api,
                                               prop,
                                               lang)
        return state

    @property
    def image(self):
        return None # TODO
    @image.setter
    def set_image(self, pix):
        self.resource.TessBaseAPISetImage2(self.api, pix)

    @property
    def utf8_text(self):
        response = self.resource.TessBaseAPIGetUTF8Text(self.api)

    def end(self):
        self.resource.TessBaseAPIEnd(self.api)

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
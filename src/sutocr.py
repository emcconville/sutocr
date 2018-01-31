from os import putenv, path
from glob import glob
from tempfile import TemporaryDirectory
from subprocess import Popen, PIPE
from cdefs.leptonica import Leptonica
from cdefs.tesseract import TessBaseAPI

def image_to_text(filepath):
    lept = Leptonica()
    tess = TessBaseAPI()
    tess.init()
    pix = lept.pixRead(filepath)
    if not pix:
        raise ValueError('Unable to open image `{0}\''.format(image))
    tess.image = pix
    results = tess.utf8_text
    lept.pixDestroy(pix)
    tess.end()
    return results

def pdf_to_text(filepath, gs_args=None):
    with TemporaryDirectory() as context:
        if not gs_args:
            gs_args = [
                'gs',
                '-sstdout=%stderr',
                '-dQUITE',
                '-dSAFER',
                '-dBATCH',
                '-dNOPAUS',
                '-dNOPROMPT',
                '-dMaxBitmap=500000000',
                '-dAlignToPixels=0',
                '-dGridFitTT=2',
                '-dBackgroundColor=16#FFFFFF',
                '-sDEVICE=jpeg',
                '-dTextAlphaBits=4',
                '-dGraphicsAlphaBits=4',
                '-r300x300',
                '-sOutputFile={0}'.format(path.join(context, 'output_%04d.jpg')),
                '-f{0}'.format(filepath)
            ]
        pid = Popen(gs_args, stdout=PIPE, stderr=PIPE)
        out, err = pid.communicate()
        for f in glob(path.join(context, 'output_*.jpg')):
            yield image_to_text(f)


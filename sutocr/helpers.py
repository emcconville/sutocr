from os import putenv, path
from glob import glob
from tempfile import TemporaryDirectory
from subprocess import Popen, PIPE
from sutocr.cdefs.leptonica import Leptonica
from sutocr.cdefs.tesseract import TessBaseAPI

def image_to_text(filepath):
    lept = Leptonica()
    tess = TessBaseAPI()
    tess.init()
    pix = lept.pixRead(filepath)
    if not pix:
        raise ValueError('Unable to open image `{0}\''.format(filepath))
    tess.image = pix
    results = tess.utf8_text
    lept.pixDestroy(pix)
    tess.end()
    return results

def pdf_to_text(filepath, *args, **kwargs):
    gs_args = [
        kwargs.get('binary','gs'),
        '-sstdout=%stderr',
        '-dQUIET',
        '-dSAFER',
        '-dBATCH',
        '-dNOPAUSE',
        '-dNOPROMPT',
        '-dMaxBitmap={0}'.format(kwargs.get('max_bitmap','500000000')),
        '-dAlignToPixels={0}'.format(kwargs.get('align_to_pixels','0')),
        '-dGridFitTT={0}'.format(kwargs.get('grid_fit_tt','2')),
        '-dBackgroundColor={0}'.format(kwargs.get('background_color',
                                                  '16#FFFFFF')),
        '-sDEVICE={0}'.format(kwargs.get('device','pngalpha')),
        '-dTextAlphaBits={0}'.format(kwargs.get('text_alpha_bits','4')),
        '-dGraphicsAlphaBits={0}'.format(kwargs.get('graphics_alpha_bits',
                                                    '4')),
        '-r{0}'.format(kwargs.get('resolution','300x300')),
    ] + list(*args)
    with TemporaryDirectory() as context:
        io = [
            '-sOutputFile={0}'.format(path.join(context, 'output_%04d')),
            '-f{0}'.format(filepath)
        ]
        pid = Popen(gs_args + io, stdout=PIPE, stderr=PIPE)
        out, err = pid.communicate()
        if pid.returncode:
            raise RuntimeError(str(err))
        for f in glob(path.join(context, 'output_*')):
            yield image_to_text(f)


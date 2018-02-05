"""
Shut UP & Tesseract OCR -- :mod:``sutocr.helpers``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A collection of simple functions to process documents with Tesseract OCR.

.. module:: sutocr.helpers
   :platform: Unix, macOS
   :synopsis: A no-thrill, featureless, Tesseract wrapper to convert PDF
              documents to text.

.. moduleauthor:: E. McConville <emcconville@emcconville.com>

"""
from os import path
from glob import glob
from tempfile import TemporaryDirectory
from subprocess import Popen, PIPE
from sutocr.cdefs.leptonica import Leptonica
from sutocr.cdefs.tesseract import TessBaseAPI

__all__ = ('image_to_text', 'pdf_to_text')


def image_to_text(filepath):
    """
    Evaluate ``filepath`` image, and attempt to extract text.

    Will return an empty string, or ``None``, if no characters were detected.
    Any library warnings, or errors, will be written to stderr.

    :param filepath: Real path of image to process with Tesseract-OCR.
                     The image's format must be supported by Leptonica library.
    :type filepath: :class:`str`
    :raises RuntimeError: if Tesseract library can not be initialized. This
                          usually occurs when train-data / language libraries
                          can not be loaded.
    :raises ValueError: if Leptonica can not process image. Either because the
                        ``filepath`` is not readable, or that the format is not
                        supported by library.
    :return: Characters detected within given image.
    :rtype: :class:`str`
    """
    lept = Leptonica()
    tess = TessBaseAPI()
    if tess.init():
        raise RuntimeError('Unable to initialize Tesseract library.')
    pix = lept.pixRead(filepath)
    if not pix:
        raise ValueError('Unable to open image `{0}\''.format(filepath))
    tess.image(pix)
    results = tess.utf8_text()
    lept.pixDestroy(pix)
    tess.end()
    return results


def pdf_to_text(filepath, *args, **kwargs):
    """Extract raster pages from a PDF document with Ghostscript, and pass
    to ``image_to_text`` function.

    :param filepath: Real path of document location.
    :type filepath: :class:`str`
    :rtype: Iterator[:class:`str`]
    """
    gs_args = [
        kwargs.get('binary', 'gs'),
        '-sstdout=%stderr',
        '-dQUIET',
        '-dSAFER',
        '-dBATCH',
        '-dNOPAUSE',
        '-dNOPROMPT',
        '-dMaxBitmap={0}'.format(kwargs.get('max_bitmap', '500000000')),
        '-dAlignToPixels={0}'.format(kwargs.get('align_to_pixels', '0')),
        '-dGridFitTT={0}'.format(kwargs.get('grid_fit_tt', '2')),
        '-dBackgroundColor={0}'.format(kwargs.get('background_color',
                                                  '16#FFFFFF')),
        '-sDEVICE={0}'.format(kwargs.get('device', 'pngalpha')),
        '-dTextAlphaBits={0}'.format(kwargs.get('text_alpha_bits', '4')),
        '-dGraphicsAlphaBits={0}'.format(kwargs.get('graphics_alpha_bits',
                                                    '4')),
        '-r{0}'.format(kwargs.get('resolution', '300x300')),
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
        pages = glob(path.join(context, 'output_*'))
        pages.sort()
        for f in pages:
            yield image_to_text(f)

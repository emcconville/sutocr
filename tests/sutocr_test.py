import sutocr

def test_image_to_text(sutocr_assets):
    filename = str(sutocr_assets.join('image_to_text.png'))
    actual = sutocr.image_to_text(filename).strip()
    expected = b'Shut Up & Tesseract OCR'
    assert expected == actual

def test_pdf_to_text(sutocr_assets):
    filename = str(sutocr_assets.join('pdf_to_text.pdf'))
    actual = [f.strip() for f in sutocr.pdf_to_text(filename)]
    expected = b'Shut Up Tesseract OCR'
    assert expected == b' '.join(actual)
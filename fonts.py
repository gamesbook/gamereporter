"""
Register a font or a font family. 
"""
import os
from reportlab.pdfbase import pdfmetrics 
from reportlab.pdfbase.ttfonts import TTFont 
from reportlab.pdfbase.pdfmetrics import registerFontFamily 

FONTS = '.local/share/fonts'
HOME = os.path.expanduser("~")
BASE = os.path.join(HOME, FONTS)

def ttf_register(name, family=False, base_dir=BASE):
    if not family:
        pdfmetrics.registerFont(TTFont(name,
        os.path.join(base_dir, '%s.ttf' % name)))
    else:
        pdfmetrics.registerFont(TTFont('%sR' % name,
            os.path.join(base_dir, '%s-Regular.ttf' % name)))
        pdfmetrics.registerFont(TTFont('%sI' % name,
            os.path.join(base_dir, '%s-Italic.ttf' % name)))
        pdfmetrics.registerFont(TTFont('%sBI' % name,
            os.path.join(base_dir, '%s-BoldItalic.ttf' % name)))
        pdfmetrics.registerFont(TTFont('%sB' % name,
            os.path.join(base_dir, '%s-Bold.ttf' % name)))
        registerFontFamily(
            '%s', normal='%sR' % name, bold='%sB' % name, italic='%sI' % name,
            boldItalic='%sBI' % name)
    
    """example:
    
    # http://www.1001freefonts.com/alegreya_sc.font
    pdfmetrics.registerFont(TTFont('AlegreyaSCR',
        os.path.join(base_dir, 'AlegreyaSC-Regular.ttf')))
    pdfmetrics.registerFont(TTFont('AlegreyaSCI',
        os.path.join(base_dir, 'AlegreyaSC-Italic.ttf')))
    pdfmetrics.registerFont(TTFont('AlegreyaSCBI',
        os.path.join(base_dir, 'AlegreyaSC-BoldItalic.ttf')))
    pdfmetrics.registerFont(TTFont('AlegreyaSCB',
        os.path.join(base_dir, 'AlegreyaSC-Bold.ttf')))
    registerFontFamily(
        'AlegreyaSC', normal='AlegreyaSCR', bold='AlegreyaSCB', italic='AlegreyaSCI',
        boldItalic='AlegreyaSCBI') 

    # http://www.1001freefonts.com/alegreya_sans_sc.font
    pdfmetrics.registerFont(TTFont('AlegreyaSansSCR',
        os.path.join(base_dir, 'AlegreyaSansSC-Regular.ttf')))
    pdfmetrics.registerFont(TTFont('AlegreyaSansSCI',
        os.path.join(base_dir, 'AlegreyaSansSC-Italic.ttf')))
    pdfmetrics.registerFont(TTFont('AlegreyaSansSCBI',
        os.path.join(base_dir, 'AlegreyaSansSC-BoldItalic.ttf')))
    pdfmetrics.registerFont(TTFont('AlegreyaSansSCB',
        os.path.join(base_dir, 'AlegreyaSansSC-Bold.ttf')))
    registerFontFamily(
        'AlegreyaSansSC', normal='AlegreyaSansSCR', bold='AlegreyaSansSCB', 
        italic='AlegreyaSansSCI', boldItalic='AlegreyaSansSCBI') 
    """


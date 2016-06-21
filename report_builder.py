#!/usr/bin/env python
"""
Author: Derek Hohls
Date: June 2016
Purpose:
    Generate a file (e.g. PDF or Excel) containing details of games (or game-
    like objects).  Basic layout is a table-per-game or a row-per-game.
Notes:
    Huge thanks to authors and developers of the following Python Libraries:
    * boardgamegeek
    * reportlab
    * xlwt
"""
# lib
from collections import OrderedDict
import json
import os
import sys
import time
# other
import xlwt
# reportlab
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_RIGHT, TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch, cm
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import black, white, slategray, slategrey, \
    lightgrey, lightslategray, lightslategrey, \
    red
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, \
    TableStyle, Image

FONTS = '.local/share/fonts'  # path for Ubuntu Linux
HOME = os.path.expanduser("~")
BASE = os.path.join(HOME, FONTS)


class GameReportBuilder(object):

    def __init__(self, *args, **kwargs):
        __version_info__ = ('1', '0', '0')
        self.__version__ = __version__
        self.games = kwargs.get('games', [])  # list of 'game' objects
        self.user = kwargs.get('user', '')
        self.time = kwargs.get('time', 'UK')
        self.filename = kwargs.get('filename')
        self.progress = kwargs.get('progress', False)
        self.family_names = kwargs.get('familys', [])
        self.font_names = kwargs.get('fonts', [])
        self.page_footer = kwargs.get(
            'page_footer', '')
        self.page_header = kwargs.get(
            'page_header', 'Board Game Geek Collection Printer (v0.1)')
        header = kwargs.get('header')
        body = kwargs.get('left')
        margin = kwargs.get('margin', 72)
        page_size = kwargs.get('page', 'A4')
        if page_size == 'A4':
            size = A4
        elif page_size == 'letter':
            size = Letter
        else:
            raise NotImplementedError('Page size "%" is not available' % page_size)
        self.set_doc(filename=self.filename, margin=margin, page=size)
        # fonts & styles
        for fname in self.family_names:
            self.ttf_register(fname, family=True)
        for fname in self.font_names:
            self.ttf_register(fname, family=False)
        self.styles = getSampleStyleSheet()
        self.set_styles(body, header)  # style sheets pre-made

    def ttf_register(self, name, family=False, base_dir=BASE):
        """
        Register a font or a font family.

        Example:

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
            'AlegreyaSC', normal='AlegreyaSCR', bold='AlegreyaSCB',
            italic='AlegreyaSCI', boldItalic='AlegreyaSCBI')

        Note:
            Acrobat PDF has 14 built-in fonts, supported by reportlab:
            Courier, Helvetica, Courier-Bold, Helvetica-Bold, Courier-Oblique,
            Helvetica-Oblique, Courier-BoldOblique, Helvetica-BoldOblique,
            Times-Roman, Times-Bold, Times-Italic, Times-BoldItalic, Symbol,
            ZapfDingbats
        """
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
                '%s', normal='%sR' % name, bold='%sB' % name,
                italic='%sI' % name, boldItalic='%sBI' % name)

    def set_doc(self, filename, margin=72, page=A4):
        _filename = filename or 'games.pdf'
        self.doc = SimpleDocTemplate(
            _filename,
            rightMargin=margin,
            leftMargin=margin,
            topMargin=margin,
            bottomMargin=margin,
            pagesize=page)

    def set_styles(self, body, header):
        """
        Make styles available to printing routines.
        """
        body = body or 'Times'
        header = header or 'Helvetica'
        page_header = 'Helvetica'
        page_footer = 'Helvetica'
        try:
            # body
            self.styles.add(ParagraphStyle(
                name='right',
                fontName=body,
                alignment=TA_RIGHT))
            self.styles.add(ParagraphStyle(
                name='left',
                fontName=body,
                alignment=TA_LEFT))
            self.styles.add(ParagraphStyle(
                name='centre',
                fontName=body,
                alignment=TA_CENTER))
            # header
            self.styles.add(ParagraphStyle(
                name='CentreHeader',
                fontName=header,
                fontSize=14,
                spaceBefore=3,
                spaceAfter=4,
                alignment=TA_CENTER))
            self.styles.add(ParagraphStyle(
                name='info',
                fontName=header,
                alignment=TA_LEFT)),
            # page_...
            self.styles.add(ParagraphStyle(
                name='page_header',
                fontName=page_header,
                fontSize=8,
                spaceAfter=6,
                alignment=TA_LEFT)),
            self.styles.add(ParagraphStyle(
                name='page_footer',
                fontName=page_footer,
                fontSize=9,
                alignment=TA_RIGHT))
        except ValueError:
            print "Unable to use or access the custom fonts!"
            sys.exit(1)

    def get_image(self, game, path, width=1*cm, height=None):
        """
        Create an image from a path - either on on disc or from a web URL.
        """
        if self.progress:
            print "Retrieving image for game: %7d" % int(game.id)
        img = ImageReader(path)
        iw, ih = img.getSize()
        aspect = ih / float(iw)
        if height:
            return Image(path, width=(height * aspect), height=height)
        else:
            return Image(path, width=width, height=(width * aspect))

    def set_header_footer(self, canvas, doc):
        """
        Set header and footer on each page; default is NO header and footer with
        a page no.
        """
        # Save canvas
        canvas.saveState()
        page_num = canvas.getPageNumber()
        # Header
        if self.page_header:
            header = Paragraph(self.page_header, self.styles['page_header'])
            w, h = header.wrap(doc.width, doc.topMargin)
            header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h)
        # Footer
        _footer = self.page_footer or "Pg. %s" % page_num
        footer = Paragraph(_footer, self.styles['page_footer'])
        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin, h)
        # Release the canvas
        canvas.restoreState()

    def create_json(self):
        """
        Create a JSON file containing games' details; entries keyed on game ID
        """
        game_list = {}
        for number, game in enumerate(self.games):
            game_list[int(game.id)] = game.__dict__
        dump = json.dumps(game_list, indent=2, default=str)
        _file = open(self.filename, 'w')
        print >> _file, dump
        _file.close()

    def create_xls(self):
        """
        Create an XLS spreadsheet displaying games' details; one game per row
        """
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet("Summary")
        sheet.col(0).width = 256 * 60
        bold_style = xlwt.easyxf('font: bold 1')
        _items = (
            ('Name', 'name'),
            ('ID', 'id'),
            ('Weight', 'averageweight'),
            ('% Weight', 'percentageweight'),
            ('Year', 'yearpublished'),
            ('Age', 'age'),
            ('Time', 'playingtime'),
            ('Min.', 'minplayers'),
            ('Max', 'maxplayers'),
            ('Mechanics', 'mechanics'),
            ('Categories', 'categories'),
        )
        items = OrderedDict(_items)
        for col, head in enumerate(items.keys()):
            sheet.write(0, col, head, bold_style)
        for number, game in enumerate(self.games):
            if self.progress:
                print "Creating the row for game: %7d" % int(game.id)
                for col, head in enumerate(items.keys()):
                    sheet.write(number + 1, col, getattr(game, items[head]))
        workbook.save(self.filename)

    def create_table_summary(self, game, num):
        """
        Create a reportlab table displaying summarised game information.

        Args:
            game: object
                a BGGGame object (or similar) whose properties correspond to
                game attributes e.g. name, description
        """
        if self.progress:
            print "Generating summary table for game: %7d" % int(game.id)
            print "Generating a summary row for game: %7d" % int(game.id)
        div = self.doc.width / 7.0
        table_data = [
            [
                Paragraph('<b>%s</b>' % game.name, self.styles['left']),
                Paragraph('<b>%s (%s)</b>' %
                          (game.averageweight, game.percentageweight),
                          self.styles['left']),
                Paragraph('<b>%s</b>' % game.yearpublished, self.styles['left']),
                Paragraph('<b>%s</b>' % game.age, self.styles['left']),
                Paragraph('<b>%s</b>' % game.playingtime, self.styles['left']),
                Paragraph('<b>%s</b>' % game.players, self.styles['left']),
            ]
        ]
        if num == 0:
            table_data.insert(0,
                [
                    Paragraph('<b>Name</b>', self.styles['info']),
                    Paragraph('<b>Weight (%)</b>', self.styles['left']),
                    Paragraph('<b>Year</b>', self.styles['left']),
                    Paragraph('<b>Age</b>', self.styles['left']),
                    Paragraph('<b>Time</b>', self.styles['left']),
                    Paragraph('<b>Players</b>', self.styles['left']),
                ]
            )
        # create the table
        game_table = Table(table_data,
                           colWidths=[div*2, div, div, div, div, div])
        game_table.setStyle(
            TableStyle([
                        ('BOX', (0, 0), (-1, -1), 0.5, black),
                        ('VALIGN',(0,0), (-1,-1), 'TOP'),
                       ]),
                      )
        return game_table

    def create_table_compact(self, game):
        """
        Create a compact reportlab table displaying game information.

        Args:
            game: object
                a BGGGame object (or similar) whose properties correspond to
                game attributes e.g. name, description
        """
        if self.progress:
            print "Generating table for game: %7d" % (int(game.id))
        div = self.doc.width / 7.0
        HT = 0.6 * cm
        # note that 'n' in div * n MUST correspond to number of cols spanned
        if 'geekdo-images' in game.image:
            _image = game.image.replace('.jpg', '_sq.jpg').replace('.png', '_sq.png')
        else:
            _image = game.image
        game_image = self.get_image(game, path=_image, height=HT*3 - 8)
        table_data = [
            [
                game_image,
                Paragraph('<b>%s</b>' % game.name, self.styles['info']),
                '', '',
                Paragraph('<b>%s</b>' % game.age, self.styles['centre']),
                Paragraph('<b>%s</b> min' % game.playingtime, self.styles['centre']),
                Paragraph('<b>%s</b> players' % game.players, self.styles['right'])
            ],
            [
                '', Paragraph('%s' % game.mechanics, self.styles['left']),
                '', '', '', '', ''
            ],
            [
                '', Paragraph('%s' % game.categories, self.styles['left']),
                '', '', '', '', ''
            ]
        ]
        # create the table
        game_table = Table(table_data,
                           colWidths=[div, div, div, div, div, div, div],
                           rowHeights=[HT] * len(table_data))
        game_table.setStyle(
            TableStyle([
                        ('BOX', (0, 0), (-1, -1), 0.5, black),
                        ('VALIGN',(0,0), (-1,-1), 'TOP'),
                        ('SPAN',(0,0),(0,2)),
                        ('SPAN',(1,0),(3,0)),
                        ('SPAN',(1,1),(6,1)),
                        ('SPAN',(1,2),(6,2)),
                       ]),
                      )
        return game_table


    def create_table(self, game):
        """
        Create a reportlab table displaying game information.

        Args:
            game: object
                a BGGGame object (or similar) whose properties correspond to
                game attributes e.g. name, description
        """
        if self.progress:
            print "Generating table for game: %7d" % int(game.id)
        div = self.doc.width / 8.0
        # note that 'n' in div * n MUST correspond to number of cols spanned
        if 'geekdo-images' in game.image:
            _image = game.image.replace('.jpg', '_md.jpg').replace('.png', '_md.png')
        else:
            _image = game.image
        game_image = self.get_image(game, path=_image, width=div * 3 - 9)
        table_data = [
            [
                Paragraph('<b>Ages</b>: %s' % game.age,
                          self.styles['info']),
                '',
                Paragraph('<b>Published</b>: %s' % game.yearpublished,
                          self.styles['info']),
                '',
                Paragraph('<b>Time</b>: %s min' % game.playingtime, self.styles['info']),
                '',
                Paragraph('<b>Players</b>: %s' % game.players, self.styles['info']),
                ''
            ],
            [
                Paragraph('<b>Categories</b>: %s' % game.categories, self.styles['info']),
                '', '', '', '', '', '', ''
            ],
            [
                Paragraph('<b>Mechanics</b>: %s' % game.mechanics, self.styles['info']),
                '', '', '', '', '', '', ''
            ],
            [
                Paragraph(game.description_html, self.styles['left']),
                '', '', '', '',
                game_image,
                '', ''
            ]
        ]
        # create the table
        game_table = Table(table_data,
                           colWidths=[div, div, div, div, div, div, div, div])
        game_table.setStyle(
            TableStyle([
                        ('BOX', (0, 0), (-1, -1), 0.5, black),
                        ('VALIGN',(0,0), (-1,-1), 'TOP'),
                        ('SPAN',(0,0),(1,0)),
                        ('SPAN',(2,0),(3,0)),
                        ('SPAN',(4,0),(5,0)),
                        ('SPAN',(6,0),(7,0)),
                        ('SPAN',(0,1),(7,1)),
                        ('SPAN',(0,2),(7,2)),
                        ('SPAN',(0,3),(4,3)),
                        ('SPAN',(5,3),(7,3)),
                       ]),
                      )
        return game_table

    def create_qr(self, ID, width=2*cm, prefix=None, suffix=None):
        """
        Generate QR image for a (default) BGG game
        """
        server = 'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data='
        _prefix = prefix or 'https://boardgamegeek.com/boardgame/'
        _suffix = suffix or ''
        url = '%s%s%s%s' % (server, prefix, ID, suffix)
        img = self.get_image(url, width)
        return img

    def save_games(self, style='full'):
        """
        Primary routine to drive creation of a reportlab PDF.

        Elements such as paragraphs & tables are collated in a list; and then
        the document is created.

        Headers and Footer are set via the doc.build().
        """
        elements = []
        if style in ['summary', 'compact']:
            elements.append(Spacer(1, 0.5*cm))
        # All done!
        if style in ['full', 'compact', 'summary']:
            # Create table per game
            for number, game in enumerate(self.games):
                if style == 'full':
                    gtable = self.create_table(game)
                    header = Paragraph('<b>%s</b>' % game.name,
                                       self.styles['CentreHeader'])
                    header.keepWithNext = True
                    elements.append(header)
                    elements.append(gtable)
                elif style == 'compact':
                    gtable = self.create_table_compact(game)
                    elements.append(gtable)
                elif style == 'summary':
                    gtable = self.create_table_summary(game, number)
                    elements.append(gtable)
            # After tables
            elements.append(Spacer(1, 0.5*cm))
            if self.time == 'US':
                _date = time.strftime("%b %d, %Y %H:%M")
            else:
                _date = time.strftime("%Y-%m-%d %H:%M")
            p2 = Paragraph('Printed at %s' % _date, self.styles['right'])
            elements.append(p2)
            if self.progress:
                print "Generating PDF Document... ... .."
            self.doc.build(
                elements,
                onFirstPage=self.set_header_footer,
                onLaterPages=self.set_header_footer)
        elif style == 'excel':
            print "Generating XLS Spreadsheet ... ..."
            self.create_xls()
        elif style == 'json':
            print "Generating a JSON File ... ... ..."
            self.create_json()
        else:
            print 'The style "%s" does not exist!' % style
            sys.exit(1)
# -*- coding: utf-8 -*-
# Copyright (C) 2016-TODAY touch:n:track <https://tnt.pythonanywhere.com>
# Part of tnt: Product XLS Import addon for Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api

from io import StringIO
from csv import DictReader

import csv

import base64
import xlrd

import logging
_logger = logging.getLogger(__name__)

class XlsImport(models.TransientModel):
    _name = "tnt.xls.import"
    _description = "Product XLS Import"

    xls_file = fields.Binary(
        "XLS File",
        required=True,
        help="Upload an XLS file.",
    )
    xls_filename = fields.Char("Filename")
    line_ids = fields.One2many('tnt.xls.import.lines',
                               'tnt_xls_import_id',
                               'Product XLS Import Lines')

    @api.onchange('xls_file')
    def _onchange_xls_file(self):
        if not self.xls_file:
            return False

        lines = self.env['tnt.xls.import.lines']

        if '.txt' in self.xls_filename:
            file = base64.b64decode(self.xls_file)
            data = StringIO(file.decode("utf-8"))
            data.seek(0)
            reader = csv.reader(data, delimiter='\t')
            for i, cols in enumerate(reader):
                if not cols[0] == "id":
                    _logger.info('import line: {}'.format(i))
                    lines.create({
                        'tnt_xls_import_id': self.id,
                        'ref_id': cols[0],
                        'name': cols[1],
                        'categ_id': cols[8],
                        'brand_id': cols[41],
                        'catalog_auto_model': cols[48],
                    })
        elif '.xls' in self.bunning_filename or '.xlsx' in self.bunning_filename:
            book = xlrd.open_workbook(
                file_contents=base64.decodebytes(self.xls_file)
            )
            sheet = book.sheet_by_index(0)
            for row in range(1, sheet.nrows):
                cols = []
                for col in range(sheet.ncols):
                    cols.append(sheet.cell(row, col).value)
                lines.create({
                    'tnt_xls_import_id': self.id,
                    'ref_id': cols[0],
                    'name': cols[1],
                    'categ_id': cols[8],
                    'brand_id': cols[41],
                    'catalog_auto_model': cols[48],
                })
        else:
            raise ValueError("Wrong file extension.")

    def xls_import_button(self):
        product_template = self.env['product.template'].sudo()
        for i, line in enumerate(self.line_ids):
            _logger.info('create line: {}'.format(i))
            product_template.create([{
                'name': line.name,
                'xls_id': line.ref_id,
                'xls_name': line.name,
                'xls_categ_id': line.categ_id,
                'xls_brand_id': line.brand_id,
                'xls_catalog_auto_model': line.catalog_auto_model,
            }])


class XlsImportLines(models.TransientModel):
    _name = "tnt.xls.import.lines"

    tnt_xls_import_id = fields.Many2one('tnt.xls.import', 'XLS Import')

    ref_id = fields.Char('id')
    name = fields.Char('name')
    categ_id = fields.Char('categ_id')
    brand_id = fields.Char('brand_id')
    catalog_auto_model = fields.Char('catalog_auto_model')

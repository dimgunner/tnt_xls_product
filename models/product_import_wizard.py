# -*- coding: utf-8 -*-
# Copyright (C) 2016-TODAY touch:n:track <https://tnt.pythonanywhere.com>
# Part of tnt: Product XLS Import addon for Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api

import base64
import xlrd


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

        if '.xls' in self.xls_filename or '.xlsx' in self.xls_filename:
            book = xlrd.open_workbook(
                file_contents=base64.decodebytes(self.xls_file)
            )
            sheet = book.sheet_by_index(0)
            rows = []
            for row in range(sheet.nrows):
                cols = []
                for col in range(sheet.ncols):
                    cols.append(sheet.cell(row, col).value)
                rows.append(cols)
        else:
            raise ValueError("Wrong file extension.")

        lines = self.env['tnt.xls.import.lines']
        for row in rows[1:]:
            lines.create({
                'tnt_xls_import_id': self.id,
                'name': row[1],
                'categ_id': row[8],
                'brand_id': row[32],
                'catalog_auto_model': row[48],
            })

    def xls_import_button(self):
        product_template = self.env['product.template'].sudo()
        for line in self.line_ids:
            product_template.create([{
                'name': line.name,
                'xls_name': line.name,
                'xls_categ_id': line.categ_id,
                'xls_brand_id': line.brand_id,
                'xls_catalog_auto_model': line.catalog_auto_model,
            }])


class XlsImportLines(models.TransientModel):
    _name = "tnt.xls.import.lines"

    tnt_xls_import_id = fields.Many2one('tnt.xls.import', 'XLS Import')

    name = fields.Char('name')
    categ_id = fields.Char('categ_id')
    brand_id = fields.Char('brand_id')
    catalog_auto_model = fields.Char('catalog_auto_model')

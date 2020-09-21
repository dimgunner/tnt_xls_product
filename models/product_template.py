# -*- coding: utf-8 -*-
# Copyright (C) 2016-TODAY touch:n:track <https://tnt.pythonanywhere.com>
# Part of tnt: Product XLS Import addon for Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    xls_name = fields.Char('name')
    xls_categ_id = fields.Char('categ_id')
    xls_brand_id = fields.Char('brand_id')
    xls_catalog_auto_model = fields.Char('catalog_auto_model')

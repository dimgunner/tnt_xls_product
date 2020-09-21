# -*- coding: utf-8 -*-
# Copyright (C) 2016-TODAY touch:n:track <https://tnt.pythonanywhere.com>
# Part of tnt: Product XLS Import addon for Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "tnt: Product XLS Import",

    'summary': """
Product XLS Import
    """,

    'description': """
Import Products from XLS File
    """,

    'author': "touch:n:track",
    'website': "https://tnt.pythonanywhere.com/",
    'category': 'Operations/Purchase',
    'version': '0.1',

    'depends': [
        'purchase',
    ],

    'data': [
        'views/product_template_view.xml',
        'views/product_import_wizard_view.xml',
    ],

    'installable': True,
    'auto_install': False,
}

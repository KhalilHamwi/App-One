# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'App One',
    'author': "Real_Project Hamwi",
    'version': '17.0.1.0',
    'summary': 'Invoices & Payments',
    'category': '',
    'website': '',
    'depends': ['base', 'sale_management', 'account', 'mail', 'contacts'],
    'data': [
        "security/ir.model.access.csv",
        'views/base_menu.xml',
        'views/property_views.xml',
        'views/owner.xml',
        'views/tag.xml',
        'views/sale_order.xml',
        'views/res_partner.xml',
        'reports/property_report.xml',
    ],
    'assets' : {
        'web.assets_backend':['app_one\static\src\css\property.css']

},

'application': True, }

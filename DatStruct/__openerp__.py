# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Data Struct ERP ',
    'version': '1.0',
    'category': 'Sales Management',
    'sequence': 14,
    'summary': 'Data Struct ERP',
    'description': """
Manage sales quotations and orders
==================================

This application allows you to manage your Day by Day processes easily    """,
    'author': 'DataStruct',
    'website': 'http://www.datstruct.com/',
    'depends': ['sale','account','stock', 'purchase'],
    'data': [
        'views/manufacture_procurement_view.xml', 
        'views/saleorder_view.xml',
        'views/invoice_view.xml',
        'views/purchase_view.xml',
        'views/res_partner_view.xml',
        'views/product_view.xml',
        'views/crm_lead.xml',
        'views/menu.xml',
        'wizard/procurement_order_group_view.xml',
        'data/data.xml', 
        'report/sale_order_report.xml',
        'report/account_invoice_report.xml',
        'report/purchase_order_report.xml',
        'report/reports.xml',

             
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

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
import time

from openerp.osv import fields, osv
from openerp.tools.translate import _

class procurement_order_group(osv.osv_memory):
    _name = "procurement.order.group"
    _description = "Procurement Request Merge"

    def fields_view_get(self, cr, uid, view_id=None, view_type='form',
                        context=None, toolbar=False, submenu=False):
        """
         Changes the view dynamically
         @param self: The object pointer.
         @param cr: A database cursor
         @param uid: ID of the user currently logged in
         @param context: A standard dictionary
         @return: New arch of view.
        """
        if context is None:
            context={}
        res = super(procurement_order_group, self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type, context=context, toolbar=toolbar,submenu=False)
        if context.get('active_model','') == 'manufacture.procurement' and len(context['active_ids']) < 2:
            raise osv.except_osv(_('Warning!'),
            _('Please select multiple order to merge in the list view.'))
        return res
    def merge_orders(self, cr, uid, ids, context=None):
        """
             To merge similar type of purchase orders.

             @param self: The object pointer.
             @param cr: A database cursor
             @param uid: ID of the user currently logged in
             @param ids: the ID or list of IDs
             @param context: A standard dictionary

             @return: purchase order view

        """
        if context.get('active_model','') :
            self.pool.get(context.get('active_model','')).merge_procurment(cr, uid,context.get('active_ids',[]))

        return True 


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

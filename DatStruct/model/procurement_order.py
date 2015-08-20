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

from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp import netsvc
from openerp import pooler
from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from openerp import tools

class procurement_order(osv.osv):
    _inherit = 'procurement.order'


    def _procure_orderpoint_confirm(self, cr, uid, automatic=False, company_id=False ,use_new_cursor=False, context=None, user_id=False):
        '''
        Create manufacture procurement based on Orderpoint
        use_new_cursor: False or the dbname

        @param self: The object pointer
        @param cr: The current row, from the database cursor,
        @param user_id: The current user ID for security checks
        @param context: A standard dictionary for contextual values
        @param param: False or the dbname
        @return:  Dictionary of values
        """
        '''
        if context is None:
            context = {}
        if use_new_cursor:
            cr = pooler.get_db(use_new_cursor).cursor()
        orderpoint_obj = self.pool.get('stock.warehouse.orderpoint')
        procurement_obj = self.pool.get('manufacture.procurement')
        offset = 0
        ids = [1]
        if automatic:
            self.create_automatic_op(cr, uid, context=context)
        while ids:
            ids = orderpoint_obj.search(cr, uid, [], offset=offset, limit=100)
            for op in orderpoint_obj.browse(cr, uid, ids, context=context):
                prods = self._product_virtual_get(cr, uid, op)

                if prods < op.product_min_qty:
                    req_qty = max(op.product_min_qty, op.product_max_qty)-prods

                    reste = req_qty % op.qty_multiple
                    if reste > 0:
                        req_qty += op.qty_multiple - reste

                    if req_qty <= 0:
                        continue
 
                    all_procurement_ids = procurement_obj.search(cr, uid, [('product_id', '=', op.product_id.id), ('state', 'in', ('draft', 'confirmed'))], context=context)
                    generated_qty = 0
                    for procurement in procurement_obj.browse(cr, uid, all_procurement_ids, context=context):
                        generated_qty += procurement.product_qty

                    if generated_qty >= req_qty:
                        continue

                    req_qty -= generated_qty
                    proc_id = procurement_obj.create_procurement(cr, uid, op.product_id.id, req_qty, op.id, context=context)

            offset += len(ids)
            if use_new_cursor:
                cr.commit()
        if use_new_cursor:
            cr.commit()
            cr.close()
        return {}

procurement_order()




class stock_warehouse_orderpoint(osv.osv):
    """
    overrided to fix multicompany warehouse bug.
    """
    _inherit = 'stock.warehouse.orderpoint'


    def _get_warehouse(self, cr, uid, context=None):
        """
            returns the default warehouse 
            id of the users current company
        """
        warehouse_id = self.pool.get('stock.warehouse').search(cr, uid, [], context=context, limit=1)
        if warehouse_id:
            return warehouse_id and warehouse_id[0]
        else:
            raise osv.except_osv(_('Invalid Action!'), _('Please create a warehouse for this company.'))


    _defaults = {
                'warehouse_id': lambda self, cr, uid, context: self._get_warehouse(cr, uid, context=context),
        
                }
    


    def default_get(self, cr, uid, fields, context=None):
        """
            core module bug fix
            description: presetted warehouse_id 
            getting removed from fields list for create.   
        """
        if 'warehouse_id' not in fields:
            fields.append('warehouse_id')
        return super(stock_warehouse_orderpoint, self).default_get(cr, uid, fields, context)




stock_warehouse_orderpoint()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

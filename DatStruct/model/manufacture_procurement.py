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

from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
import datetime

# Manufacture Procurement
# ------------------------------------------------------------------
#
# Generate procurement orders from 
# Manufacturing Portal Users
#  



class manufacture_procurement(osv.osv):
    """
    Manufacture Procurements
    """
    _name = "manufacture.procurement"
    _description = "Manufacture Procurement"
    _inherit = ['mail.thread']

    _columns = {
        
        'name': fields.char('Name'),
        'partner_id':fields.many2one('res.partner','Supplier', domain=[('supplier','=',True)]),
        'description': fields.text('Description'),
        'date_generated': fields.date('Generated date', required=True, select=True),
        'date_close': fields.date('Closing Date'),
        'product_id': fields.many2one('product.product', 'Product', required=True, readonly=True),
        'product_qty': fields.float('Quantity', required=True, states={'draft':[('readonly',False)]}, readonly=True),
        'state': fields.selection([
            ('draft','Draft'),
            ('cancel', 'Cancel'),
            ('done','Done'),], 'Status', required=True, track_visibility='onchange'),
        'company_id': fields.many2one('res.company','Company',required=True),
        'orderpoint_id': fields.many2one('stock.warehouse.orderpoint', 'Orderpoint'),
        'active': fields.boolean('Active'),
    }

    _defaults = {
        'state': 'draft',
        'date_generated': fields.date.context_today,
        'company_id': lambda self, cr, uid, c: self.pool.get('res.company')._company_default_get(cr, uid, 'procurement.order', context=c)
    }



    def button_cancel(self, cr, uid, ids, context=None):
        for proc in self.browse(cr, uid, ids, context=context):
            proc.write({'state':'cancel'})
        return True



    def unlink(self, cr, uid, ids, context=None):
        procurements = self.read(cr, uid, ids, ['state'], context=context)
        unlink_ids = []
        for s in procurements:
            if s['state'] in ['draft','cancel']:
                unlink_ids.append(s['id'])
            else:
                raise osv.except_osv(_('Invalid Action!'),
                        _('Cannot delete Procurement Order(s) which are in %s state.') %s['state'])
        return osv.osv.unlink(self, cr, uid, unlink_ids, context=context)


    def create_procurement(self, cr, uid, product_id, quantity, orderpoint_id, context=None):
        supplierinfo = self.pool.get('product.supplierinfo')
        supplier = False
        product_brw = self.pool.get('product.product').browse(cr, uid, product_id, context= context)
        supplier_id=self.pool.get('product.supplierinfo').search(cr,uid,[('product_tmpl_id','=',product_brw.product_tmpl_id.id),('min_qty','<=',quantity)],order='sequence',context=None)
        if supplier_id :
            supplier = supplierinfo.browse(cr, uid,supplier_id and supplier_id[0],context = context)   
        vals = {    'name':product_brw.name,
                    'product_id': product_id,
                    'product_qty': quantity, 
                    'orderpoint_id': orderpoint_id,   
                    'partner_id': supplier and supplier.name and supplier.name.id or False                  

                }        
        return self.create(cr, uid, vals, context=context)
        

    def make_procurement_done(self, cr, uid, ids, context=None):
        today=fields.date.context_today(self, cr, uid, context=context)
        return self.write(cr, uid, ids, {'active': False, 'state':'done', 'date_close':today}, context=context)

    def merge_procurment(self, cr, uid, ids, context=None):
        context = context or {}
        vals  = {}
        warehouse = self.pool.get('stock.warehouse')
        purchase_id = False
        purchase_obj = self.pool.get ('purchase.order')
        for procurement in self.browse(cr, uid, ids, context):
          
            if not purchase_id : 
                warehouse_id=warehouse.search(cr,uid,[('company_id','=',procurement.company_id.id)],context=context)
                picking_type_id = purchase_obj._get_picking_in(cr, uid, context) 
                res = purchase_obj.onchange_picking_type_id( cr, uid,  [], picking_type_id, context=None)
                vals.update(res.get('value',{}))
                partner_id = procurement.partner_id and procurement.partner_id.id or False 
                like_partner_ids = self.search(cr, uid, [('id', 'in',ids),('partner_id','=',partner_id)]) 
                if len(ids) != len(like_partner_ids) or not len(ids) == 1:
                    raise osv.except_osv(_('Invalid Action!'),
                                _('Please select products of same supplier to give purchase order or update supplier in all lines'))
                else :
                    vals.update({
                            'picking_type_id': picking_type_id ,
                           'company_id'     : procurement.company_id.id, 
                           'invoice_method' : 'order', 
                           'pricelist_id'   : procurement.partner_id.property_product_pricelist_purchase.id , 
                           'partner_id'     : partner_id, 
       
                    
                    })
                    purchase_id = self.pool.get ('purchase.order').create( cr, uid,vals,context=context) 
                      
            self.pool.get('purchase.order.line').create( cr, uid, self.get_linedata(cr, uid,procurement.product_id,procurement.product_qty,purchase_id, context= context ), context=context)
            self.make_procurement_done(cr, uid, ids,context )
        return  purchase_id     
        

        
        
    def get_linedata(self,cr,uid,product_id,qty,purchase_id,context=None):
        
            return {
                'product_id'  : product_id and product_id.id, 
                'product_uom' : product_id and product_id.product_tmpl_id.uom_id.id,
                'price_unit'  : product_id.standard_price,
                'product_qty' : qty,
                'name'        : product_id.name,
                'date_planned': fields.date.context_today(self, cr, uid, context=context),
                'order_id'    : purchase_id
                    }                  
            
            


manufacture_procurement()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

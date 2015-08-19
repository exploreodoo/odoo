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
from datetime import timedelta

import pytz
from datetime import date
from openerp import models, fields, api, _
from openerp.exceptions import Warning



class crem_lead(models.Model):
    _inherit = 'crm.lead'
    
    
    #@api.
    @api.model
    def update_to_do_list(self):
        today=date.today().strftime('%Y-%m-%d')
        user_ids = self.env['res.users'].search([])
        print user_ids 
        for user in user_ids:
            print "data", today
            lead_ids = self.search([('user_id','=',user.id),('date_action','=', today)])
            for lead in lead_ids : 
                self.env['mail.message'].create({ 'body':'<b>Next action to be performed on the oppturnity %s </b>' %(lead.name),
                                              'author_id': 1,
                                              'type':'notification'
                                             })
        return True 
          

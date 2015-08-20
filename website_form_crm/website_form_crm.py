# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution, third party addon
#    Copyright (C) 2004-2015 Vertel AB (<http://vertel.se>).
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
from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning
from openerp import http
from openerp.http import request
from openerp import SUPERUSER_ID
from datetime import datetime
import werkzeug
import pytz
import re

import logging

_logger = logging.getLogger(__name__)


class website_form_crm(http.Controller):
    @http.route(['/form/<string:form>/lead/<model("crm.lead"):lead>', ], type='http', auth="user", website=True)
    def form_lead(self, form=False, lead=False, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        form = request.env['form.form'].search([('name', '=', form)])
        if not form:
            _logger.warning("not form ")
            return request.render('website.page_404', {})
            
        if not lead:
            _logger.warning("not lead ")
            return request.render('website.page_404', {})

        _logger.warning("Lead_id search: name: %s" % (lead.partner_name))

        if request.httprequest.method == 'POST':

            serial_fields = {}
            for key in post.keys():  # fields project.issue.description_1 .. nn
                if re.match(".*_(\d+)", key):
                    field_name = key.split('_')[0].split('.')[-1]
                    _logger.warning("Lead_id split: fieldname: %s" % (field_name))
                    if serial_fields.get(field_name):
                        serial_fields[field_name].append(post.pop(key))
                    else:
                        serial_fields[field_name] = [post.pop(key)]

            form_data = dict((field_name, post.pop(form.model_id.model + '.' + field_name))  # fields project.issue.name
                             for field_name in request.env[form.model_id.model].fields_get().keys()
                             if post.get(form.model_id.model + '.' + field_name))
            for key in serial_fields.keys():
                if type(serial_fields[key]) is list:
                    form_data[key] = ', '.join(serial_fields[key])
            
            _logger.warning("Form Data %s %s" % (form_data, post))
            
            
            
            lead.write(form_data)
            
            return werkzeug.utils.redirect(form.thanks_url)


            

            # form_data['type'] = 'opportunity'
            # crm.stage_lead1
            form_data['name'] = 'Canon 100D'
            form_data['active'] = 1
            form_data['type'] = 'opportunity'
            # form_data['user_id'] = 1
            # form_data['stage_id'] = 1
            # form_data['section_id'] = 1
            # form_data['company_id'] = 1
            form_data['priority'] = '2'
            # form_data['color'] = 0
            form_data['partner_id'] = 7

            # lead = request.env[form.model_id.model].write(form_data.pop('id'),form_data)
            lead = request.env[form.model_id.model].browse(form_data.pop('id'))
            _logger.warning("Form Data 2 %s %s" % (form_data, post))
            lead.write(form_data)
            # lead = request.env[form.model_id.model].create(form_data)
            # lead.write({'partner_name': u'Christelle'})
            # l2o = request.env['crm.lead2opportunity.partner'].with_context(active_id=lead.id,active_ids=[lead.id],active_model="crm.lead").action_apply()


            _logger.warning("Form created object %s" % (lead))
            # l2o = request.env['crm.lead2opportunity.partner'].with_context(active_id=lead_id, active_model="crm.lead").create({
            #    'name': 'convert',
            #    'action': 'create',
            #    #~ 'user_id': lead.user_id,
            #    #~ 'section_id': lead.section_id,
            # })
            # l2o.with_context(active_id=lead_id,active_ids=[lead_id], active_model="crm.lead").action_apply()


        _logger.warning("This is form post form: %s post: %s lead: %s name: %s" % (form, post, lead, lead.partner_name))
        return request.render('website_form_crm.lead_form', {'form': form, 'lead': lead})

    # ~ class form_form(models.Model):
    # ~ _name = 'form.form'
    # ~ _description = 'Simple Form'
    # ~ _order = 'name'
    # ~
    # ~ name = fields.Char('Name',required=True)
    # ~ model_id = fields.Many2one(comodel_name='ir.model',string='Model')
    # ~ body = fields.Html('Body',sanitize=False)
    # ~ thanks_url = fields.Char('Thanks Url', default="/page/website_form.thank_you")
    # ~ auth_type = fields.Selection([('public','public'),('user','user'),('admin','admin')])

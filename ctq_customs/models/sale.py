# -*- coding: utf-8 -*-
# Copyright 2021 Morwi Encoders Consulting SA de CV
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import _, api, models, fields
from datetime import datetime, timedelta


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    version_number = fields.Integer(default="1")
    version_cluster = fields.Many2one('sale.order')

    @api.model
    def create(self, vals):
        result = super(SaleOrder, self).create(vals)
        result.version_cluster = result
        result.name = result.name + str(result.version_number)
        return result

    def new_version(self):
        so_new_version = self.copy()
        so_new_version.version_number += 1
        so_new_version.version_cluster = self.version_cluster
        so_new_version.name = so_new_version.version_cluster.name[:-1] + str(so_new_version.version_number)
        
        # Recompute Dates
        d1 = self.date_order.date()
        d2 = self.validity_date
        so_new_version.validity_date = datetime.now() + timedelta(days=(d2-d1).days)
        
        self.action_cancel()
        
        # Redirect user to Version History Tree View
        field_ids = self.env['sale.order'].search([('version_cluster', '=', self.version_cluster.id)]).ids
        return {
            'name': _('Versions History'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'sale.order',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': [('id', 'in', field_ids)],
        }

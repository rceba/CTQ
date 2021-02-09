# -*- coding: utf-8 -*-
# Copyright 2020 Morwi Encoders Consulting SA de CV
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.onchange('parent_id', 'company_id')
    def _onchange_company_id(self):
        if self.parent_id:
            self.company_id = self.parent_id.company_id.id
        elif not self.company_id and not self.parent_id:
            self.company_id = self.env.company.id

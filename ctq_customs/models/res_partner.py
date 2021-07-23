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

    @api.constrains('address_format')
    def _check_address_format(self):
        for record in self:
            if record.address_format:
                address_fields = self.env['res.partner']._formatting_address_fields() + [
                    'state_code',
                    'state_name',
                    'country_code',
                    'country_name',
                    'company_name',
                    'l10n_mx_edi_colony',
                ]
                try:
                    record.address_format % {i: 1 for i in address_fields}
                except (ValueError, KeyError):
                    raise UserError(_('The layout contains an invalid format key'))

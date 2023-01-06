# -*- coding: utf-8 -*-
# Copyright 2020 Morwi Encoders Consulting SA de CV
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    pots = fields.Binary(string="Proof of Tax Situation")
    so_confirmed = fields.Boolean(compute="_compute_so_confirmed", store=True)

    @api.onchange('parent_id', 'company_id')
    def _onchange_company_id(self):
        if self.parent_id:
            self.company_id = self.parent_id.company_id.id
        elif not self.company_id and not self.parent_id:
            self.company_id = self.env.company.id

    def _display_address(self, without_company=False):

        '''
        The purpose of this function is to build and return an address formatted accordingly to the
        standards of the country where it belongs.

        :param address: browse record of the res.partner to format
        :returns: the address formatted in a display that fit its country habits (or the default ones
            if not country is specified)
        :rtype: string
        '''
        # get the information that will be injected into the display format
        # get the address format
        address_format = self._get_address_format()
        args = {
            'state_code': self.state_id.code or '',
            'state_name': self.state_id.name or '',
            'country_code': self.country_id.code or '',
            'country_name': self._get_country_name(),
            'company_name': self.commercial_company_name or '',
            'l10n_mx_edi_colony': self.l10n_mx_edi_colony or '',
        }
        for field in self._formatting_address_fields():
            args[field] = getattr(self, field) or ''
        if without_company:
            args['company_name'] = ''
        elif self.commercial_company_name:
            address_format = '%(company_name)s\n' + address_format
        return address_format % args


    def _compute_so_confirmed(self):
        for rec in self:
            rec.so_confirmed = False
            confirmed_so = rec.sale_order_ids.filtered(
                lambda s: s.state in ['sale', 'done'])
            if confirmed_so:
                rec.so_confirmed = True

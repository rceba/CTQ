# -*- coding: utf-8 -*-
# Copyright 2020 Morwi Encoders Consulting SA de CV
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def reload_mx_group(self, companies):
        user = self.env.user
        has_mx = False

        for company in self.env['res.company'].browse(companies):
            if company.country_id == self.env.ref('base.mx'):
                has_mx = True
        if has_mx and not self.user_has_groups(
                'ctq_customs.group_account_l10n_mx'):
            self.env.user.groups_id += self.env.ref(
                'ctq_customs.group_account_l10n_mx')
        elif not has_mx and self.user_has_groups(
                'ctq_customs.group_account_l10n_mx'):
            self.env.user.write({
                'groups_id': [(3, self.env.ref(
                    'ctq_customs.group_account_l10n_mx').id)]
            })

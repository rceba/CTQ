# coding: utf-8
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    def post(self):
        super(AccountMove, self).post()

        for move in self.filtered(lambda move: move.is_invoice()):
            for line in move.line_ids:
                if line.l10n_mx_edi_customs_number:
                    name = line.l10n_mx_edi_customs_number.split(',')
                    landed_cost = self.env['stock.landed.cost'].sudo().search([
                        ('l10n_mx_edi_customs_number', 'in', name),
                    ])
                    if landed_cost:
                        line.name = line.product_id.description_sale + " [Fecha documento aduanero: {}]".format(landed_cost.date)

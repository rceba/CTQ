# coding: utf-8
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    def post(self):
        for move in self.filtered(lambda move: move.is_invoice()):
            move.state = 'posted'
            lots = move._get_invoiced_lot_values()
            move.state = 'draft'
            for line in move.line_ids:
                landed_cost = False
                product_name = str(line.product_id.display_name)
                if line.product_id.description_sale:
                    product_name += " " + str(line.product_id.description_sale)
                if line.l10n_mx_edi_customs_number:
                    name = line.l10n_mx_edi_customs_number.split(',')
                    landed_cost = self.env['stock.landed.cost'].sudo().search([
                        ('l10n_mx_edi_customs_number', 'in', name),
                    ])
                    if landed_cost:
                        line.name = product_name + " [Fecha documento aduanero: {}]".format(landed_cost.date)
                if lots:
                    for lot in lots:
                        if lot['product_name'] == line.product_id.display_name:
                            string = " [Número de Lote: {}]".format(lot['lot_name'])
                            if landed_cost:
                                line.name += " -" + string
                            else:
                                line.name = product_name + string
                if move.ref:
                    string = " [Referencia: {}]".format(move.ref)
                    if landed_cost or lots:
                        line.name += " -" + string
                    else:
                        line.name = product_name + string

        super(AccountMove, self).post()

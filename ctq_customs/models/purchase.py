# Copyright 2022 Morwi Encoders Consulting SA de CV
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models, fields, api


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    name = fields.Html()


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    account_analytic_ids = fields.Many2many('account.analytic.account', compute="_compute_account_analytic_ids", store=True)

    @api.depends('order_line')
    def _compute_account_analytic_ids(self):
        for order in self:
            accounts = []
            for line in order.order_line:
                if line.account_analytic_id:
                    accounts.append(line.account_analytic_id.id)
                    
            if len(accounts) > 0:
                order.account_analytic_ids = [(6, 0, accounts)]
            else:
                order.account_analytic_ids = False
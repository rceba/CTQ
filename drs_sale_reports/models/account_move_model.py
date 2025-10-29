from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    foreign_payment_method_id = fields.Many2one(
        comodel_name="l10n_mx_edi.payment.method",
        string="Payment way"
    )

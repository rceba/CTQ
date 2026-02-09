from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    foreign_payment_method_id = fields.Many2one(
        comodel_name="l10n_mx_edi.payment.method", string="Payment way"
    )

    @api.model_create_multi
    def create(self, vals_list):
        moves = super().create(vals_list)
        try:
            other_payment_method_id = self.env.ref(
                "l10n_mx_edi.payment_method_otros", raise_if_not_found=False
            ).id
        except AttributeError:
            pass
        else:
            others = moves.filtered(
                lambda s: s.country_code == "MX"
                and not s.l10n_mx_edi_payment_method_id
                and s.l10n_mx_edi_payment_policy == "PPD"
            )
            others.write({"l10n_mx_edi_payment_method_id": other_payment_method_id})
        return moves

    def write(self, vals):
        res = super().write(vals)
        if vals.get("l10n_mx_edi_payment_method_id"):
            return res
        try:
            other_payment_method_id = self.env.ref(
                "l10n_mx_edi.payment_method_otros", raise_if_not_found=False
            ).id
        except AttributeError:
            pass
        else:
            others = self.filtered(
                lambda s: s.country_code == "MX"
                and not s.l10n_mx_edi_payment_method_id
                and s.l10n_mx_edi_payment_policy == "PPD"
            )
            others.write({"l10n_mx_edi_payment_method_id": other_payment_method_id})
        return res

# Copyright 2021 Morwi Encoders Consulting SA de CV
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class PaymentMethod(models.Model):
    _inherit = 'l10n_mx_edi.payment.method'

    name = fields.Char(translate=True)

# coding: utf-8

from odoo import fields, models


class PaymentMethod(models.Model):
    _inherit = 'l10n_mx_edi.payment.method'

    name = fields.Char(translate=True)

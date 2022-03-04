# -*- coding: utf-8 -*-
# Copyright 2021 Morwi Encoders Consulting SA de CV
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models

class UtmSource(models.Model):
    _inherit = 'utm.source'

    active = fields.Boolean(default=True)

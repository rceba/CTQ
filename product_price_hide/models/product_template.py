# Copyright 2020 Morwi Encoders Consulting SA de CV
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"
    
    pricelist_item_ids = fields.One2many(
        'product.pricelist.item',
        'product_tmpl_id'
    )

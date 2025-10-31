from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    description_sale = fields.Html()

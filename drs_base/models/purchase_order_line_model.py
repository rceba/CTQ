from odoo import models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

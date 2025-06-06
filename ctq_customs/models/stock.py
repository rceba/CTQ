# Copyright 2021 Morwi Encoders Consulting SA de CV
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models, fields, api

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    def _check_no_duplicate_line(self):
        for quant in self:
            domain = [
                ('id', '!=', quant.id),
                ('product_id', '=', quant.product_id.id),
                ('location_id', '=', quant.location_id.id),
                ('owner_id', '=', quant.owner_id.id),
                ('package_id', '=', quant.package_id.id),
                ('lot_id', '=', quant.lot_id.id),
            ]
            existings = self.search_count(domain)
            if existings:
                raise UserError(_("There is already one inventory adjustment quant for this product,"
                                  " you should rather modify this one instead of creating a new one."))

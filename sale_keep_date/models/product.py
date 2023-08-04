# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models
from odoo.tools import float_compare


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _get_filtered_sellers(self, partner_id=False, quantity=0.0, date=None, uom_id=False, params=False, filter_company=True):
        self.ensure_one()
        if date is None:
            date = fields.Date.context_today(self)
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')

        sellers_filtered = self._prepare_sellers(params)
        if filter_company:
            sellers_filtered = sellers_filtered.filtered(lambda s: not s.company_id or s.company_id.id == self.env.company.id)
        sellers = self.env['product.supplierinfo']
        for seller in sellers_filtered:
            # Set quantity in UoM of seller
            quantity_uom_seller = quantity
            if quantity_uom_seller and uom_id and uom_id != seller.product_uom:
                quantity_uom_seller = uom_id._compute_quantity(quantity_uom_seller, seller.product_uom)

            if seller.date_start and seller.date_start > date:
                continue
            if seller.date_end and seller.date_end < date:
                continue
            if partner_id and seller.name not in [partner_id, partner_id.parent_id]:
                continue
            if quantity is not None and float_compare(quantity_uom_seller, seller.min_qty, precision_digits=precision) == -1:
                continue
            if seller.product_id and seller.product_id != self:
                continue
            sellers |= seller
        return sellers

    def _select_seller(self, partner_id=False, quantity=0.0, date=None, uom_id=False, params=False, filter_company=True):
        sellers = self._get_filtered_sellers(partner_id=partner_id, quantity=quantity, date=date, uom_id=uom_id, params=params, filter_company=filter_company)
        res = self.env['product.supplierinfo']
        for seller in sellers:
            if not res or res.name == seller.name:
                res |= seller
        return res and res.sorted('price')[:1]
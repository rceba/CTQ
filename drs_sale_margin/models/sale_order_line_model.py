from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends("price_subtotal", "product_uom_qty", "purchase_price")
    def _compute_margin(self):
        to_do = self.filtered("product_id")
        super(SaleOrderLine, self - to_do)._compute_margin()
        for line in to_do:
            purchase_price = 0
            date = line.order_id.date_order.date()
            supplierinfo_id = line.product_id._select_seller(
                quantity=line.product_uom_qty,
                date=line.order_id.date_order and date,
                uom_id=line.product_uom,
            )
            if supplierinfo_id:
                frm_cur = supplierinfo_id.currency_id
                to_cur = line.order_id.pricelist_id.currency_id
                purchase_price = frm_cur._convert(
                    supplierinfo_id.price,
                    to_cur,
                    line.order_id.company_id or self.env.company,
                    date or fields.Date.today(),
                )
            line.purchase_price = purchase_price
            line.margin = line.price_subtotal - (
                line.purchase_price * line.product_uom_qty
            )
            line.margin_percent = (
                line.price_subtotal and line.margin / line.price_subtotal
            )

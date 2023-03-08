# -*- coding: utf-8 -*-
# Copyright 2020 Morwi Encoders Consulting SA de CV
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import _, api, models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    confirmation_date = fields.Datetime(
        string='Confirmation Date',
        index=True,
        help="Confirmation date of confirmed orders.",
    )
    date_order = fields.Datetime(
        help="Create date of sale quotations.",
        readonly=False,
    )
    dateonly_order = fields.Date(
        compute="_compute_dateonly_order")

    @api.depends('date_order')
    def _compute_dateonly_order(self):
        for order in self:
            order.dateonly_order = order.date_order.date()

    def action_confirm(self):
        if self._get_forbidden_state_confirm() & set(self.mapped('state')):
            raise UserError(_(
                'It is not allowed to confirm an order in the following '
                'states: %s'
            ) % (', '.join(self._get_forbidden_state_confirm())))

        for order in self.filtered(
                lambda order: order.partner_id not in
                order.message_partner_ids):
            order.message_subscribe([order.partner_id.id])
        self.write({
            'state': 'sale',
            'confirmation_date': fields.Datetime.now(),
        })
        self._action_confirm()
        if self.env.user.has_group('sale.group_auto_done_setting'):
            self.action_done()
        return True


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends('price_subtotal', 'product_uom_qty', 'purchase_price')
    def _compute_margin(self):
        for line in self:
            purchase_price = 0
            date = line.order_id.date_order.date()
            for line in self:
                supplierinfo_id = line.product_id._select_seller(
                    quantity=line.product_uom_qty,
                    date=line.order_id.date_order and date,
                    uom_id=line.product_uom
                )
                if supplierinfo_id:
                    frm_cur = supplierinfo_id.currency_id
                    to_cur = line.order_id.pricelist_id.currency_id
                    purchase_price = frm_cur._convert(
                        supplierinfo_id.price,
                        to_cur,
                        line.order_id.company_id or self.env.company,
                        date or fields.Date.today()
                    )

            line.purchase_price = purchase_price
            line.margin = line.price_subtotal - (line.purchase_price * line.product_uom_qty)
            line.margin_percent = line.price_subtotal and line.margin/line.price_subtotal

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
    dateonly_order = fields.Date(compute="_compute_dateonly_order")

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

    def _compute_margin(self, order_id, product_id, product_uom_id):
        price = 0
        date = order_id.date_order.date()
        for line in self:
            supplierinfo_id = product_id._select_seller(
                quantity=line.product_uom_qty,
                date=order_id.date_order and date,
                uom_id=product_uom_id
            )
            if supplierinfo_id:
                frm_cur = supplierinfo_id.currency_id
                to_cur = order_id.pricelist_id.currency_id
                price = frm_cur._convert(
                    supplierinfo_id.price,
                    to_cur,
                    order_id.company_id or self.env.company,
                    date or fields.Date.today()
                )
        return price
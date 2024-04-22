# -*- coding: utf-8 -*-
# Copyright 2022 Morwi Encoders Consulting SA de CV
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models, fields, api


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    name = fields.Html()

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    account_analytic_ids = fields.Many2many('account.analytic.account', compute="_compute_account_analytic_ids", store=True)
    sale_order_id = fields.Many2one(comodel_name="sale.order")

    @api.depends('order_line')
    def _compute_account_analytic_ids(self):
        for order in self:
            accounts = []
            for line in order.order_line:
                if line.account_analytic_id:
                    accounts.append(line.account_analytic_id.id)
                    
            if len(accounts) > 0:
                order.account_analytic_ids = [(6, 0, accounts)]
            else:
                order.account_analytic_ids = False
    @api.model
    def write(self, vals):
        """
            description: SE HEREDA LA FUNCION NATIVA write DE ODOO PARA EL MODELO purchase.order
            CON LA FINALIDAD DE CAMBIAR EL ORDEN DE LAS LINEAS DE LA COMPRA QUE SE GENERAN AL
            CONFIRMAR UNA ORDEN DE VENTA.

            fields: origin, sale_order_id, order_line

            return: nuevas lineas en la orden de la compra con el mismo orden de la venta
        """
        res = super(PurchaseOrder, self).write(vals)
        if vals.get('origin'):
            origin = vals.get('origin')
            origin_list = origin.split(', ')
            if len(origin_list) > 1:
                origin = origin_list[-1]
            sale_id = self.sale_order_id.search([('name', '=', origin)],limit=1)
            if sale_id:
                self.sale_order_id = sale_id.id
        if vals.get('sale_order_id'):
            sale_order_product_ids = self.sale_order_id.order_line.mapped('product_id.name')
            sale_order_product_ids_copy = (sale_order_product_ids)
            for record in sale_order_product_ids_copy:
                product_product_id = self.env['product.template'].search([('name', '=', record), ('company_id', '=', self.sale_order_id.company_id.id)])
                if product_product_id.detailed_type in 'service':
                    sale_order_product_ids.remove(record)
            sorted_order_lines = sorted(self.order_line, key=lambda x: sale_order_product_ids.index(x.product_id.name))
            purchase_order_line = self.order_line
            for id in sorted_order_lines:
                for line in id:
                    self.env['purchase.order.line'].create({
                        'product_id': line.product_id.id,
                        'price_unit': line.price_unit,
                        'product_qty': line.product_qty,
                        'order_id': self.id,
                    })
            #SE DESVINCULAN LOS ANTIGUOS IDS SIN ORDEN DE LA COMPRA
            for id in purchase_order_line.ids:
                self.order_line = [(3, id)]
        return res
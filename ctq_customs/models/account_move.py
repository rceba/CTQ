# -*- coding: utf-8 -*-
# Copyright 2021 Morwi Encoders Consulting SA de CV
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, models, fields, _
from datetime import timedelta


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    description = fields.Char(string="Notes")
    name = fields.Html()


class AccountMove(models.Model):
    _inherit = 'account.move'

    narration = fields.Html()
    amount_untaxed_mxn = fields.Monetary(string='Untaxed Amount (MXN)', store=True, readonly=True,
        related='amount_untaxed_signed')
    amount_tax_mxn = fields.Monetary(string='Tax (MXN)', store=True, readonly=True,
        related='amount_tax_signed')
    amount_total_mxn = fields.Monetary(string='Total (MXN)', store=True, readonly=True,
        related='amount_total_signed')
    amount_untaxed_usd = fields.Monetary(string='Untaxed Amount (USD)', store=True, readonly=True,
        compute='_compute_amount_cur')
    amount_tax_usd = fields.Monetary(string='Tax (USD)', store=True, readonly=True,
        compute='_compute_amount_cur')
    amount_total_usd = fields.Monetary(string='Total (USD)', store=True, readonly=True,
        compute='_compute_amount_cur')
    tasa_cambio = fields.Float(string='Tasa de cambio', readonly=True,
                               digits=(16, 4), compute='_compute_tasa_cambio')

    @api.depends('amount_untaxed', 'amount_tax', 'amount_total')
    @api.onchange('amount_untaxed', 'amount_tax', 'amount_total')
    def _compute_amount_cur(self):
        for invoice in self:
            invoice.amount_untaxed_mxn = invoice.amount_untaxed_signed
            invoice.amount_tax_mxn = invoice.amount_tax_signed
            invoice.amount_total_mxn = invoice.amount_total_signed

            frm_cur = invoice.currency_id
            to_cur = self.env.ref('base.USD')
            invoice.amount_untaxed_usd = frm_cur._convert(
                invoice.amount_untaxed,
                to_cur,
                invoice.company_id or self.env.company,
                invoice.date or fields.Date.today()
            )
            invoice.amount_tax_usd = frm_cur._convert(
                invoice.amount_tax,
                to_cur,
                invoice.company_id or self.env.company,
                invoice.date or fields.Date.today()
            )
            invoice.amount_total_usd = frm_cur._convert(
                invoice.amount_total,
                to_cur,
                invoice.company_id or self.env.company,
                invoice.date or fields.Date.today()
            )

    def post(self):
        for move in self.filtered(lambda move: move.is_invoice()):
            move.state = 'posted'
            lots = move._get_invoiced_lot_values()
            move.state = 'draft'
            for line in move.line_ids:
                if line.display_type in ('line_section', 'line_note'):
                    continue
                landed_cost = False
                product_name = ""
                if self.partner_id.lang:
                    product = line.product_id.with_context(lang=move.partner_id.lang)
                else:
                    product = line.product_id
                if line.description:
                    product_name +=  str(line.description) + " "
                product_name += str(product.display_name)
                if product.description_sale:
                    product_name += " " + str(product.description_sale)
                line.name = product_name
                if line.l10n_mx_edi_customs_number:
                    name = line.l10n_mx_edi_customs_number.split(',')
                    landed_cost = self.env['stock.landed.cost'].sudo().search([
                        ('l10n_mx_edi_customs_number', 'in', name),
                    ])
                    if landed_cost:
                        line.name += _(" [Customs document date: {}]").format(landed_cost.date)
                if lots:
                    count = line.quantity
                    string = _(" [Lots Number(s): ")
                    while lots and count > 0:
                        count -= 1
                        lot = lots[0]
                        if lot['product_name'] == product.display_name:
                            string += str(lot['lot_name']) + ", "
                            lots.remove(lot)
                    if string != _(" [Lots Number(s): "):
                        string = string[:-2] + "]"
                        if landed_cost:
                            line.name += " -"
                        line.name += string
                if move.ref:
                    string = _(" [Reference: {}]").format(move.ref)
                    if landed_cost or lots:
                        line.name += " -"
                    line.name += string
        return super(AccountMove, self).post()

    @api.depends('amount_total_signed', 'amount_total')
    def _compute_tasa_cambio(self):
        for rec in self:
            if rec.amount_total_signed and rec.amount_total:
                rec.tasa_cambio = rec.amount_total_signed / rec.amount_total
            else:
                rec.tasa_cambio = 0.0
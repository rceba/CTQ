# Copyright 2020 Morwi Encoders Consulting SA de CV
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class SaleReport(models.Model):
    _inherit = 'sale.report'

    medium_id = fields.Many2one(
        'utm.medium',
        compute='_compute_medium_id',
        store=True,
    )

    @api.depends('order_id')
    def _compute_medium_id(self):
        for rec in self:
            rec.medium_id = (
                rec.order_id.medium_id.id or
                rec.order_id.opportunity_id.medium_id.id)

    # def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
    #     fields['medium_id'] = """
    #         , s.medium_id AS medium_id"""

    #     groupby += ', s.medium_id'

    #     return super(SaleReport, self)._query(
    #         with_clause, fields, groupby, from_clause)

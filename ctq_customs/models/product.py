
# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    description_purchase = fields.Html(translate=True)
    description_sale = fields.Html(translate=True)


class ProductSupplierinfo(models.Model):
    _inherit = 'product.supplierinfo'

    # Constrain for date_start and date_end where if both are set, date_end must be greater than date_start
    @api.constrains('date_start', 'date_end')
    def _check_date_start_end(self):
        for record in self:
            if record.date_start and record.date_end:
                if record.date_end < record.date_start:
                    raise ValidationError(_('The start date must be prior to the end date.'))

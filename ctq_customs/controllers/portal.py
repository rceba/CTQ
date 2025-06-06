# Copyright 2021 Morwi Encoders Consulting SA de CV
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

import base64

from odoo import http
from odoo.http import content_disposition, Controller, request, route
from odoo.addons.portal.controllers.portal import CustomerPortal


CustomerPortal.OPTIONAL_BILLING_FIELDS.append('l10n_mx_type_of_operation')
CustomerPortal.OPTIONAL_BILLING_FIELDS.append('pots')


class CustomCustomerPortal(CustomerPortal):
    @route(['/my/account'], type='http', auth='user', website=True)
    def account(self, redirect=None, **post):
        test_file = post.get('pots')
        if test_file:
            file_base64 = base64.encodestring(test_file.read())
            post.update({'pots': file_base64})
        res = super(CustomCustomerPortal, self).account(redirect=None, **post)
        return res
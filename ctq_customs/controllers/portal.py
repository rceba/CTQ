# -*- coding: utf-8 -*-
# Copyright 2021 Morwi Encoders Consulting SA de CV
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo.addons.portal.controllers.portal import CustomerPortal


CustomerPortal.OPTIONAL_BILLING_FIELDS.append('l10n_mx_type_of_operation')
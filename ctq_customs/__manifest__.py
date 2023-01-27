# -*- coding: utf-8 -*-
# Copyright 2021 Morwi Encoders Consulting SA de CV
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    'name': 'CTQ Customizations',
    'category': 'Hidden',
    'version': '15.0.1.0.0',
    'description': """
       Module add custom flows for CTQ
        """,
    'summary': """
        Module add custom flows for CTQ
        """,
    'depends': [
        'web',
        'l10n_mx_edi',
        'l10n_mx_edi_landing',
        'l10n_mx_reports',
        'sale_keep_date',
        'purchase',
    ],
    'data': [
        'report/purchase_report_templates.xml',
        'report/report_invoice.xml',
        'report/sale_report_templates.xml',
        'data/res_groups_data.xml',
        'views/account_move_views.xml',
        'views/report_templates.xml',
        'views/res_partner_views.xml',
        'views/sale_views.xml',
        'views/purchase_views.xml',
        'views/templates.xml',
        'views/views.xml',
    ],
    'assets': {
    'web.assets_backend': [
        'ctq_customs/static/src/js/**/*',
        'ctq_customs/static/src/css/**/*',
    ],
    'web.report_assets_common': [
        'ctq_customs/static/src/css/report.css',
    ],
},
}
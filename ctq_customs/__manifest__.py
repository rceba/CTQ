# -*- coding: utf-8 -*-
# Copyright 2021 Morwi Encoders Consulting SA de CV
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    'name': 'CTQ Customizations',
    'category': 'Hidden',
    'version': '13.0.1.0.0',
    'description': """
       Module add custom flows for CTQ
        """,
    'summary': """
        Module add custom flows for CTQ
        """,
    'depends': [
        'web',
        'l10n_mx_edi',
        'l10n_mx_reports',
    ],
    'data': [
        'report/report_invoice.xml',
        'report/sale_report_templates.xml',
        'data/res_groups_data.xml',
        'views/report_templates.xml',
        'views/templates.xml',
        'views/views.xml',
    ],
}

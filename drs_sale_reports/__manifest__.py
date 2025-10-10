# -*- coding: utf-8 -*-
{
    "name": "Drasi | drs_sale_reports",
    "summary": "Mejora en los formatos",
    "description": """
        Este módulo complementa los reportes de ventas, compras.
    """,
    "author": "Drasi Consulting",
    "website": "https://www.drasi.odoo.com",
    "category": "Sale",
    "version": "17.0.1.0.0",
    "depends": [
        'sale',
        'drs_sale',
        'purchase',
        'purchase_stock',
        'l10n_mx_edi',
        'l10n_mx_edi_extended'
    ],
    "data": [
        'views/report_saleorder_document.xml',
        'views/purchase_quotation_templates.xml',
        'views/purchase_order_templates.xml',
        'views/report_invoice.xml',
        'views/report_invoice_trac.xml',
        'views/sale_report_views.xml'
    ],
    "licence": "LGPL-3",
}

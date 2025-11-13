# -*- coding: utf-8 -*-
{
    "name": "Drasi | drs_sale",
    "summary": "Cambios en Ventas",
    "description": """
        Este módulo implementa los cambios al flujo de Ventas.
    """,
    "author": "Drasi Consulting",
    "website": "https://www.drasi.odoo.com",
    "category": "Sale",
    "version": "17.0.1.0.1",
    "depends": ["sale", "drs_base"],
    "data": [
        "views/sale_report_views.xml",
        "views/product_template_views.xml",
        "views/sale_order_views.xml",
    ],
    "licence": "LGPL-3",
}

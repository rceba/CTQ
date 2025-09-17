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
    "version": "17.0.1.0.0",
    "depends": ["sale"],
    "data": [
        # 'security/ir.model.access.csv',
        "views/sale_order_views.xml",
    ],
    "web.assets_backend": [
        "drs_sale/static/src/css/backend.css",
    ],
    "licence": "LGPL-3",
}

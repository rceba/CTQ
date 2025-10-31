{
    "name": "DRASI | drs_base",
    "summary": "Migrations tools",
    "description": """
        This module add scripts for migrations
    """,
    "author": "Drasi Consulting",
    "website": "https://www.drasi.odoo.com",
    "category": "Tools",
    "version": "17.0.1.0.2",
    "depends": ["base", "hr_work_entry", "sale_margin"],
    "data": [
        "data/payroll.xml",
        "views/sale_order_views.xml",
        "views/purchase_order_views.xml",
        "views/account_move_views.xml"
    ],
    "application": True,
    "installable": True,
    "web.assets_backend": [
        "drs_sale/static/src/css/backend.css",
    ],
    "licence": "LGPL-3",
}

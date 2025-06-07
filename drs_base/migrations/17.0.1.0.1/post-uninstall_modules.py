import logging

from odoo.upgrade import util

_logger = logging.getLogger("DRS_MIG")


def migrate(cr, version):
    modules_to_remove = [
        "auditlog",
        "ctq_customs",
        "mail_tracking",
        "product_price_hide",
        "sale_keep_date",
    ]

    for module in modules_to_remove:
        if util.module_installed(cr, module):
            util.remove_module(cr, module)
            _logger.info(f"Modulo {module} desinstalado correctamente.")

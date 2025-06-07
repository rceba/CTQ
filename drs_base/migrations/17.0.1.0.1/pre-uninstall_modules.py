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

    util.parallel_execute(
        cr,
        [
            "DELETE FROM ir_ui_view WHERE name='Odoo Studio: sale.order.form customization'",
            "DELETE FROM ir_ui_view WHERE name='Odoo Studio: sale.order.search.inherit.quotation customization'",
            "DELETE FROM ir_ui_view WHERE name='Odoo Studio: sale.order.search.inherit.sale customization'",
            "DELETE FROM ir_ui_view WHERE name='Odoo Studio: sale.order.tree customization'",
            "DELETE FROM ir_ui_view WHERE name='Odoo Studio: account.invoice.tree customization'",
            "DELETE FROM ir_ui_view WHERE name='Odoo Studio: account.payment.tree customization'",
        ],
    )

    for module in modules_to_remove:
        if util.module_installed(cr, module):
            util.remove_module(cr, module)
            _logger.info(f"Eliminado modulo {module}.")

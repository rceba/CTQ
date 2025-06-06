from odoo.upgrade import util


def migrate(cr, version):
    modules_to_remove = ["auditlog", "ctq_customs", "mail_tracking", "product_price_hide", "sale_keep_date"]

    for module in modules_to_remove:
        if util.is_module_installed(cr, module):
            util.uninstall_module(cr, module)

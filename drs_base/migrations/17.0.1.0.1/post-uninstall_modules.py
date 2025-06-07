import logging

from odoo.upgrade import util

_logger = logging.getLogger("DRS_MIG")


def migrate(cr, version):
    def_contract = util.ref(cr, "hr_contract_migration")
    if def_contract:
        util.parallel_execute(
            cr,
            [
                "UPDATE hr_work_entry SET contract_id=%s WHERE contract_id IS NULL" % def_contract
            ],
        )

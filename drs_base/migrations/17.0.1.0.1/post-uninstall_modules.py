import logging

from odoo.upgrade import util

_logger = logging.getLogger("DRS_MIG")


def migrate(cr, version):
    util.parallel_execute(
        cr,
        [
            "DELETE FROM hr_work_entry WHERE contract_id IS NULL"
        ],
    )

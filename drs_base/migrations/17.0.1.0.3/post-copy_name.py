import logging

from odoo.upgrade import util

_logger = logging.getLogger("DRS_MIG")


def migrate(cr, version):
    util.parallel_execute(
        cr,
        [
            "UPDATE account_move_line SET ctq_name=name",
        ],
    )

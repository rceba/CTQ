import logging

from odoo import SUPERUSER_ID, api
from odoo.tools import html2plaintext

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    _logger.info('Iniciando migración: Conversión HTML a texto plano')

    env = api.Environment(cr, SUPERUSER_ID, {})

    try:
        for sol in env["sale.order.line"].search([("name", "!=", False)]):
            try:
                sol.write({"name": html2plaintext(sol.name)})
            except Exception as e:
                _logger.error(f'Error en registro {sol.id}: {str(e)}')
                continue
        for pol in env["purchase.order.line"].search([("name", "!=", False)]):
            try:
                pol.write({"name": html2plaintext(pol.name)})
            except Exception as e:
                _logger.error(f'Error en registro {pol.id}: {str(e)}')
                continue
    except Exception as e:
        _logger.info(str(e))

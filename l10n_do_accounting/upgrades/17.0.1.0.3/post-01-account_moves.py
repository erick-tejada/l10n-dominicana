import logging
from odoo.upgrade import util

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    env = util.env(cr)
    
    _logger.warning("Starting NCF Migration -> Removed NCF for Canceled Bills")

    canceled_bills = env["account.move"].search([('state','=','cancel'),('move_type','=','in_invoice')])
    names = []
    for bill in canceled_bills:
        names.append(bill.name)
        bill.write({
            'l10n_latam_document_number': '',
            'l10n_do_fiscal_number': '',
            'l10n_do_sequence_prefix': '',
            'l10n_do_sequence_number': False,
        })

    _logger.warning("Removed NCF info for: %s", ', '.join(names))
import logging
from odoo.upgrade import util

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    env = util.env(cr)
    
    _logger.warning("------------------------------------------------------------------------------------")
    _logger.warning("Changing XML References for old Tax Groups")
    
    tax_groups = env['account.tax.group'].search([
        ('module','=','account'),
        ('name', 'in', ['1_group_tax', '1_group_isr', '1_group_itbis', '1_group_ret'])
    ])
    
    processed_identifiers = []
    for group in tax_groups:
        vals = str(group.name).split('_')        
        if vals[0] == '1':
            vals.insert(1, 'tax')
            new_name = '_'.join(vals)
            group.name = new_name
            processed_identifiers.append(new_name)
    
    _logger.warning("Processed Identifiers: %s" % ', '.join(processed_identifiers))
    _logger.warning("------------------------------------------------------------------------------------")
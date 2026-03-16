import logging

from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})

    TaxGroup = env["account.tax.group"]
    IrModelData = env["ir.model.data"]

    companies = env["res.company"].search([])

    for company in companies:

        itbis_groups = TaxGroup.search([
            ("name", "ilike", "itbis"),
            ("company_id", "=", company.id),
        ])

        for group in itbis_groups:

            new_xmlid = "%s_tax_group_itbis" % company.id

            existing = IrModelData.search([
                ("module", "=", "account"),
                ("name", "=", new_xmlid),
            ])

            if existing:
                _logger.info("XMLID ya existe: %s", new_xmlid)
                continue

            IrModelData.create({
                "module": "account",
                "name": new_xmlid,
                "model": "account.tax.group",
                "res_id": group.id,
                "noupdate": True,
            })

            _logger.info(
                "Creado XMLID %s para tax group %s",
                new_xmlid,
                group.name,
            )
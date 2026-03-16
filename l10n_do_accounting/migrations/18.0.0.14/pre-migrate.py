import logging

from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})

    TaxGroup = env["account.tax.group"]
    IrModelData = env["ir.model.data"]

    companies = env["res.company"].search([])

    tax_groups = [
        ("itbis", "tax_group_itbis"),
        ("isr", "tax_group_isr"),
    ]

    for company in companies:

        for search_name, xml_suffix in tax_groups:

            groups = TaxGroup.search([
                ("name", "ilike", search_name),
                ("company_id", "=", company.id),
            ], limit=1)

            for group in groups:

                new_xmlid = "%s_%s" % (company.id, xml_suffix)

                existing = IrModelData.search([
                    ("module", "=", "account"),
                    ("name", "=", new_xmlid),
                ], limit=1)

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
# -*- coding: utf-8 -*-
# © 2013 Guewen Baconnier,Camptocamp SA,Akretion
# © 2016 Sodexis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import AbstractComponent
from odoo.addons.connector.exception import MappingError


class OdooImportMapper(AbstractComponent):
    _name = 'odoo.import.mapper'
    _inherit = ['base.odoo.connector', 'base.import.mapper']
    _usage = 'import.mapper'

    def _get_many2one_internal_id(self, record, model, field_name):
        """
        Return the Internal ID of the related field value
        :param record: Current record containing the external ID
        :param model: Model of the many2one
        :param field_name: Name of the field containing the external ID
        :return: The internal ID of the relation binded with given external ID
        :rtype: int
        """
        if not record.get(field_name):
            return

        binder = self.binder_for(model)
        model_binding = binder.to_internal(record[field_name][0])

        if not model_binding:
            raise MappingError(
                "The %s with distant Odoo id %s is not import." % (
                    model, record[field_name][0])
            )

        return {field_name: model_binding.odoo_id.id}


class OdooExportMapper(AbstractComponent):
    _name = 'odoo.export.mapper'
    _inherit = ['base.odoo.connector', 'base.export.mapper']
    _usage = 'export.mapper'


def normalize_datetime(field):
    """Change a invalid date which comes from Magento, if
    no real date is set to null for correct import to
    OpenERP"""

    def modifier(self, record, to_attr):
        if record[field] == '0000-00-00 00:00:00':
            return None
        return record[field]
    return modifier

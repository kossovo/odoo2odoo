from odoo.tools.translate import _
from odoo.addons.component.core import AbstractComponent


class OdooDeleter(AbstractComponent):
    """ Base deleter for Odoo"""
    _name = 'odoo.exporter.deleter'
    _inherit = 'base.deleter'
    _usage = 'record.exporter.deleter'

    def run(self, external_id):
        """ Run the synchronization, delete the record on distant Odoo

        :param external_id: identifier of the record to delete
        """
        self.backend_adapter.delete(external_id)
        return _('Record %s deleted on distant Odoo') % (external_id,)
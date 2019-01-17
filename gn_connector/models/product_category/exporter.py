import logging

from odoo.addons.component.core import Component

_logger = logging.getLogger(__name__)


class OdooProductCategoryExporter(Component):
    """ Export product categories to distant Odoo """
    _name = 'odoo.product.category.exporter'
    _inherit = 'odoo.exporter'
    _apply_on = ['odoo.product.category']
    _usage = 'product.category.exporter'


    def run(self, binding):
        """ Run the job to export the product category"""
        external_id = None
        try:
            data = {
                'name': binding.odoo_id.name,
            }
            if binding.external_id:
                self.backend_adapter.write(binding.external_id, data)
            else:
                external_id = self.backend_adapter.create(data)
        except Exception as e:
            raise

        if external_id:
            self.binder.bind(external_id, binding.id)

    def _before_export(self):
        """ Export parent categories before this one."""
        relation = (self.binding.odoo_parent_id or self.binding.odoo_id)
        self._export_dependencies(relation, 'odoo.product.category')
from odoo.addons.component.core import Component
from odoo.addons.component_event import skip_if


class OdooBindingProductCategoryListener(Component):
    _name = 'odoo.binding.product.category.listener'
    _inherit = 'base.connector.listener'
    _apply_on = ['odoo.product.category']

    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_record_create(self, record, fields=None):
        record.with_delay().export_record()

    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_record_write(self, record, fields=None):
        record.with_delay().export_record()


class OdooProductCategoryListener(Component):
    _name = 'odoo.product.category.listener'
    _inherit = 'base.connector.listener'
    _apply_on = ['product.category']

    def on_record_create(self, record, fields=None):
        if not record.odoo_bind_ids:
            self.category_create_bindings(record)

    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_record_write(self, record, fields=None):
        if record.odoo_bind_ids:
            for binding in record.odoo_bind_ids:
                binding.with_delay().export_record()

    def category_create_bindings(self, category):
         """
         Create a ``odoo.product.category` record. This record will then
         be exported to distant Odoo.
         """
         for backend in self.env['odoo.backend'].search([]):
             self.env['odoo.product.category'].create({
                 'backend_id': backend.id,
                 'odoo_id': category.id,
                 'odoo_parent_id': category.parent_id.odoo_bind_ids and category.parent_id.odoo_bind_ids[0],
             })
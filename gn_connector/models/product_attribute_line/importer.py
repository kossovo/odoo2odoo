from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping
from odoo.addons.connector.exception import MappingError



class ProductAttributeLineBatchImporter(Component):
    """ Import the distant Odoo Product Attribute Lines.

    For every product Attribute Lines in the list, a delayed job is created.
    """
    _name = 'odoo.product.attribute.line.batch.importer'
    _inherit = 'odoo.delayed.batch.importer'
    _apply_on = ['odoo.product.attribute.line']

    def _import_record(self, external_id, job_options=None):
        """ Delay the job for the import"""
        super(ProductAttributeLineBatchImporter, self)._import_record(
            external_id, job_options=job_options,
        )

    def run(self, filters=[]):
        """ Run the synchronization"""
        updated_ids = self.backend_adapter.search(filters)

        for updated in updated_ids:
            self._import_record(updated)


class ProductAttributeLineImporter(Component):
    _name = 'odoo.product.attribute.line.importer'
    _inherit = 'odoo.importer'
    _apply_on = ['odoo.product.attribute.line']

    def _import_dependencies(self):
        """ Import the attribute dependencies for the record"""
        record = self.odoo_record
        # import product template
        if record.get('product_tmpl_id'):
            self._import_dependency(record.get('product_tmpl_id')[0], 'odoo.product.template')
        # import product attribute
        if record.get('attribute_id'):
            self._import_dependency(record.get('attribute_id')[0], 'odoo.product.attribute')
        # import product attribute value
        if record.get('value_ids'):
            for value_id in record.get('value_ids'):
                self._import_dependency(value_id, 'odoo.product.attribute.value')


class ProductAttributeLineImportMapper(Component):
    _name = 'odoo.product.attribute.line.import.mapper'
    _inherit = 'odoo.import.mapper'
    _apply_on = 'odoo.product.attribute.line'

    direct = [
    ]

    @mapping
    def backend_id(self, record):
        return {'backend_id': self.backend_record.id}

    @mapping
    def attribute_id(self, record):
        return self._get_many2one_internal_id(record, 'odoo.product.attribute', 'attribute_id')

    @mapping
    def product_tmpl_id(self, record):
        return self._get_many2one_internal_id(record, 'odoo.product.template', 'product_tmpl_id')

    @mapping
    def value_ids(self, record):
        values = []
        binder = self.binder_for('odoo.product.attribute.value')
        if record.get('value_ids'):
            for value_id in record.get('value_ids'):
                values.append(binder.to_internal(value_id).id)

        return {'value_ids': [(6, 0, values)]}

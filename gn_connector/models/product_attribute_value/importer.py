from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping
from odoo.addons.connector.exception import MappingError


class ProductAttributeValueBatchImporter(Component):
    """ Import the distant Odoo Product Attribute Values.

    For every product Attribute Values in the list, a delayed job is created.
    """
    _name = 'odoo.product.attribute.value.batch.importer'
    _inherit = 'odoo.delayed.batch.importer'
    _apply_on = ['odoo.product.attribute.value']

    def _import_record(self, external_id, job_options=None):
        """ Delay the job for the import"""
        super(ProductAttributeValueBatchImporter, self)._import_record(
            external_id, job_options=job_options,
        )

    def run(self, filters=[]):
        """ Run the synchronization"""
        updated_ids = self.backend_adapter.search(filters)

        for updated in updated_ids:
            self._import_record(updated)


class ProductAttributeValueImporter(Component):
    _name = 'odoo.product.attribute.value.importer'
    _inherit = 'odoo.importer'
    _apply_on = ['odoo.product.attribute.value']

    def _import_dependencies(self):
        """ Import the attribute dependencies for the record"""
        record = self.odoo_record
        # import product attribute
        if record.get('attribute_id'):
            self._import_dependency(record.get('attribute_id')[0], 'odoo.product.attribute')


class ProductAttributeValueImportMapper(Component):
    _name = 'odoo.product.attribute.value.import.mapper'
    _inherit = 'odoo.import.mapper'
    _apply_on = 'odoo.product.attribute.value'

    direct = [
        ('name', 'name'),
        ('code', 'code'),
        ('sequence', 'sequence'),
    ]

    @mapping
    def backend_id(self, record):
        return {'backend_id': self.backend_record.id}

    @mapping
    def attribute_id(self, record):
        if not record.get('attribute_id'):
            return
        binder = self.binder_for('odoo.product.attribute')
        attribute_binding = binder.to_internal(record['attribute_id'][0])

        if not attribute_binding:
            raise MappingError("The product attribute with "
                               "distant Odoo id %s is not import." %
                               record['attribute_id'][0])

        attribute = attribute_binding.odoo_id
        return {
            'attribute_id': attribute.id,
        }

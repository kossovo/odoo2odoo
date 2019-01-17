from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping



class ProductAttributeBatchImporter(Component):
    """ Import the distant Odoo Product Attributes.

    For every product Attributes in the list, a delayed job is created.
    """
    _name = 'odoo.product.attribute.batch.importer'
    _inherit = 'odoo.delayed.batch.importer'
    _apply_on = ['odoo.product.attribute']

    def _import_record(self, external_id, job_options=None):
        """ Delay the job for the import"""
        super(ProductAttributeBatchImporter, self)._import_record(
            external_id, job_options=job_options,
        )

    def run(self, filters=[]):
        """ Run the synchronization"""
        updated_ids = self.backend_adapter.search(filters)

        for updated in updated_ids:
            self._import_record(updated)


class ProductAttributeImporter(Component):
    _name = 'odoo.product.attribute.importer'
    _inherit = 'odoo.importer'
    _apply_on = ['odoo.product.attribute']


class ProductAttributeImportMapper(Component):
    _name = 'odoo.product.attribute.import.mapper'
    _inherit = 'odoo.import.mapper'
    _apply_on = 'odoo.product.attribute'

    direct = [
        ('name', 'name'),
        ('create_variant', 'create_variant'),
        ('sequence', 'sequence'),
    ]

    @mapping
    def backend_id(self, record):
        return {'backend_id': self.backend_record.id}

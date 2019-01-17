from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping
from odoo.addons.connector.exception import MappingError


class BreastPumpBatchImporter(Component):
    """ Import the distant Odoo Breast Pump.

    For every Breast Pumps in the list, a delayed job is created.
    """
    _name = 'odoo.breast.pump.batch.importer'
    _inherit = 'odoo.delayed.batch.importer'
    _apply_on = ['odoo.breast.pump']

    def _import_record(self, external_id, job_options=None):
        """ Delay the job for the import"""
        super(BreastPumpBatchImporter, self)._import_record(
            external_id, job_options=job_options,
        )

    def run(self, filters=[]):
        """ Run the synchronization"""
        updated_ids = self.backend_adapter.search(filters)

        for updated in updated_ids:
            self._import_record(updated)


class BreastPumpImporter(Component):
    _name = 'odoo.breast.pump.importer'
    _inherit = 'odoo.importer'
    _apply_on = ['odoo.breast.pump']

    def _import_dependencies(self):
        """ Import the partner dependencies for the record"""
        record = self.odoo_record
        # Import product
        if record.get('product_id'):
            self._import_dependency(record.get('product_id')[0], 'odoo.product.product')


class BreastPumpImportMapper(Component):
    _name = 'odoo.breast.pump.import.mapper'
    _inherit = 'odoo.import.mapper'
    _apply_on = 'odoo.breast.pump'

    direct = [
        ('manufacturing_date', 'manufacturing_date'),
        ('name', 'name'),
        ('warrantly_till', 'warrantly_till'),
    ]

    @mapping
    def backend_id(self, record):
        return {'backend_id': self.backend_record.id}

    @mapping
    def product_id(self, record):
        if not record.get('product_id'):
            return
        binder = self.binder_for('odoo.product.product')
        product_binding = binder.to_internal(record['product_id'][0])

        if not product_binding:
            raise MappingError("The product with "
                               "distant Odoo id %s is not import." %
                               record['product_id'][0])

        product = product_binding.odoo_id
        return {
            'product_id': product.id,
        }

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping
from odoo.addons.connector.exception import MappingError


class ProductBrandBatchImporter(Component):
    """ Import the distant Odoo Product Brand.

    For every Product Brands in the list, a delayed job is created.
    """
    _name = 'odoo.product.brand.batch.importer'
    _inherit = 'odoo.delayed.batch.importer'
    _apply_on = ['odoo.product.brand']

    def _import_record(self, external_id, job_options=None):
        """ Delay the job for the import"""
        super(ProductBrandBatchImporter, self)._import_record(
            external_id, job_options=job_options,
        )

    def run(self, filters=[]):
        """ Run the synchronization"""
        updated_ids = self.backend_adapter.search(filters)

        for updated in updated_ids:
            self._import_record(updated)


class ProductBrandImporter(Component):
    _name = 'odoo.product.brand.importer'
    _inherit = 'odoo.importer'
    _apply_on = ['odoo.product.brand']

    def _import_dependencies(self):
        """ Import the partner dependencies for the record"""
        record = self.odoo_record
        # Import partner
        if record.get('partner_id'):
            self._import_dependency(record.get('partner_id')[0], 'odoo.res.partner')


class ProductBrandImportMapper(Component):
    _name = 'odoo.prdouct.brand.import.mapper'
    _inherit = 'odoo.import.mapper'
    _apply_on = 'odoo.product.brand'

    direct = [
        ('name', 'name'),
        ('description', 'description'),
        ('logo', 'logo'),
    ]

    @mapping
    def backend_id(self, record):
        return {'backend_id': self.backend_record.id}

    @mapping
    def partner_id(self, record):
        if not record.get('partner_id'):
            return
        binder = self.binder_for('odoo.res.partner')
        partner_binding = binder.to_internal(record['partner_id'][0])

        if not partner_binding:
            raise MappingError("The partner with "
                               "distant Odoo id %s is not import." %
                               record['partner_id'][0])

        partner = partner_binding.odoo_id
        return {
            'partner_id': partner.id,
        }

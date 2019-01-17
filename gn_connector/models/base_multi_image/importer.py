from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping
from odoo.addons.connector.exception import MappingError


class ImageBatchImporter(Component):
    """ Import the distant Odoo Images.

    For every Images in the list, a delayed job is created.
    """
    _name = 'odoo.base_multi_image.image.batch.importer'
    _inherit = 'odoo.delayed.batch.importer'
    _apply_on = ['odoo.base_multi_image.image']

    def _import_record(self, external_id, job_options=None):
        """ Delay the job for the import"""
        super(ImageBatchImporter, self)._import_record(
            external_id, job_options=job_options,
        )

    def run(self, filters=[]):
        """ Run the synchronization"""
        updated_ids = self.backend_adapter.search(filters)

        for updated in updated_ids:
            self._import_record(updated)


class ImageImporter(Component):
    _name = 'odoo.base_multi_image.image.importer'
    _inherit = 'odoo.importer'
    _apply_on = ['odoo.base_multi_image.image']

    def _import_dependencies(self):
        """ Import the attribute dependencies for the record"""
        record = self.odoo_record
        # import product attribute
        if record.get('product_variant_ids'):
            for variant_id in record.get('product_variant_ids'):
                self._import_dependency(variant_id, 'odoo.product.product')


class ImageImportMapper(Component):
    _name = 'odoo.base_multi_image.image.import.mapper'
    _inherit = 'odoo.import.mapper'
    _apply_on = 'odoo.base_multi_image.image'

    direct = [
        ('owner_model', 'owner_model'),
        ('storage', 'storage'),
        ('filename', 'filename'),
        ('comments', 'comments'),
        ('sequence', 'sequence'),
        ('name', 'name'),
        ('file_db_store', 'file_db_store'),
    ]

    @mapping
    def backend_id(self, record):
        return {'backend_id': self.backend_record.id}

    @mapping
    def product_variant_ids(self, record):
        if not record.get('product_variant_ids'):
            return
        binder = self.binder_for('odoo.product.product')
        variant_ids = []
        for variant in record.get('product_variant_ids'):
            variant_binding = binder.to_internal(variant)

            if not variant_binding:
                raise MappingError("The product with "
                                   "distant Odoo id %s is not import." %
                                   variant)

            variant_ids.append(variant_binding.odoo_id)
        return {
            'product_variant_ids': [(6, 0, variant_ids)]
        }

    @mapping
    def owner_id(self, record):
        if not record.get('owner_model') or not record.get('owner_id'):
            return
        binding_model = record.get('owner_model')
        binding_id = record.get('owner_id')
        binder = self.binder_for('odoo.%s' % binding_model)
        if not binder:
            return

        record_binding = binder.to_internal(binding_id)
        if not record_binding:
            raise MappingError("The %s with "
                               "distant Odoo id %s is not import." % (
                                    binding_model,
                                    binding_id,
                                )
            )

        return {
            'owner_id': record_binding.odoo_id.id,
        }

    @mapping
    def owner_ref_id(self, record):
        if not record.get('owner_model') or not record.get('owner_id'):
            return

        return {
            'owner_ref_id': '%s,%s' % (
                record.get('owner_model'),
                self.owner_id(record).get('owner_id'),
            )
        }

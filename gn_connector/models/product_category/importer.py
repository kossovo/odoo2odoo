from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping
from odoo.addons.connector.exception import MappingError



class ProductCategoryBatchImporter(Component):
    """ Import the distant Odoo Product Category Values.

    For every product Category Values in the list, a delayed job is created.
    """
    _name = 'odoo.product.category.batch.importer'
    _inherit = 'odoo.delayed.batch.importer'
    _apply_on = ['odoo.product.category']

    def _import_record(self, external_id, job_options=None):
        """ Delay the job for the import"""
        super(ProductCategoryBatchImporter, self)._import_record(
            external_id, job_options=job_options,
        )

    def run(self, filters=[]):
        """ Run the synchronization"""
        updated_ids = self.backend_adapter.search(filters)

        binder = self.binder_for()

        for updated in updated_ids:
            record = binder.to_internal(updated)
            if not record:
                adapter = self.component(usage='backend.adapter')
                record_dict = adapter.read(updated)
                for r_dict in record_dict:
                    domain = [('name', '=', r_dict['name'])]
                    if r_dict['parent_id']:
                        domain.append(('parent_id', '=', binder.to_internal(r_dict['parent_id'][0]).id  ))
                    exists = self.env['product.category'].search(domain)
                    if exists:
                        data = {
                            'odoo_id': exists[0].id,
                            'backend_id': self.backend_record.id,
                        }
                        record = self.model.create(data)
                        binder.bind(updated, record)
            self._import_record(updated)


class ProductCategoryImporter(Component):
    _name = 'odoo.product.category.importer'
    _inherit = 'odoo.importer'
    _apply_on = ['odoo.product.category']

    def _import_dependencies(self):
        """ Import the attribute dependencies for the record"""
        record = self.odoo_record
        # import product attribute
        if record.get('parent_id'):
            self._import_dependency(record.get('parent_id')[0], 'odoo.product.category')


class ProductCategoryImportMapper(Component):
    _name = 'odoo.product.category.import.mapper'
    _inherit = 'odoo.import.mapper'
    _apply_on = 'odoo.product.category'

    direct = [
        ('name', 'name'),
        ('complete_name', 'complete_name'),
    ]

    @mapping
    def backend_id(self, record):
        return {'backend_id': self.backend_record.id}

    @mapping
    def parent_id(self, record):
        return self._get_many2one_internal_id(record, 'odoo.product.category', 'parent_id')

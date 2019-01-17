from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping
from odoo.addons.connector.exception import MappingError


class ProductUoMBatchImporter(Component):
    """ Import the distant Odoo Product UoM.

    For every product UoM in the list, a delayed job is created.
    """
    _name = 'odoo.product.uom.batch.importer'
    _inherit = 'odoo.delayed.batch.importer'
    _apply_on = ['odoo.product.uom']

    def _import_record(self, external_id, job_options=None):
        """ Delay the job for the import"""
        super(ProductUoMBatchImporter, self)._import_record(
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
                exists = self.env['product.uom'].search([('name', '=', record_dict[0]['name'])])
                if exists:
                    data = {
                        'odoo_id': exists[0].id,
                        'backend_id': self.backend_record.id,
                    }
                    record = self.model.create(data)
                    binder.bind(updated, record)
            self._import_record(updated)


class ProductUoMImporter(Component):
    _name = 'odoo.product.uom.importer'
    _inherit = 'odoo.importer'
    _apply_on = ['odoo.product.uom']

    def _import_dependencies(self):
        """ Import the attribute dependencies for the record"""
        record = self.odoo_record
        # import product UoM Category
        if record.get('category_id'):
            self._import_dependency(record.get('category_id')[0], 'odoo.product.uom.categ')


class ProductUomImportMapper(Component):
    _name = 'odoo.product.uom.import.mapper'
    _inherit = 'odoo.import.mapper'
    _apply_on = 'odoo.product.uom'

    direct = [
        ('name', 'name'),
        ('factor', 'factor'),
        ('rounding', 'rounding'),
        ('active', 'active'),
        ('uom_type', 'uom_type'),
    ]

    @mapping
    def backend_id(self, record):
        return {'backend_id': self.backend_record.id}

    @mapping
    def category_id(self, record):
        if not record.get('category_id'):
            return
        binder = self.binder_for('odoo.product.uom.categ')
        category_binding = binder.to_internal(record['category_id'][0])

        if not category_binding:
            raise MappingError("The product category with "
                               "distant Odoo id %s is not import." %
                               record['category_id'][0])

        category = category_binding.odoo_id
        return {
            'category_id': category.id,
        }

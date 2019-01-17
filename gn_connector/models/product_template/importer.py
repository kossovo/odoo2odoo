from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping
from odoo.addons.connector.exception import MappingError


class ProductTemplateBatchImporter(Component):
    """ Import the distant Odoo Product Template.

    For every Product Templaes in the list, a delayed job is created.
    """
    _name = 'odoo.product.template.batch.importer'
    _inherit = 'odoo.delayed.batch.importer'
    _apply_on = ['odoo.product.template']

    def _import_record(self, external_id, job_options=None):
        """ Delay the job for the import"""
        super(ProductTemplateBatchImporter, self)._import_record(
            external_id, job_options=job_options,
        )

    def run(self, filters=[]):
        """ Run the synchronization"""
        offset = 0

        updated_ids = self.backend_adapter.search(filters, limit=100, offset=offset)
        while updated_ids:
            for updated in updated_ids:
                self._import_record(updated)
            offset += 100
            updated_ids = self.backend_adapter.search(filters, limit=100, offset=offset)


class ProductTemplateImporter(Component):
    _name = 'odoo.product.template.importer'
    _inherit = 'odoo.importer'
    _apply_on = ['odoo.product.template']

    def _import_dependencies(self):
        """ Import the ependencies for the record"""
        record = self.odoo_record

        depends = [
            ('categ_id', 'odoo.product.category'),
            ('uom_id', 'odoo.product.uom'),
            ('uom_po_id', 'odoo.product.uom'),
            ('pump_set', 'odoo.product.product'),
            ('product_brand_id', 'odoo.product.brand'),
            ('manufacturer', 'odoo.res.partner'),
        ]

        for dep in depends:
            if record.get(dep[0]):
                self._import_dependency(record.get(dep[0])[0], dep[1])

        if record.get('categ_ids'):
            for c in record.get('categ_ids'):
                self._import_dependency(c, 'odoo.product.category')


class ProductTemplateImportMapper(Component):
    _name = 'odoo.product.template.import.mapper'
    _inherit = 'odoo.import.mapper'
    _apply_on = 'odoo.product.template'

    direct = [
        ('name', 'name'),
        ('sequence', 'sequence'),
        ('description', 'description'),
        ('description_purchase', 'description_purchase'),
        ('description_sale', 'description_sale'),
        ('type', 'type'),
        ('rental', 'rental'),
        ('list_price', 'list_price'),
        ('cost_price', 'cost_price'),
        ('volume', 'volume'),
        ('weight', 'weight'),
        ('sale_ok', 'sale_ok'),
        ('purchase_ok', 'purchase_ok'),
        ('active', 'active'),
        ('color', 'color'),
        ('service_type', 'service_type'),
        ('description_picking', 'description_picking'),
        ('description_pickingout', 'description_pickingout'),
        ('description_pickingin', 'description_pickingin'),
        ('who_product', 'who_product'),
        ('pro_product', 'pro_product'),
        ('breast_pump', 'breast_pump'),
        ('followup_breast_pump', 'followup_breast_pump'),
        ('caution_amount', 'caution_amount'),
        ('compact_breast_pump', 'compact_breast_pump'),
        ('silent_breast_pump', 'silent_breast_pump'),
        ('breast_pump_power_type', 'breast_pump_power_type'),
        ('return_indications', 'return_indications'),
        ('manufacturer_pname', 'manufacturer_pname'),
        ('manufacturer_pref', 'manufacturer_pref'),
        ('manufacturer_purl', 'manufacturer_purl'),
        # ('purchase_method', 'purchase_method'),
        ('code_prefix', 'code_prefix'),
    ]

    @mapping
    def backend_id(self, record):
        return {'backend_id': self.backend_record.id}

    @mapping
    def categ_id(self, record):
        return self._get_many2one_internal_id(record, 'odoo.product.category', 'categ_id')

    @mapping
    def categ_ids(self, record):
        categ_ids = []
        for categ in record.get('categ_ids', []):
            binder = self.binder_for('odoo.product.category')
            model_binding = binder.to_internal(categ)

            if not model_binding:
                raise MappingError(
                    "The odoo.product.category with distant Odoo id %s is not import." % (
                        categ)
                )
            else:
                categ_ids.append(model_binding.odoo_id.id)

        return {'categ_ids': [(6, 0, categ_ids)]}

    @mapping
    def uom_id(self, record):
        return self._get_many2one_internal_id(record, 'odoo.product.uom', 'uom_id')

    @mapping
    def uom_po_id(self, record):
        return self._get_many2one_internal_id(record, 'odoo.product.uom', 'uom_po_id')

    @mapping
    def pump_set(self, record):
        return self._get_many2one_internal_id(record, 'odoo.product.product', 'pump_set')

    @mapping
    def product_brand_id(self, record):
        return self._get_many2one_internal_id(record, 'odoo.product.brand', 'product_brand_id')

    @mapping
    def manufacturer(self, record):
        return self._get_many2one_internal_id(record, 'odoo.res.partner', 'manufacturer')

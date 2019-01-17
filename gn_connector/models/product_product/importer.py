from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping


class ProductProductBatchImporter(Component):
    """ Import the distant Odoo Product Product.

    For every Products in the list, a delayed job is created.
    """
    _name = 'odoo.product.product.batch.importer'
    _inherit = 'odoo.delayed.batch.importer'
    _apply_on = ['odoo.product.product']

    def _import_record(self, external_id, job_options=None):
        """ Delay the job for the import"""
        super(ProductProductBatchImporter, self)._import_record(
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


class ProductProductImporter(Component):
    _name = 'odoo.product.product.importer'
    _inherit = 'odoo.importer'
    _apply_on = ['odoo.product.product']

    def _import_dependencies(self):
        """ Import the dependencies for the record"""
        record = self.odoo_record

        if record.get('product_tmpl_id'):
            self._import_dependency(record.get('product_tmpl_id')[0], 'odoo.product.template')

        # import product attribute value
        if record.get('attribute_value_ids'):
            for value_id in record.get('attribute_value_ids'):
                self._import_dependency(value_id, 'odoo.product.attribute.value')

    def _after_import(self, binding):
        """
        Remove autocreated product.product
        :param binding:
        :return:
        """
        product_ids = self.env['product.product'].search([('product_tmpl_id', '=', binding.odoo_id.product_tmpl_id.id)])
        for product in product_ids:
            if not (self.env['odoo.product.product'].search([('odoo_id', '=', product.id)])):
                product.unlink()


class ProductProductImportMapper(Component):
    _name = 'odoo.product.product.import.mapper'
    _inherit = 'odoo.import.mapper'
    _apply_on = 'odoo.product.product'

    direct = [
        ('default_code', 'default_code'),
        ('barcode', 'barcode'),
        ('manual_code', 'manual_code'),
        # Template fields
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
        # ('tracking', 'tracking'),
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
    def product_tmpl_id(self, record):
        return self._get_many2one_internal_id(record, 'odoo.product.template', 'product_tmpl_id')

    @mapping
    def attribute_value_ids(self, record):
        values = []
        binder = self.binder_for('odoo.product.attribute.value')
        if record.get('attribute_value_ids'):
            for value_id in record.get('attribute_value_ids'):
                values.append(binder.to_internal(value_id).id)

        return {'attribute_value_ids': [(6, 0, values)]}
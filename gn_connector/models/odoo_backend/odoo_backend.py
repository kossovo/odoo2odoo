from datetime import datetime

from odoo import models
from odoo import fields
from odoo import api
from odoo import exceptions
from odoo import _

from odoo.addons.component.core import Component


class BackendOdoo(models.Model):
    _inherit = 'odoo.backend'

    instance_code = fields.Char(
        string='Company code',
        required=True,
    )
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('checked', 'Checked'),
            ('production', 'Production'),
        ],
        default='draft',
        string='Status',
        required=True,
    )

    @api.multi
    def button_reset_to_draft(self):
        self.ensure_one()
        self.write({'state': 'draft'})

    @api.multi
    def _check_connection(self):
        self.ensure_one()
        with self.work_on('odoo.backend') as work:
            component = work.component_by_name(name='odoo.adapter.test')

    @api.multi
    def button_check_connection(self):
        try:
            self._check_connection()
            # raise exceptions.UserError(_('Connection successful'))
            self.write({'state': 'checked'})
        except Exception as e:
            raise exceptions.UserError(_('Connection error: %s') % str(e))

    @api.multi
    def synchronize_base_data(self):
        for backend in self:
            for model_name in [
                'odoo.res.lang',
                'odoo.res.country',
                'odoo.product.uom.categ',
            ]:
                with backend.work_on(model_name) as work:
                    importer = work.component(usage='auto.matching.importer')
                    importer.run()
            backend.write({'state': 'production'})
        return True

    import_product_data_from_date = fields.Datetime(
        string='Last date of import product data',
    )
    import_products_from_date = fields.Datetime(
        string='Last date of import products',
    )
    import_simple_delivery_from_date = fields.Datetime(
        string='Import Simple Delivery from date',
    )

    # ### Technical fields
    import_uom_from_date = fields.Datetime(
        string='Import UoM from date',
    )
    import_product_categ_from_date = fields.Datetime(
        string='Import Product Category from date',
    )
    import_product_attribute_from_date = fields.Datetime(
        string='Import Product Attributes from date',
    )
    import_product_attr_value_from_date = fields.Datetime(
        string='Import Product Attribute Value from date',
    )
    import_product_brand_from_date = fields.Datetime(
        string='Import Product Brand from date',
    )
    import_product_template_from_date = fields.Datetime(
        string='Import Product Template from date',
    )
    import_product_attr_line_from_date = fields.Datetime(
        string='Import Product Attribute Line from date',
    )
    import_product_product_from_date = fields.Datetime(
        string='Import Product from date',
    )
    import_product_image_from_date = fields.Datetime(
        string='Import Product image from date',
    )

    # """
    # Product Data Imports
    # """
    # @api.model
    # def _scheduler_import_product_data(self):
    #     for backend in self.search([]):
    #         backend.import_product_data()
    #         backend.import_products()
    #
    @api.multi
    def import_product_data(self):
        current_date = fields.Datetime.to_string(datetime.now())
        product_data = [
            # UoMs
            ('odoo.product.uom', 'import_uom_from_date'),
            # Categories
            ('odoo.product.category', 'import_product_categ_from_date'),
            # Attributes
            ('odoo.product.attribute', 'import_product_attribute_from_date'),
            # Attribute values
            ('odoo.product.attribute.value', 'import_product_attr_value_from_date'),
            # Product Brands
            ('odoo.product.brand', 'import_product_brand_from_date'),
        ]

        for model, date_field in product_data:
            self._import_from_date(model, date_field)

        self.import_product_data_from_date = current_date

        return True

    @api.multi
    def import_products(self):
        current_date = fields.Datetime.to_string(datetime.now())
        product_data = [
            # Product Templates
            ('odoo.product.template', 'import_product_template_from_date'),
            # Products
            ('odoo.product.product', 'import_product_product_from_date'),
            # # Product Attribute Lines
            ('odoo.product.attribute.line', 'import_product_attr_line_from_date'),
            # Product images
            ('odoo.base_multi_image.image', 'import_product_image_from_date'),
        ]

        for model, date_field in product_data:
            self._import_from_date(model, date_field)

        self.import_products_from_date = current_date

        return True

    """
    Simple delivery
    """
    @api.model
    def _scheduler_import_simple_delivery(self):
        for backend in self.search([]):
            backend.import_simple_delivery()

    @api.multi
    def import_simple_delivery(self):
        self._import_from_date('odoo.simple.delivery', 'import_simple_delivery_from_date')


class NoModelAdapter(Component):
    """ Used to test the connection """
    _name = 'odoo.adapter.test'
    _inherit = 'odoo.adapter'
    _apply_on = 'odoo.backend'
    _odoo_model = ''

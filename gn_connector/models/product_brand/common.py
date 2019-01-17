import logging

from odoo import models
from odoo import fields

from odoo.addons.component.core import Component

_logger = logging.getLogger(__name__)


class OdooProductBrand(models.Model):
    _name = 'odoo.product.brand'
    _inherit = 'odoo.binding'
    _inherits = {'product.brand': 'odoo_id'}

    odoo_id = fields.Many2one(
        comodel_name='product.brand',
        string='Product Brand',
        required=True,
        ondelete='cascade',
    )


class ProductBrand(models.Model):
    _inherit = 'product.brand'

    odoo_bind_ids = fields.One2many(
        comodel_name='odoo.product.brand',
        inverse_name='odoo_id',
        string='Odoo Bindings',
    )


class ProductBrandAdapter(Component):
    _name = 'odoo.product.brand.adapter'
    _inherit = 'odoo.adapter'
    _apply_on = 'odoo.product.brand'

    _odoo_model = 'product.brand'

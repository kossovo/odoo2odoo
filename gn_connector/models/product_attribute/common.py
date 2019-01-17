import logging

from odoo import models
from odoo import fields

from odoo.addons.component.core import Component

_logger = logging.getLogger(__name__)


class OdooProductAttribute(models.Model):
    _name = 'odoo.product.attribute'
    _inherit = 'odoo.binding'
    _inherits = {'product.attribute': 'odoo_id'}

    odoo_id = fields.Many2one(
        comodel_name='product.attribute',
        string='Product Attribute',
        required=True,
        ondelete='cascade',
    )


class ProductAttribute(models.Model):
    _inherit = 'product.attribute'

    odoo_bind_ids = fields.One2many(
        comodel_name='odoo.product.attribute',
        inverse_name='odoo_id',
        string='Odoo Bindings',
    )


class ProductAttributeAdapter(Component):
    _name = 'odoo.product.attribute.adapter'
    _inherit = 'odoo.adapter'
    _apply_on = 'odoo.product.attribute'

    _odoo_model = 'product.attribute'

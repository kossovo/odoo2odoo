import logging

from odoo import models
from odoo import fields

from odoo.addons.component.core import Component

_logger = logging.getLogger(__name__)


class OdooProductAttributeValue(models.Model):
    _name = 'odoo.product.attribute.value'
    _inherit = 'odoo.binding'
    _inherits = {'product.attribute.value': 'odoo_id'}

    odoo_id = fields.Many2one(
        comodel_name='product.attribute.value',
        string='Product Attribute Value',
        required=True,
        ondelete='cascade',
    )


class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'

    odoo_bind_ids = fields.One2many(
        comodel_name='odoo.product.attribute.value',
        inverse_name='odoo_id',
        string='Odoo Bindings',
    )


class ProductAttributeValueAdapter(Component):
    _name = 'odoo.product.attribute.value.adapter'
    _inherit = 'odoo.adapter'
    _apply_on = 'odoo.product.attribute.value'

    _odoo_model = 'product.attribute.value'

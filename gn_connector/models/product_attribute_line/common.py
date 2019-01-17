import logging

from odoo import models
from odoo import fields

from odoo.addons.component.core import Component

_logger = logging.getLogger(__name__)


class OdooProductAttributeLine(models.Model):
    _name = 'odoo.product.attribute.line'
    _inherit = 'odoo.binding'
    _inherits = {'product.attribute.line': 'odoo_id'}

    odoo_id = fields.Many2one(
        comodel_name='product.attribute.line',
        string='Product Attribute Line',
        required=True,
        ondelete='cascade',
    )


class ProductAttributeLine(models.Model):
    _inherit = 'product.attribute.line'

    odoo_bind_ids = fields.One2many(
        comodel_name='odoo.product.attribute.line',
        inverse_name='odoo_id',
        string='Odoo Bindings',
    )


class ProductAttributeLineAdapter(Component):
    _name = 'odoo.product.attribute.line.adapter'
    _inherit = 'odoo.adapter'
    _apply_on = 'odoo.product.attribute.line'

    _odoo_model = 'product.attribute.line'

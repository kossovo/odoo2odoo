import logging

from odoo import models
from odoo import fields

from odoo.addons.component.core import Component

_logger = logging.getLogger(__name__)


class OdooProductProduct(models.Model):
    _name = 'odoo.product.product'
    _inherit = 'odoo.binding'
    _inherits = {'product.product': 'odoo_id'}

    odoo_id = fields.Many2one(
        comodel_name='product.product',
        string='Product Product',
        required=True,
        ondelete='cascade',
    )


class ProductProduct(models.Model):
    _inherit = 'product.product'

    odoo_bind_ids = fields.One2many(
        comodel_name='odoo.product.product',
        inverse_name='odoo_id',
        string='Odoo Bindings',
    )


class ProductProductAdapter(Component):
    _name = 'odoo.product.product.adapter'
    _inherit = 'odoo.adapter'
    _apply_on = 'odoo.product.product'

    _odoo_model = 'product.product'

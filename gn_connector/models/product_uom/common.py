import logging

from odoo import models
from odoo import fields

from odoo.addons.component.core import Component

_logger = logging.getLogger(__name__)


class OdooProductUoM(models.Model):
    _name = 'odoo.product.uom'
    _inherit = 'odoo.binding'
    _inherits = {'product.uom': 'odoo_id'}

    odoo_id = fields.Many2one(
        comodel_name='product.uom',
        string='Product UoM',
        required=True,
        ondelete='cascade',
    )


class ProductUom(models.Model):
    _inherit = 'product.uom'

    odoo_bind_ids = fields.One2many(
        comodel_name='odoo.product.uom',
        inverse_name='odoo_id',
        string='Odoo Bindings',
    )


class ProductUomAdapter(Component):
    _name = 'odoo.product.uom.adapter'
    _inherit = 'odoo.adapter'
    _apply_on = 'odoo.product.uom'

    _odoo_model = 'product.uom'

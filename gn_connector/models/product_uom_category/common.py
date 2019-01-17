import logging

from odoo import models
from odoo import fields

from odoo.addons.component.core import Component

_logger = logging.getLogger(__name__)


class OdooProductUoMCateg(models.Model):
    _name = 'odoo.product.uom.categ'
    _inherit = 'odoo.binding'
    _inherits = {'product.uom.categ': 'odoo_id'}

    odoo_id = fields.Many2one(
        comodel_name='product.uom.categ',
        string='Product UoM Category',
        required=True,
        ondelete='cascade',
    )


class ProductUomCateg(models.Model):
    _inherit = 'product.uom.categ'

    odoo_bind_ids = fields.One2many(
        comodel_name='odoo.product.uom.categ',
        inverse_name='odoo_id',
        string='Odoo Bindings',
    )


class ProductUomCategAdapter(Component):
    _name = 'odoo.product.uom.categ.adapter'
    _inherit = 'odoo.adapter'
    _apply_on = 'odoo.product.uom.categ'

    _odoo_model = 'product.uom.categ'

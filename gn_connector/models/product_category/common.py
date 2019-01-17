import logging

from odoo import models, fields
from odoo.addons.component.core import Component

_logger = logging.getLogger(__name__)


class OdooProductCategory(models.Model):
    _name = 'odoo.product.category'
    _inherit = 'odoo.binding'
    _inherits = {'product.category': 'odoo_id'}

    odoo_id = fields.Many2one(
        comodel_name='product.category',
        string='Product Category',
        required=True,
        ondelete='cascade',
    )
    odoo_parent_id = fields.Many2one(
        comodel_name='odoo.product.category',
        string='Distant Odoo Parent Category',
        ondelete='cascade',
    )
    odoo_child_ids = fields.One2many(
        comodel_name='odoo.product.category',
        inverse_name='odoo_parent_id',
        string='Distant Odoo Child Categories',
    )


class ProductCategory(models.Model):
    _inherit = 'product.category'

    odoo_bind_ids = fields.One2many(
        comodel_name='odoo.product.category',
        inverse_name='odoo_id',
        string='Odoo Bindings',
    )


class ProductCategoryAdapter(Component):
    _name = 'odoo.product.category.adapter'
    _inherit = 'odoo.adapter'
    _apply_on = 'odoo.product.category'

    _odoo_model = 'product.category'
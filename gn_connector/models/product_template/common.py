import logging

from odoo import models
from odoo import fields

from odoo.addons.component.core import Component

_logger = logging.getLogger(__name__)


class OdooProductTemplate(models.Model):
    _name = 'odoo.product.template'
    _inherit = 'odoo.binding'
    _inherits = {'product.template': 'odoo_id'}

    odoo_id = fields.Many2one(
        comodel_name='product.template',
        string='Product Template',
        required=True,
        ondelete='cascade',
    )


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    odoo_bind_ids = fields.One2many(
        comodel_name='odoo.product.template',
        inverse_name='odoo_id',
        string='Odoo Bindings',
    )


class ProductTemplateAdapter(Component):
    _name = 'odoo.product.template.adapter'
    _inherit = 'odoo.adapter'
    _apply_on = 'odoo.product.template'

    _odoo_model = 'product.template'

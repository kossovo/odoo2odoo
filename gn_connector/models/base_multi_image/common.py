import logging

from odoo import models
from odoo import fields

from odoo.addons.component.core import Component

_logger = logging.getLogger(__name__)


class OdooImage(models.Model):
    _name = 'odoo.base_multi_image.image'
    _inherit = 'odoo.binding'
    _inherits = {'base_multi_image.image': 'odoo_id'}

    odoo_id = fields.Many2one(
        comodel_name='base_multi_image.image',
        string='Image',
        required=True,
        ondelete='cascade',
    )


class Image(models.Model):
    _inherit = 'base_multi_image.image'

    odoo_bind_ids = fields.One2many(
        comodel_name='odoo.base_multi_image.image',
        inverse_name='odoo_id',
        string='Odoo Bindings',
    )


class ImageAdapter(Component):
    _name = 'odoo.base_multi_image.image.adapter'
    _inherit = 'odoo.adapter'
    _apply_on = 'odoo.base_multi_image.image'

    _odoo_model = 'base_multi_image.image'

import logging

from odoo import models
from odoo import fields

from odoo.addons.component.core import Component

_logger = logging.getLogger(__name__)


class OdooBreastPump(models.Model):
    _name = 'odoo.breast.pump'
    _inherit = 'odoo.binding'
    _inherits = {'breast.pump': 'odoo_id'}

    odoo_id = fields.Many2one(
        comodel_name='breast.pump',
        string='Breast Pump',
        required=True,
        ondelete='cascade',
    )


class BreastPump(models.Model):
    _inherit = 'breast.pump'

    odoo_bind_ids = fields.One2many(
        comodel_name='odoo.breast.pump',
        inverse_name='odoo_id',
        string='Odoo Bindings',
    )


class BreastPumpAdapter(Component):
    _name = 'odoo.breast.pump.adapter'
    _inherit = 'odoo.adapter'
    _apply_on = 'odoo.breast.pump'

    _odoo_model = 'stock.production.lot'

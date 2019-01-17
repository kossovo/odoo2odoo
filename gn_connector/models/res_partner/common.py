import logging

from odoo import models
from odoo import fields
from odoo import api

from odoo.addons.component.core import Component
from odoo.addons.queue_job.job import job, related_action

_logger = logging.getLogger(__name__)


class OdooResPartner(models.Model):
    _name = 'odoo.res.partner'
    _inherit = 'odoo.binding'
    _inherits = {'res.partner': 'odoo_id'}

    odoo_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner',
        required=True,
        ondelete='cascade',
    )

    # _sql_constraints = [
    #     ('odoo_uniq', 'unique(backend_id, odoo_id)',
    #      'A Distant Odoo bingding for this partner already exists.')
    # ]

    @job(default_channel='root.odoo')
    @related_action(action='related_action_unwrap_binding')
    @api.multi
    def export_record(self):
        """
        Export a waiting simple delivery
        :return:
        """
        self.ensure_one()
        with self.backend_id.work_on(self._name) as work:
            exporter = work.component(usage='res.partner.exporter')
            return exporter.run(self)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    odoo_bind_ids = fields.One2many(
        comodel_name='odoo.res.partner',
        inverse_name='odoo_id',
        string='Odoo Bindings',
    )


class ResPartnerAdapter(Component):
    _name = 'odoo.res.partner.adapter'
    _inherit = 'odoo.adapter'
    _apply_on = 'odoo.res.partner'

    _odoo_model = 'res.partner'

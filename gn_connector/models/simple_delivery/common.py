import logging

from odoo import api
from odoo import models
from odoo import fields
from odoo.addons.component.core import Component
from odoo.addons.queue_job.job import job, related_action
from odoo.addons.connector.exception import IDMissingInBackend


_logger = logging.getLogger(__name__)


class OdooSimpleDelivery(models.Model):
    _name = 'odoo.simple.delivery'
    _inherit = 'odoo.binding'
    _inherits = {'simple.delivery': 'odoo_id'}
    _description = 'Odoo Simple Delivery -> Stock picking'

    odoo_id = fields.Many2one(
        comodel_name='simple.delivery',
        string='Simple delivery',
        required=True,
        ondelete='cascade',
    )

    _sql_constraints = [
        ('odoo_uniq', 'unique(backend_id, odoo_id)',
         'A Distant Odoo bingding for this delivery already exists.')
    ]

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
            exporter = work.component(usage='simple.delivery.exporter')
            return exporter.run(self)


class SimpleDelivery(models.Model):
    _inherit = 'simple.delivery'

    odoo_bind_ids = fields.One2many(
        comodel_name='odoo.simple.delivery',
        inverse_name='odoo_id',
        string='Odoo bindings',
    )

    @api.multi
    def to_waiting(self):
        """
        Change the state of the delivery to ``waiting``
        :return:
        """
        res = super(SimpleDelivery, self).to_waiting()

        for record in self:
            self._event('on_delivery_waiting').notify(record)

        return res


class SimpleDeliveryAdapter(Component):
    _name = 'odoo.delivery.adapter'
    _inherit = 'odoo.adapter'
    _apply_on = 'odoo.simple.delivery'

    _odoo_model = 'stock.picking'

    def action_confirm(self, id):
        return self._call(
            self._odoo_model,
            'action_confirm',
            [int(id)],
        )

    def action_assign(self, id):
        return self._call(
            self._odoo_model,
            'action_assign',
            [int(id)],
        )


class OdooSimpleDeliveryLine(models.Model):
    _name = 'odoo.simple.delivery.line'
    _inherit = 'odoo.binding'
    _inherits = {'simple.delivery.line': 'odoo_id'}
    _description = 'Odoo Simple Delivery Line -> Stock move'

    odoo_id = fields.Many2one(
        comodel_name='simple.delivery.line',
        string='Simple delivery line',
        required=True,
        ondelete='cascade',
    )

    _sql_constraints = [
        ('odoo_uniq', 'unique(backend_id, odoo_id)',
         'A Distant Odoo bingding for this delivery line already exists.')
    ]

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
            exporter = work.component(usage='simple.delivery.line.exporter')
            return exporter.run(self)


class SimpleDeliveryLine(models.Model):
    _inherit = 'simple.delivery.line'

    odoo_bind_ids = fields.One2many(
        comodel_name='odoo.simple.delivery.line',
        inverse_name='odoo_id',
        string='Odoo bindings',
    )


class SimpleDeliveryLineAdapter(Component):
    _name = 'odoo.delivery.line.adapter'
    _inherit = 'odoo.adapter'
    _apply_on = 'odoo.simple.delivery.line'

    _odoo_model = 'stock.move'
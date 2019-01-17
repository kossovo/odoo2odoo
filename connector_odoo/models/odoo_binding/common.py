from odoo import models
from odoo import fields
from odoo import api
from odoo.addons.queue_job.job import job, related_action


class OdooBinding(models.AbstractModel):
    """ Abstract Model for the Bindings.

    All the models used as bindings between local Odoo and
    distant Odoo (``odoo.res.partner``, ``odoo.product.product``, ...)
    should ``_inherit`` it."""
    _name = 'odoo.binding'
    _inherit = 'external.binding'
    _description = 'Odoo Binding (abstract)'

    # odoo_id = odoo-side id must be declared in concrete model
    backend_id = fields.Many2one(
        comodel_name='odoo.backend',
        string='Odoo Backend',
        required=True,
        ondelete='restrict',
    )
    external_id = fields.Integer(
        string='ID on distant Odoo',
    )

    _sql_constraints = [
        ('odoo_uniq', 'unique(backend_id, external_id)',
         'A binding already exists wit the same distant Odoo ID'),
    ]

    @job(default_channel='root.odoo')
    @api.model
    def import_batch(self, backend, filters=[]):
        """ Prepare the import of records modified on distant Odoo"""
        with backend.work_on(self._name) as work:
            importer = work.component(usage='batch.importer')
            return importer.run(filters=filters)

    @job(default_channel='root.odoo')
    @api.model
    def import_record(self, backend, external_id, force=False):
        """ Import a distant Odoo record"""
        with backend.work_on(self._name) as work:
            importer = work.component(usage='record.importer')
            return importer.run(external_id, force=force)

    @job(default_channel='root.odoo')
    @related_action(action='related_action_unwrap_binding')
    @api.multi
    def export_record(self, fields=None):
        """ Export a record to distant Odoo """
        self.ensure_one()
        with self.backend_id.work_on(self._name) as work:
            exporter = work.component(usage='odoo.exporter')
            return exporter.run(self)

    @job(default_channel='root.odoo')
    def export_delete_record(self, backend, external_id):
        """ Delete a record on distant Odoo """
        with backend.work_on(self._name) as work:
            deleter = work.component(usage='record.exporter.deleter')
            return deleter.run(external_id)

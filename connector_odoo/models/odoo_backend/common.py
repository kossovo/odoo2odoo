import logging

from contextlib import contextmanager

from datetime import datetime, timedelta
from odoo import models, fields, api

from odoo.addons.connector.models.checkpoint import add_checkpoint
from ...components.backend_adapter import OdooLocation, OdooAPI

_logger = logging.getLogger(__name__)

IMPORT_DELTA_BUFFER = 30    # seconds


class OdooBackend(models.Model):
    _name = 'odoo.backend'
    _description = 'Odoo Backend'
    _inherit = 'connector.backend'

    @api.model
    def select_versions(self):
        """ Available versions in the backend.

        Can be inherited to add custom versions. Using this method
        to add a version from an ``_inherit`` does not constrain
        to redefine teh ``version`` field in the ``_inherit`` model.
        """
        return [('11.0', '11.0+')]

    name = fields.Char(
        string='Name',
        required=True,
    )
    version = fields.Selection(selection='select_versions', required=True)
    location = fields.Char(
        string='Location',
        required=True,
        help="Url to distant Odoo application",
        defaults='localhost'
    )
    port = fields.Char(
        string='Port',
        required=True,
        help="Pour to distant Odoo application",
        defaults=8069,
    )
    username = fields.Char(
        string='Username',
        help="Webservice user",
        required=True,
        defaults='admin',
    )
    password = fields.Char(
        string='Password',
        help="Webservice password",
        required=True,
        defaults='admin',
    )
    database = fields.Char(
        string='Database',
        required=True,
        help="Distant database",
    )

    @contextmanager
    @api.multi
    def work_on(self, model_name, **kwargs):
        self.ensure_one()
        odoo_location = OdooLocation(
            location=self.location,
            port=self.port,
            username=self.username,
            password=self.password,
            database=self.database,
        )
        # We create a Odoo Client API here, so we can create the
        # client once (lazily on the first use) and propagate it
        # through all the sync session, instead of recreating a client
        # in each backend adapter usage.
        with OdooAPI(odoo_location) as odoo_api:
            _super = super(OdooBackend, self)
            # from the components we'll be able to do: self.work.odoo_api
            with _super.work_on(
                model_name, odoo_api=odoo_api, **kwargs) as work:
                yield work

    @api.multi
    def add_checkpoint(self, record):
        self.ensure_one()
        record.ensure_one()
        return add_checkpoint(self.env, record._name, record.id,
                              self._name, self.id)

    @api.multi
    def _import_from_date(self, model, from_date_field):
        import_start_time = datetime.now()
        for backend in self:
            from_date = backend[from_date_field]
            filters = [
                ('write_date', '<=', fields.Datetime.to_string(import_start_time))
            ]
            if from_date:
                filters.append(('write_date', '>=', from_date))

            self.env[model].import_batch(
                backend,
                filters,
            )
        # Record from distant Odoo are imported based on their `created_date`
        # date. This date is set on distant Odoo at the beginning of a
        # transaction, so if the import is run between the beginning and
        # the end of a transaction, the import of a record may be
        # missed. That's why we add a small buffer back in time where
        # the eventually missed records will be retrieved. This also
        # means that we'll have jobs that import twick the same records,
        # but this is not a big deal because the will be skipped when
        # the last `sync_date` is the same.
        next_time = import_start_time - timedelta(seconds=IMPORT_DELTA_BUFFER)
        next_time = fields.Datetime.to_string(next_time)
        self.write({from_date_field: next_time})

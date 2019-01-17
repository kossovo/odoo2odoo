from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping
from odoo.addons.connector.exception import MappingError


class SimpleDeliveryBatchImporter(Component):
    """ Update local from the distant Odoo Delivery.

    For every delivery in the list, a delayed job is created.
    """
    _name = 'odoo.simple.delivery.batch.importer'
    _inherit = 'odoo.delayed.batch.importer'
    _apply_on = ['odoo.simple.delivery']

    def _import_record(self, external_id, job_options=None):
        """ Delay the job for the import"""
        super(SimpleDeliveryBatchImporter, self)._import_record(
            external_id, job_options=job_options,
        )

    def run(self, filters=[]):
        """ Run the synchronization"""
        filters.append(
            ('state', 'in', ['done', 'cancel']),
        )

        # Get all distant ID for each simple.delivery
        existing_ids = self.env['odoo.simple.delivery'].search([
            ('backend_id', '=', self.backend_record.id),
            ('external_id', '!=', False),
        ])
        filters.append(['id', 'in', [x.external_id for x in existing_ids]])

        super(SimpleDeliveryBatchImporter, self).run(filters)


class SimpleDeliveryImporter(Component):
    _name = 'odoo.simple.delivery.importer'
    _inherit = 'odoo.importer'
    _apply_on = ['odoo.simple.delivery']

    def _import_dependencies(self):
        """
        Import update of lines before update the simple delivery.
        :return:
        """
        record = self.odoo_record
        for line_id in record.get('move_lines'):
            self._import_dependency(line_id, 'odoo.simple.delivery.line', always=True)


class SimpleDeliveryImportMapper(Component):
    _name = 'odoo.simple.delivery.import.mapper'
    _inherit = 'odoo.import.mapper'
    _apply_on = 'odoo.simple.delivery'

    direct = [
        ('carrier_tracking_ref', 'tracking_reference'),
        ('scheduled_date', 'expected_date'),
        ('check_amount', 'check_amount'),
    ]

    @mapping
    def state(self, record):
        map_states = {
            'draft': 'draft',
            'waiting': 'waiting',
            'confirmed': 'waiting',
            'assigned': 'waiting',
            'done': 'complete',
            'cancel': 'complete',
        }
        if not record.get('state'):
            return

        return {'state': map_states.get(record.get('state'))}


class SimpleDeliveryLineImporter(Component):
    _name = 'odoo.simple.delivery.line.importer'
    _inherit = 'odoo.importer'
    _apply_on = ['odoo.simple.delivery.line']

    def _import_dependencies(self):
        """ Import the partner dependencies for the record"""
        record = self.odoo_record
        # Import product
        if record.get('breast_pump_id'):
            self._import_dependency(record.get('breast_pump_id')[0], 'odoo.breast.pump')


class SimpleDeliveryLineImportMapper(Component):
    _name = 'odoo.simple.delivery.line.import.mapper'
    _inherit = 'odoo.import.mapper'
    _apply_on = 'odoo.simple.delivery.line'

    direct = [
    ]

    @mapping
    def lot_id(self, record):
        if not record.get('breast_pump_id'):
            return
        binder = self.binder_for('odoo.breast.pump')
        bp_binder = binder.to_internal(record['breast_pump_id'][0])

        if not bp_binder:
            raise MappingError("The breast pump with "
                               "distant Odoo id %s is not import." %
                               record['breast_pump_id'][0])

        breast_pump = bp_binder.odoo_id
        return {
            'breast_pump_id': breast_pump.id,
        }

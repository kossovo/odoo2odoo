from odoo.addons.component.core import Component
from odoo.addons.component_event import skip_if


class OdooBindingSimpleDeliveryListener(Component):
    _name = 'odoo.binding.simple.delivery.listener'
    _inherit = 'base.connector.listener'
    _apply_on = ['odoo.simple.delivery']

    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_record_create(self, record, fields=None):
        record.with_delay().export_record()
        # for line in record.delivery_lines:
        #     line.with_delay().export_record()

    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_record_write(self, record, fields=None):
        record.with_delay().export_record()
        # for line in record.delivery_lines:
        #     line.with_delay().export_record()


class OdooSimpleDeliveryListener(Component):
    _name = 'odoo.simple.delivery.listener'
    _inherit = 'base.connector.listener'
    _apply_on = ['simple.delivery']

    def on_delivery_waiting(self, record):
        if not record.odoo_bind_ids:
            self.delivery_create_bindings(record)

    def delivery_create_bindings(self, delivery):
         """
         Create a ``odoo.simple.delivery` record. This record will then
         be exported to distant Odoo.
         """
         for backend in self.env['odoo.backend'].search([]):
             self.env['odoo.simple.delivery'].create({
                 'backend_id': backend.id,
                 'odoo_id': delivery.id,
             })


class OdooBindingSimpleDeliveryLineListener(Component):
    _name = 'odoo.binding.simple.delivery.line.listener'
    _inherit = 'base.connector.listener'
    _apply_on = ['odoo.simple.delivery.line']

    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_record_create(self, record, fields=None):
        record.export_record()

    # @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    # def on_record_write(self, record, fields=None):
    #     print('on_record_write odoo.simple.delivery.line')
    #     record.with_delay().export_record()


class OdooSimpleDeliveryListener(Component):
    _name = 'odoo.simple.delivery.line.listener'
    _inherit = 'base.connector.listener'
    _apply_on = ['simple.delivery.line']

    def on_delivery_waiting(self, record, fields=None):
        if not record.odoo_bind_ids:
            self.delivery_create_bindings(record)

    def delivery_create_bindings(self, line):
        """
        Create a ``odoo.simple.delivery.line` record. This record will then
        be exported to distant Odoo.
        """
        for backend in self.env['odoo.backend'].search([]):
            self.env['odoo.simple.delivery.line'].create({
                'backend_id': backend.id,
                'odoo_id': line.id,
            })

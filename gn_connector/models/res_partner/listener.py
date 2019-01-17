from odoo.addons.component.core import Component
from odoo.addons.component_event import skip_if


class OdooBindingPartnerListener(Component):
    _name = 'odoo.binding.res.partner.listener'
    _inherit = 'base.connector.listener'
    _apply_on = ['odoo.res.partner']

    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_record_create(self, record, fields=None):
        record.with_delay().export_record()
    #
    # @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    # def on_record_write(self, record, fields=None):
    #     if 'customer' in fields and record.customer:
    #         record.with_delay().export_record()


class OdooSimpleDeliveryListener(Component):
    _name = 'odoo.res.partner.listener'
    _inherit = 'base.connector.listener'
    _apply_on = ['res.partner']

    def on_record_create(self, record, fields=None):
        if not record.odoo_bind_ids:
            self.partner_create_bindings(record)
    #
    # @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    # def on_record_write(self, record, fields=None):
    #     if record.odoo_bind_ids and 'customer' in fields and record.customer:
    #         for binding in record.odoo_bind_ids:
    #             binding.with_delay().export_record()

    def partner_create_bindings(self, partner):
        """
        Create a ``odoo.res.partner` record. This record will then
        be exported to distant Odoo.
        """
        for backend in self.env['odoo.backend'].search([]):
            self.env['odoo.res.partner'].create({
                'backend_id': backend.id,
                'odoo_id': partner.id,
            })

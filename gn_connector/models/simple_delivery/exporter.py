import logging

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping
from odoo.addons.connector.exception import MappingError

_logger = logging.getLogger(__name__)


class OdooSimpleDeliveryExporter(Component):
    """ Export simple delivery to distant Odoo """
    _name = 'odoo.simple.delivery.exporter'
    _inherit = 'odoo.exporter'
    _apply_on = ['odoo.simple.delivery']
    _usage = 'simple.delivery.exporter'

    def _export_dependencies(self):
        """ Export the simple delivery before export lines """
        record = self.binding and self.binding.odoo_id
        if record and record.partner_id:
            self._export_dependency(record.partner_id, 'odoo.res.partner',
                                    component_usage='res.partner.exporter')

    def _after_export(self):
        ext_id = self.binding and self.binding.external_id
        record = self.binding and self.binding.odoo_id
        for line in record.delivery_lines:
            self.env['simple.delivery.line']._event('on_delivery_waiting').notify(line)
        self.backend_adapter.action_confirm(ext_id)
        self.backend_adapter.action_assign(ext_id)


class OdooSimpleDeliveryLineExporter(Component):
    """ Export simple delivery line to distant Odoo"""
    _name = 'odoo.simple.delivery.line.exporter'
    _inherit = 'odoo.exporter'
    _apply_on = ['odoo.simple.delivery.line']
    _usage = 'simple.delivery.line.exporter'

    def _export_dependencies(self):
        """ Export the simple delivery before export lines """
        record = self.binding and self.binding.odoo_id
        if record and record.delivery_id:
            self._export_dependency(record.delivery_id, 'odoo.simple.delivery',
                                    component_usage='simple.delivery.exporter')


class SimpleDeliveryExportMapper(Component):
    _name = 'odoo.simple.delivery.export.mapper'
    _inherit = 'odoo.export.mapper'
    _apply_on = 'odoo.simple.delivery'

    direct = [
        ('tracking_reference', 'carrier_tracking_ref'),
        ('name', 'name'),
    ]

    @mapping
    def company_code(self, record):
        return {'company_code': record.backend_id.instance_code}

    @mapping
    def contract_report(self, record):
        """

        :param record:
        :return:
        """
        contract_report = False
        if record.contract_report:
            contract_report = record.contract_report.decode('utf-8')
        return {'contract_report': contract_report}

    @mapping
    def invoice_report(self, record):
        """

        :param record:
        :return:
        """
        invoice_report = False
        if record.invoice_report:
            invoice_report = record.invoice_report.decode('utf-8')
        return {'invoice_report': invoice_report}

    @mapping
    def origin(self, record):
        """
        Origin = contract name / sgrandale order name
        """
        origin = ''
        if record.contract_id:
            origin = record.contract_id.name
        if record.sale_id:
            if origin:
                origin = '%s / %s' % (
                    origin, record.sale_id.name)
            else:
                origin = record.sale_id.name

        return {'origin': origin}

    @mapping
    def contract_name(self, record):
        """

        :param record:
        :return:
        """
        if record.contract_id:
            return {'contract_name': record.contract_id.name}
        return

    @mapping
    def picking_type(self, record):
        if record.picking_type == 'return_bp':
            return {'picking_type': 'in'}
        else:
            return {'picking_type': 'out'}

    @mapping
    def transporter(self, record):
        if not record.delivery_carrier:
            return
        return {'transporter': record.delivery_carrier.code}

    @mapping
    def partner_id(self, record):
        if not record.partner_id:
            return
        binder = self.binder_for('odoo.res.partner')
        partner_id = binder.to_external(record.partner_id.id, wrap=True)

        if not partner_id:
            raise MappingError("The partner with "
                               "distant Odoo id %s is not export." %
                               record.partner_id.id)

        return {
            'partner_id': partner_id,
        }


class SimpleDeliveryLineExportMapper(Component):
    _name = 'odoo.simple.delivery.line.export.mapper'
    _inherit = 'odoo.export.mapper'
    _apply_on = 'odoo.simple.delivery.line'

    direct = []

    @mapping
    def product_id(self, record):
        if not record.product_id:
            return
        binder = self.binder_for('odoo.product.product')
        product_id = binder.to_external(record.product_id.id, wrap=True)

        if not product_id:
            raise MappingError("The product with "
                               "internal Odoo id %s is not export." %
                               record.product_id.id)

        return {
            'product_id': product_id,
        }

    @mapping
    def product_uom_qty(self, record):
        return {
            'product_uom_qty': record.product_qty,
        }

    @mapping
    def picking_id(self, record): 
        if not record.delivery_id:
            return
        binder = self.binder_for('odoo.simple.delivery')
        picking_id = binder.to_external(record.delivery_id.id, wrap=True)

        if not picking_id:
            raise MappingError("The delivery with "
                               "internal Odoo id %s is not export." %
                               record.delivery_id.id)

        return {
            'picking_id': picking_id,
        }

    @mapping
    def name(self, record):
        if not record.product_id:
            return {'name': ''}
        else:
            return {'name': record.product_id.name}

    @mapping
    def breast_pump_id(self, record):
        if not record.breast_pump_id:
            return

        binder = self.binder_for('odoo.breast.pump')
        breast_pump_id = binder.to_external(record.breast_pump_id.id, wrap=True)

        if not breast_pump_id:
            raise MappingError("The breast pump with "
                               "internal Odoo id %s is not export." %
                               record.breast_pump_id.id)

        return {
            'breast_pump_id': breast_pump_id,
        }

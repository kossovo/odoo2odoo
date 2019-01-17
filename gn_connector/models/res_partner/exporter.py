import logging

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping

_logger = logging.getLogger(__name__)


class OdooResPartnerExporter(Component):
    """ Export partner to distant Odoo """
    _name = 'odoo.res.partner.exporter'
    _inherit = 'odoo.exporter'
    _apply_on = ['odoo.res.partner']
    _usage = 'res.partner.exporter'

    direct = [
        ('name', 'name'),
        ('ref', 'ref'),
        ('website', 'website'),
        ('comment', 'comment'),
        ('barcode', 'barcode'),
        ('customer', 'customer'),
        ('supplier', 'supplier'),
        ('function', 'function'),
        ('street', 'street'),
        ('street2', 'street2'),
        ('zip', 'zip'),
        ('city', 'city'),
        ('email', 'email'),
        ('phone', 'phone'),
        ('mobile', 'mobile'),
        ('is_company', 'is_company'),
        ('company_name', 'company_name'),
        ('firstname', 'firstname'),
        ('lastname', 'lastname'),
        ('manufacturer', 'manufacturer'),
        # ('image', 'image'),
    ]

    def run(self, binding):
        """ Run the job to export the simple delivery"""
        external_id = None
        try:
            data = {}
            for field in self.direct:
                if hasattr(binding.odoo_id, field[1]):
                    data[field[0]] = getattr(binding.odoo_id, field[1])

            if binding.external_id:
                self.backend_adapter.write(binding.external_id, data)
            else:
                external_id = self.backend_adapter.create(data)
        except Exception as e:
            raise

        if external_id:
            self.binder.bind(external_id, binding.id)

# class PartnerImportMapper(Component):
#     _name = 'odoo.res.partner.export.mapper'
#     _inherit = 'odoo.export.mapper'
#     _apply_on = 'odoo.res.partner'
#
#     direct = [
#         ('name', 'name'),
#         ('ref', 'ref'),
#         ('website', 'website'),
#         ('comment', 'comment'),
#         ('barcode', 'barcode'),
#         ('customer', 'customer'),
#         ('supplier', 'supplier'),
#         ('function', 'function'),
#         ('street', 'street'),
#         ('street2', 'street2'),
#         ('zip', 'zip'),
#         ('city', 'city'),
#         ('email', 'email'),
#         ('phone', 'phone'),
#         ('mobile', 'mobile'),
#         ('is_company', 'is_company'),
#         ('company_name', 'company_name'),
#         ('firstname', 'firstname'),
#         ('lastname', 'lastname'),
#         ('manufacturer', 'manufacturer'),
#         ('image', 'image'),
#     ]
#
#     @mapping
#     def backend_id(self, record):
#         return {'backend_id': self.backend_record.id}
#
#     @mapping
#     def state(self, record):
#         if not record.get('state'):
#             return
#         else:
#             state = self.env['res.country.state'].search([
#                 ('name', '=', record.get('state')[1]),
#             ])
#             if not state:
#                 return
#             else:
#                 return {'state': state[0].id}
#
#     @mapping
#     def country_id(self, record):
#         if not record.get('country_id'):
#             return
#         else:
#             country = self.env['res.country'].search([
#                 ('name', '=', record.get('country_id')[1]),
#             ])
#             if not country:
#                 return
#             else:
#                 return {'country_id': country[0].id}
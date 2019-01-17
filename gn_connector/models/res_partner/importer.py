from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping
from odoo.addons.connector.exception import MappingError


class PartnerBatchImporter(Component):
    """ Import the distant Odoo Partner.

    For every Partners in the list, a delayed job is created.
    """
    _name = 'odoo.res.partner.batch.importer'
    _inherit = 'odoo.delayed.batch.importer'
    _apply_on = ['odoo.res.partner']

    def _import_record(self, external_id, job_options=None):
        """ Delay the job for the import"""
        super(PartnerBatchImporter, self)._import_record(
            external_id, job_options=job_options,
        )

    def run(self, filters=[]):
        """ Run the synchronization"""
        updated_ids = self.backend_adapter.search(filters)

        for updated in updated_ids:
            self._import_record(updated)


class PartnerImporter(Component):
    _name = 'odoo.res.partner.importer'
    _inherit = 'odoo.importer'
    _apply_on = ['odoo.res.partner']

    def _import_dependencies(self):
        """ Import the partner dependencies for the record"""
        record = self.odoo_record
        # Import parent partner
        if record.get('parent_id'):
            self._import_dependency(record.get('parent_id')[0], self.model)


class PartnerImportMapper(Component):
    _name = 'odoo.res.partner.import.mapper'
    _inherit = 'odoo.import.mapper'
    _apply_on = 'odoo.res.partner'

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
        ('image', 'image'),
    ]

    @mapping
    def backend_id(self, record):
        return {'backend_id': self.backend_record.id}

    @mapping
    def state(self, record):
        if not record.get('state'):
            return
        else:
            state = self.env['res.country.state'].search([
                ('name', '=', record.get('state')[1]),
            ])
            if not state:
                return
            else:
                return {'state': state[0].id}

    @mapping
    def country_id(self, record):
        if not record.get('country_id'):
            return
        else:
            country = self.env['res.country'].search([
                ('name', '=', record.get('country_id')[1]),
            ])
            if not country:
                return
            else:
                return {'country_id': country[0].id}

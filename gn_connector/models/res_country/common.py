# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


from odoo import fields, models

from odoo.addons.component.core import Component


class OdooResCountry(models.Model):
    _name = 'odoo.res.country'
    _inherit = 'odoo.binding'
    _inherits = {'res.country': 'odoo_id'}

    odoo_id = fields.Many2one(
        comodel_name='res.country',
        required=True,
        ondelete='cascade',
        string='Country',
        oldname='openerp_id',
    )


class ResCountry(models.Model):
    _inherit = 'res.country'

    odoo_bind_ids = fields.One2many(
        comodel_name='odoo.res.country',
        inverse_name='odoo_id',
        readonly=True,
        string='Distant Odoo Bindings',
    )

class ResCountryAdapter(Component):
    _name = 'odoo.res.country.adapter'
    _inherit = 'odoo.adapter'
    _apply_on = 'odoo.res.country'
    _odoo_model = 'res.country'

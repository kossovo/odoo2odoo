# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, fields
from odoo.addons.component.core import Component


class OdooResLang(models.Model):
    _name = 'odoo.res.lang'
    _inherit = 'odoo.binding'
    _inherits = {'res.lang': 'odoo_id'}

    odoo_id = fields.Many2one(
        comodel_name='res.lang',
        required=True,
        ondelete='cascade',
        string='Language',
        oldname='openerp_id',
    )
    active = fields.Boolean(
        string='Active in Distant Odoo',
        default=False,
    )


class ResLang(models.Model):
    _inherit = 'res.lang'

    odoo_bind_ids = fields.One2many(
        comodel_name='odoo.res.lang',
        inverse_name='odoo_id',
        readonly=True,
        string='Odoo Bindings',
    )


class ResLangAdapter(Component):
    _name = 'odoo.res.lang.adapter'
    _inherit = 'odoo.adapter'
    _apply_on = 'odoo.res.lang'
    _odoo_model = 'res.lang'

from odoo.addons.component.core import Component


class OdooModelBinder(Component):
    """ Bind records and give odoo/odoo ids correspondance"""
    _name = 'odoo.binder'
    _inherit = ['base.binder', 'base.odoo.connector']
    _apply_on = [
    ]

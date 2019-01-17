from odoo.addons.component.core import Component


class ProductCategoryDeleter(Component):
    """ Product category for Odoo"""
    _name = 'odoo.product.category.exporter.deleter'
    _inherit = 'odoo.exporter.deleter'
    _apply_on = ['odoo.product.category']
from odoo.addons.component.core import Component


class OdooModelBinder(Component):
    """ Bind records and give odoo/odoo ids correspondance"""
    _inherit = 'odoo.binder'
    _apply_on = [
        'odoo.product.uom.categ',           # Product UoM Categories
        'odoo.product.uom',                 # Product UoM
        'odoo.product.attribute',           # Product Attributes
        'odoo.product.attribute.value',     # Product Attribute Values
        'odoo.res.partner',                 # Partners
        'odoo.product.brand',               # Product brands
        'odoo.product.template',            # Product Templates
        'odoo.product.product',             # Product Product
        'odoo.product.category',            # Product Category
        'odoo.product.attribute.line',      # Product Attribute Lines
        'odoo.breast.pump',                 # Breast pumps
        'odoo.simple.delivery',             # Simple Deliveries
        'odoo.simple.delivery.line',        # Simple Delivery Lines
        'odoo.base_multi_image.image',      # Images
        'odoo.res.lang',                    # Lang
        'odoo.res.country',                 # Country
    ]

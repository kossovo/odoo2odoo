from odoo.addons.component.core import AbstractComponent


class BaseOdooConnectorComponent(AbstractComponent):
    """
    Base Odoo Connector Component

    All components of this connector should inherit from it.
    """
    _name = 'base.odoo.connector'
    _inherit = 'base.connector'
    _collection = 'odoo.backend'

from odoo.addons.component.core import Component


class ProductUoMCategoryImporter(Component):
    """ Import the distant Odoo Product UoM Categories.

    For every product UoM category in the list, a delayed job is created.
    """
    _name = 'odoo.product.uom.categ.batch.importer'
    _inherit = 'odoo.auto.matching.importer'
    _apply_on = ['odoo.product.uom.categ']

    _local_field = 'name'
    _distant_field = 'name'
    _copy_fields = [
    ]

    def _compare_function(self, distant_val, local_val, distant_dict, local_dict):
        if len(local_val) >= 2 and len(distant_val) >= 2 and \
                local_val[0:2].lower() == distant_val[0:2].lower():
            return True
        return False

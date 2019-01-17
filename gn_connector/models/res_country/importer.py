# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.addons.component.core import Component

class CountryImporter(Component):
    _name = 'odoo.res.country.importer'
    _inherit= 'odoo.auto.matching.importer'
    _apply_on = 'odoo.res.country'

    _local_field = 'code'
    _distant_field = 'code'

    def _compare_function(self, distant_val, local_val, distant_dict, local_dict):
        if (
            local_val and
            distant_val and
            len(local_val) >= 2 and
            len(distant_val) >= 2 and
                local_val[0:2].lower() == distant_val[0:2].lower()
        ):
            return True
        return False

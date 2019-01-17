# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo.addons.component.core import Component

from odoo import _, exceptions

_logger = logging.getLogger(__name__)


class AutoMatchingImporter(Component):
    _name = 'odoo.auto.matching.importer'
    _inherit = 'odoo.importer'
    _usage = 'auto.matching.importer'

    _local_field = None
    _distant_field = None
    _copy_fields = []

    def _compare_function(ps_val, local_val, distant_dict, local_dict):
        raise NotImplementedError

    def run(self):
        _logger.debug(
            "[%s] Starting synchro between two Odoo instances"
            % self.model._name
        )
        nr_distant_already_mapped = 0
        nr_distant_mapped = 0
        nr_distant_not_mapped = 0
        local_model_name = list(self.model._inherits.keys())[0]
        local_rec_name = self.env[local_model_name]._rec_name
        model = self.env[local_model_name].with_context(active_test=False)
        local_ids = model.search([])
        local_list_dict = local_ids.read()
        adapter = self.component(usage='backend.adapter')
        # Get the IDS from PS
        distant_ids = adapter.search()
        if not distant_ids:
            raise exceptions.Warning(
                _('Failed to query %s via PS webservice')
                % adapter.odoo_model
            )

        binder = self.binder_for()
        # Loop on all PS IDs
        for distant_id in distant_ids:
            # Check if the PS ID is already mapped to an OE ID
            record = binder.to_internal(distant_id)
            if record:
                # Do nothing for the PS IDs that are already mapped
                _logger.debug(
                    "[%s] Distant Odoo ID %s is already mapped to Local Odoo ID %s"
                    % (self.model._name, distant_id, record.id)
                )
                nr_distant_already_mapped += 1
            else:
                # Distant Odoo IDs not mapped => I try to match between the Distant Odoo ID and
                # the Local Odoo ID. First, I read field in Distant Odoo
                distant_dict = adapter.read(distant_id)
                if isinstance(distant_dict, list):
                    distant_dict = distant_dict[0]
                mapping_found = False
                # Loop on OE IDs
                for local_dict in local_list_dict:
                    # Search for a match
                    local_val = local_dict[self._local_field]
                    distant_val = distant_dict[self._distant_field]
                    if self._compare_function(
                            distant_val, local_val, distant_dict, local_dict):
                        # it matches, so I write the external ID
                        data = {
                            'odoo_id': local_dict['id'],
                            'backend_id': self.backend_record.id,
                        }
                        for local_field, distant_field in self._copy_fields:
                            data[local_field] = local_dict[distant_field]
                        record = self.model.create(data)
                        binder.bind(distant_id, record)
                        _logger.debug(
                            "[%s] Mapping Distant Odoo '%s' (%s) "
                            "to Local Odoo '%s' (%s) " %
                            (self.model._name,
                             distant_dict['name'],  # not hardcode if needed
                             distant_dict[self._distant_field],
                             local_dict[local_rec_name],
                             local_dict[self._local_field]))
                        nr_distant_mapped += 1
                        mapping_found = True
                        break
                if not mapping_found:
                    # if it doesn't match, I just print a warning
                    _logger.warning(
                        "[%s] Distant Odoo '%s' (%s) was not mapped "
                        "to any Local Odoo entry" %
                        (self.model._name,
                         distant_dict['name'],
                         distant_dict[self._distant_field]))

                    nr_distant_not_mapped += 1

        _logger.info(
            "[%s] Synchro between Local Odoo and Distant Odoo successfull"
            % self.model._name
        )
        _logger.info(
            "[%s] Number of Distant Odoo entries already mapped = %s"
            % (self.model._name, nr_distant_already_mapped)
        )
        _logger.info(
            "[%s] Number of Distant Odoo entries mapped = %s"
            % (self.model._name, nr_distant_mapped)
        )
        _logger.info(
            "[%s] Number of Distant Odoo entries not mapped = %s"
            % (self.model._name, nr_distant_not_mapped)
        )

        return True

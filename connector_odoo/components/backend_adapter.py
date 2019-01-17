import logging

from datetime import datetime

from odoo.addons.component.core import AbstractComponent
from odoo.addons.connector.exception import ConnectorException

_logger = logging.getLogger(__name__)

try:
    import odoorpc
except ImportError:
    _logger.debug("Cannot import 'odoorpc'")


class OdooLocation(object):

    def __init__(self, location, port, username,
                 password, database):
        self.location = location
        self.port = port
        self.username = username
        self.password = password
        self.database = database


class OdooAPI(object):

    def __init__(self, location):
        """
        :param location: Odoo location
        :type location: :class:`OdooLocation`
        """
        self._location = location
        self._api = None

    @property
    def api(self):
        if self._api is None:
            api = odoorpc.ODOO(
                host=self._location.location,
                port=self._location.port,
            )
            self._api = api
        return self._api

    def __enter__(self):
        # we do nothing, api is lazy
        if self._api is not None:
            self._api.login(
                db=self._location.database,
                login=self._location.username,
                password=self._location.password,
            )
        return self

    def __exit__(self, type, value, traceback):
        if self._api is not None:
            self._api.logout()

    def call(self, model, method, arguments):
        """

        :param method:
        :param arguments:
        :return:
        """
        try:
            if isinstance(arguments, list):
                while arguments and arguments[-1] is None:
                    arguments.pop()
            start = datetime.now()
            result = None
            self.api
            with self as api:
                try:
                    rpc_model = api.api.env[model]
                    if not isinstance(arguments, list):
                        arguments = [arguments]
                    self.api.env.context.update({'from_sync': True})
                    if hasattr(rpc_model, method):
                        result = getattr(rpc_model, method)(*arguments)
                    else:
                        result = api.api.execute(model, method, *arguments)
                    _logger.info("api.call('%s', '%s', %s') returned %s in %s seconds",
                                  model, method, arguments, result,
                                  (datetime.now() - start).seconds)
                except:
                    _logger.error("api.call('%s', '%s', %s') returned %s in %s seconds",
                                  model, method, arguments, result,
                                  (datetime.now() - start).seconds)
                    raise
                else:
                    _logger.debug("api.call('%s', '%s', '%s') returned %s in %s seconds",
                                  model, method, arguments, result,
                                  (datetime.now() - start).seconds)
                    return result
        except odoorpc.error.RPCError as err:
            raise ConnectorException(
                'A connector error caused the failure of the job: '
                '%s' % err)


class OdooCRUDAdapter(AbstractComponent):
    """ External Records Adapter for Odoo"""

    _name = 'odoo.crud.adapter'
    _inherit = ['base.backend.adapter', 'base.odoo.connector']
    _usage = 'backend.adapter'

    def search(self, filters=None):
        """
        Search records according to some criterias
        and returns a list of ids"""
        raise NotImplementedError

    def read(self, id, attributes=None):
        """ Returns the information of a record """
        raise NotImplementedError

    def search_read(self, filters=None):
        """ Search records according to some criterias
        and returns their information"""
        raise NotImplementedError

    def create(self, data):
        """ Create a record on the external system"""
        raise NotImplementedError

    def write(self, id, data):
        """ Update records on the external system"""
        raise NotImplementedError

    def delete(self, id):
        """ Delete a record on the external system"""
        raise NotImplementedError

    def _call(self, model, method, arguments):
        try:
            odoo_api = getattr(self.work, 'odoo_api')
        except AttributeError:
            raise AttributeError(
                'You must provide a odoo_api attribute with a '
                'OdooAPI instance to be able to user the '
                'Backend Adapter.'
            )
        return odoo_api.call(model, method, arguments)


class GenericAdapter(AbstractComponent):

    _name = 'odoo.adapter'
    _inherit = 'odoo.crud.adapter'

    _odoo_model = None

    def search(self, filters=[], limit=False, offset=False):
        """ Search records according to some criterias
        and returns a list of ids

        :rtype: list
        """
        arguments = []
        if filters or filters == []:
            arguments.append(filters)
        else:
            arguments.append([])
        if offset:
            arguments.append(offset)
        else:
            arguments.append(0)
        if limit:
            arguments.append(limit)
        else:
            arguments.append(False)

        return self._call(self._odoo_model,
                          'search',
                          arguments)

    def read(self, id, attributes=None):
        """ Returns the information of a record

        :rtype: dict
        """
        arguments = [int(id)]
        if attributes:
            arguments.append(attributes)
        return self._call(self._odoo_model,
                          'read',
                          arguments)

    def create(self, data):
        """ Create a record on the external system"""
        return self._call(
            self._odoo_model,
            'create',
            data
        )

    def write(self, id, data):
        """ Update records on the external system"""
        return self._call(
            self._odoo_model,
            'write',
            [int(id), data]
        )

    def delete(self, id):
        """ Delete a record on the external system"""
        return self._call(
            self._odoo_model,
            'unlink',
            [int(id)],
        )
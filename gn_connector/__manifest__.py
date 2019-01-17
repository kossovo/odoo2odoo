{
    'name': 'GLX Odoo Connector',
    'version': '11.0.1.0.0',
    'category': 'Connector',
    'depends': [
        'connector_odoo',
    ],
    'author': 'Amaris',
    'licence': 'AGPL-3',
    'website': 'http://www.amaris.com',
    'images': [

    ],
    'data': [
        'data/gn_connector_data.xml',
        'views/odoo_backend_view.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
}

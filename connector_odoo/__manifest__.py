{
    'name': 'Odoo Connector',
    'version': '11.0.1.0.0',
    'category': 'Connector',
    'depends': [
        'base_technical_user',
        'connector',
        'connector_base_product',
    ],
    'external_dependencies': {
        'python': ['odoorpc'],
    },
    'author': 'Amaris',
    'licence': 'AGPL-3',
    'website': 'http://www.amaris.com',
    'images': [

    ],
    'data': [
        'views/odoo_backend_view.xml',
        'views/connector_odoo_menu.xml',
        'data/connector_odoo_data.xml',
    ],
    'installable': True,
    'application': False,
}
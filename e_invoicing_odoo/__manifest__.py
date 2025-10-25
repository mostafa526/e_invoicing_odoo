{
    'name': 'E-INVOICING',
    'version': '16.0.1.0.0',
    'summary': 'Send invoice to API when validated',
    'description': """
        This module automatically triggers an API call when an invoice is validated.
        It is standardized and reusable across projects.
    """,
    'author': 'Mostafa',
    'depends': ['account'],
    'data': [
        #'security/ir.model.access.csv',
    ],

    'images': [
        'images/main_screenshot.png',
        
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    "license": "LGPL-3",
}
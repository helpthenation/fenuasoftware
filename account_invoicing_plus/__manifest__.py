# -*- coding: utf-8 -*-
{
    'name': "Invoicing Management +",
    'summary': """
    """,
    'description': """
    """,
    'author': "Fenua Software",
    'website': "https://www.fenuasoftware.com",
    'category': 'Invoicing Management',
    'version': '0.1',
    'depends': ['fsw_base', 'account_invoicing', 'base_import'],
    'data': [
        'data/account_payment_action_server.xml',
        'views/res_config_settings_views.xml',
        'views/account_invoicing_plus_views.xml',
        'views/account_payment_view.xml',
        'views/report_invoice.xml',
        'wizard/account_bank_statement_import_views.xml',
        'security/security.xml',
    ],
}

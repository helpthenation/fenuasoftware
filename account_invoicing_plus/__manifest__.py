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
    'depends': ['fsw_base', 'account', 'base_import'],
    'data': [
        # 'data/account_payment_action_server.xml',
        'views/res_config_settings_views.xml',
        'views/account_invoicing_plus_views.xml',
        'views/account_payment_view.xml',
        # 'views/report_invoice.xml',
        'security/security.xml',
    ],
}

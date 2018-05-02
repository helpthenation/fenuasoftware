# -*- coding: utf-8 -*-
{
    'name': "Polynésie Française - Accounting",

    'summary': """
This is the module to manage the accounting chart for French Polynesia in Odoo.
    """,

    'description': """
This is the module to manage the accounting chart for French Polynesia in Odoo.

This module applies to companies based in French Polynesia.
    """,

    'author': "Fenua Software",
    'website': "http://www.fenuasoftware.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Localization',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['account', 'base_iban', 'base_vat',],

    # always loaded
    'data': [
        #data
        'data/account_chart_template.xml',
        'data/account_account_template.xml',
        'data/account_tax_group.xml',
        'data/res_bank.xml',

        #views
        'views/mail_template_views.xml',
        'views/res_company_views.xml',
    ],
}
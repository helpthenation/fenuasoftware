# -*- coding: utf-8 -*-
{
    'name': "Payroll Sailor in French Polynesia",

    'summary': """
    """,

    'description': """
Gestion de la paie des marins en Polynésie Française - En accord avec le fichier de la Direction des Ressources Maritimes et Minières
    """,

    'author': "Fenua Software",
    'website': "http://www.fenuasoftware.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Human Resources',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['l10n_fr', 'account', 'hr'],

    # always loaded
    'data': [
        #data
        'data/ir_sequence.xml',
        
        #security
        'security/ir.model.access.csv',

        #views
        'views/account_invoice_view.xml',
        'views/fishing_campaign.xml',
        'views/hr_payroll_views.xml',
        'views/hr_views.xml',
        'views/res_partner_views.xml',
        'views/templates.xml',
    ],
}
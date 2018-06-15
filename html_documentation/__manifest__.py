# -*- coding: utf-8 -*-
{
    'name': "Documentations",
    'summary': """
    Formulaire HTML de saisie de document.
    """,
    'description': """
    Formulaire HTML de saisie de document.
    """,
    'author': "Fenua Softw@re",
    'website': "https://www.fenuasoftware.com",
    'category': 'Tools',
    'version': '0.1',
    'depends': ['base', 'mass_mailing'],
    'data': [
        'security/ir.model.access.csv',
        'views/documentation_views.xml',
        'views/documentation_templates.xml',
        'views/reports.xml',
    ],
}

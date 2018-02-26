# -*- coding: utf-8 -*-
{
    'name': "Suivis Médical",
    'summary': """
    Ordonnance médicale, liste des interventions
    """,
    'description': """
    """,
    'author': "Fenua Softw@re",
    'website': "https://www.fenuasoftware.com",
    'category': 'Industries & Healthcare',
    'version': '0.1',
    'depends': ['base','product'],
    'data': [
        'security/ir.model.access.csv',
        'views/prescription_views.xml',
        'views/medical_intervention_views.xml',
        'views/res_partner_views.xml',
        'views/reports.xml',
    ],
}

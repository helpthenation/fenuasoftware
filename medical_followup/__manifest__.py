# -*- coding: utf-8 -*-
{
    'name': "Suivis Médical",
    'summary': """
    Ordonnance médicale, consultation médicales
    """,
    'description': """
    """,
    'author': "Fenua Softw@re",
    'website': "https://www.fenuasoftware.com",
    'category': 'Industries & Healthcare',
    'version': '0.1',
    'depends': ['product', 'sale', 'website_quote'],
    'data': [
        'security/ir.model.access.csv',
        'views/medical_followup_view.xml',
        'views/medical_information_document.xml',
        'views/medical_consultation_views.xml',
        'views/medical_consultation_template.xml',
        'views/prescription_views.xml',
        'views/prescription_template.xml',
        'views/res_partner_views.xml',
        'views/reports.xml',
    ],
    'application': True,
}

# -*- coding: utf-8 -*-
{
    'name': "Fleet MRP Repair Link",
    'summary': """
    Link between Fleet and MRP Repair
    """,
    'description': """
    Ajoute le véhicule dans la fiche atelier et sur la facture.
    """,
    'author': "Fenua Softw@re",
    'website': "http://www.fenuasoftware.com",
    'category': 'Link',
    'version': '0.1',
    'depends': ['fleet_plus', 'repair_plus'],
    'data': [
        'views/repair_order_views.xml',
        'views/account_invoice_views.xml',
    ],
}

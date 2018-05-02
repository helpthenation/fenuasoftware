# -*- coding: utf-8 -*-
{
    'name': "Compta Facile (TPE)",
    'summary': """
        Gestion comptable simplifié pour les Très Petite Entreprise (TPE) Entreprise Individuelle.
    """,
    'description': """
        Gestion comptable simplifié pour les Très Petite Entreprise (TPE) Entreprise Individuelle.
    """,
    'author': "Fenua Softw@re",
    'contributors': ['Heifara MATAPO'],
    'website': "https://www.fenuasoftware.com",
    'category': 'Accounting',
    'version': '0.1',
    'depends': ['l10n_pf', 'account_move_template'],
    'data': [
        # data
        'data/account_move_template.xml',

        # views
        'views/views.xml',
        'views/purchase_account_move_views.xml',
        'views/sale_account_move_views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'price': 500,
    'currency': 'EUR',
    'application': True,
}
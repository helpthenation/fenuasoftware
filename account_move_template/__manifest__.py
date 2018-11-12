# -*- coding: utf-8 -*-
{
    'name': "Journal Item Template",
    'summary': """
    Ajoute la fonctionnalité de modèle de pièce comptable.
    """,
    'description': """
    Dans une pièce comptable, lorsqu'on choisit un modèle, la pièce comptable se remplis avec les données du modèle. De plus l'utilisateur peut saisir un montant et la pièce comptable se recalcule automatiquement.
    """,
    'author': "Fenua Softw@re",
    'website': "https://www.fenuasoftware.com",
    'category': 'Accounting',
    'version': '0.1',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_move_template_views.xml',
        'views/account_move_view.xml',
        'views/res_partner_views.xml',
    ],
}

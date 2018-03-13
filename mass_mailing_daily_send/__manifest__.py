# -*- coding: utf-8 -*-
{
    'name': "Mass Mailing Daily send",
    'summary': """
    Envois un mail tous les jours.
    """,
    'description': """
        Créer plusieurs Publipostage. Placer à l'état Daily via le bouton Daily Queued. Le cron 'Process Mass Mailing Daily' s'exécute à 8h tous les matin et envoi un publipostage Daily au hasard.
    """,
    'author': "Fenua Softw@re",
    'website': "https://www.fenuasoftware.com",
    'category': 'Marketing',
    'version': '0.1',
    'depends': ['fsw_base', 'mass_mailing'],
    'data': [
        'data/cron.xml',
        'views/mass_mailing_views.xml',
    ],
}

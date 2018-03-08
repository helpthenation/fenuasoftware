# -*- coding: utf-8 -*-
{
    'name': "Fleet Contacts",
    'summary': """
    Link between Fleet and Contacts
    """,
    'description': """
    Dans la fiche contact, ajoute un lien vers les véhicules du contact.
    """,
    'author': "FenuaSoftw@re",
    'website': "http://www.fenuasoftware.com",
    'category': 'Link',
    'version': '0.1',
    'depends': ['fleet_plus', 'contacts'],
    'data': [
        'views/res_partner_views.xml',
    ],
}

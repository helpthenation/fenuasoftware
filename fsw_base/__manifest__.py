# -*- coding: utf-8 -*-
{
    'name': "Fenua Softw@re",
    'summary': """
    """,
    'description': """
    """,
    'author': "Fenua Software",
    'website': "https://fenuasoftware.com/",
    'category': 'Technical Settings',
    'version': '0.1',
    'depends': ['base', 'mail', 'calendar', 'board'],
    'data': [
        'views/mail_template_views.xml',
        'views/mail_templates.xml',
        'views/res_config_settings_views.xml',
        'views/webclient_templates.xml',
        'data/functions_after_installation.xml',
    ],
    'qweb': [
        "static/src/xml/*.xml",
    ],
}

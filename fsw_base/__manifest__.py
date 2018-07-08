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
    'version': '0.2',
    'depends': ['base', 'mail', 'calendar', 'board'],
    'data': [
        'data/on_update.xml',
        'security/ir_model_access.xml',
        'views/base_menu.xml',
        'views/mail_template_views.xml',
        'views/mail_templates.xml',
        'views/module_views.xml',
        'views/res_config_settings_views.xml',
        'views/webclient_templates.xml',
    ],
    'qweb': [
        "static/src/xml/*.xml",
    ],
}

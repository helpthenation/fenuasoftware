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
    'auto_install': True,
    'depends': ['web', 'base'],
    'data': [
        'data/on_update.xml',
        'security/ir_model_access.xml',
        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'views/module_views.xml',
        'views/res_company_views.xml',
        'views/res_config_settings_views.xml',
        'views/webclient_templates.xml',
    ],
    'qweb': [
        "static/src/xml/base.xml",
    ],
}

# -*- coding: utf-8 -*-
{
    'name': "theme_backend",

    'summary': """
        Odoo 11.0 community theme based on web_responsive of Openworx
        """,

    'description': """
        Odoo 11.0 community theme based on web_responsive of Openworx
    """,

    'author': "FenuaSoftware",
    'website': "http://www.fenuasoftware.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Themes/Backend',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['web_responsive'],

    # always loaded
    'data': [
        'views/assets.xml',
    ],
}
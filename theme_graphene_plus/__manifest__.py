# -*- coding: utf-8 -*-
{
    'name': "Graphene +",

    'summary': """
    """,

    'description': """
    """,

    'author': "Fenua Software",
    'website': "http://www.fenuasoftware.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Theme/Corporate',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['theme_graphene'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/assets.xml',
        'views/customize_modal.xml',
        'views/options.xml',
    ],
}
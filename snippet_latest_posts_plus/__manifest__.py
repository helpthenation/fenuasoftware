# -*- coding: utf-8 -*-
{
    'name': "Latest Posts Snippet +",

    'summary': """
    """,

    'description': """
    """,

    'author': "Fenua Software",
    'website': "http://www.fenuasoftware.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Website',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['snippet_latest_posts'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/options.xml',
        'views/s_latest_posts_caroussel.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    
    'auto_install': True,
}
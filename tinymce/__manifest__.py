# -*- coding: utf-8 -*-
{
    'name': "Integration Tiny MCE",

    'summary': """
    """,

    'description': """
    """,

    'author': "FenuaSoftware",
    'website': "https://fenuasoftware.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Tool',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['web'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/assets.xml',
        'views/views.xml',
    ],

    # template
    'qweb': [
        'static/src/xml/*.xml'
    ],
}
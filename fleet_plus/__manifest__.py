# -*- coding: utf-8 -*-
{
    'name': "Fleet Management +",

    'summary': """
In addition of Odoo Fleet Management module, this handle ship and others.
    """,

    'description': """
    """,

    'author': "Fenua Software",
    'website': "http://www.fenuasoftware.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Employees',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['fleet'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',

        'views/fleet_view.xml',
    ],
}
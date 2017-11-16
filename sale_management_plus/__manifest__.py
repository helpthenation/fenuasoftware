# -*- coding: utf-8 -*-
{
    'name': "Sales Management +",

    'summary': """
    """,

    'description': """
    """,

    'author': "Fenua Softw@re",
    'website': "https://www.fenuasoftware.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale_management'],

    # always loaded
    'data': [
        'views/mail_template_views.xml',
    ],
    'auto_install': True,
}

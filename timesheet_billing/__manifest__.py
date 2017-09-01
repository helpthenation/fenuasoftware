# -*- coding: utf-8 -*-
{
    'name': "Timesheet Billing",

    'summary': """
    """,

    'description': """
    """,

    'author': "Fenua Software",
    'website': "http://www.fenuasoftware.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Invoicing & Payments',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr_timesheet', 'timesheet_grid','account','sale_contract'],

    # always loaded
    'data': [
        'views/account_invoice_views.xml',
        'views/project_task_views.xml',
        'views/timesheet_grid_views.xml',
    ],
}
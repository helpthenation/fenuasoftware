# -*- coding: utf-8 -*-
{
    'name': "Timesheet on Helpdesk",

    'summary': """
    Timesheet on Tickets
    """,

    'description': """
    Timesheet on Tickets
    """,

    'author': "Fenua Software",
    'website': "http://www.fenuasoftware.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Helpdesk',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['helpdesk','hr_timesheet'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/helpdesk_ticket_views.xml',
    ],
}
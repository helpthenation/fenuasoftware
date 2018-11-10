# -*- coding: utf-8 -*-
{
    'name': "Repairs Management +",
    'summary': """
    """,

    'description': """
    """,

    'author': "Fenua Softw@re",
    'website': "https://www.fenuasoftware.com",
    'category': 'Manufacturing',
    'version': '0.1',
    'depends': ['mrp_repair', 'purchase'],
    'data': [
        'security/ir.model.access.csv',
        'views/mrp_repair_views.xml',
        'views/purchase_order_views.xml',
    ],
}
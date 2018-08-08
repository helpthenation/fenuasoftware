# -*- coding: utf-8 -*-
{
    'name': "Membership Management +",
    'summary': """
    """,
    'description': """
    """,
    'author': "Fenua Software",
    'website': "https://www.fenuasoftware.com",
    'category': 'Sales',
    'version': '0.1',
    'depends': ['membership'],
    'data': [
        'reports/membership_card_template.xml',
        'reports/membership_card_report.xml',
        'views/membership_barcode_templates.xml',
        'views/membership_barcode_views.xml',
        'views/membership_invoice_views.xml',
        'views/membership_views.xml',
        'views/res_config_settings_views.xml',
        'views/templates.xml',
    ],
    'qweb': [
        "static/src/xml/membership_inscription_barcode.xml",
    ],

}

# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Mass Mailing Themes +',
    'summary': 'Design gorgeous mails',
    'description': """
Design gorgeous mails
    """,
    'version': '1.0',
    'sequence': 110,
    'website': 'https://fenuasoftware.com',
    'category': 'Marketing',
    'depends': [
        'mass_mailing',
    ],
    'data': [
        'views/assets.xml',
        'views/email_designer_snippets.xml',
        'views/sample_theme_template.xml',
    ],
    'qweb': [],
}

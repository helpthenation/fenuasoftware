# -*- coding: utf-8 -*-
{
    'name': "Polynésie Française - Payroll",

    'summary': """
Payroll in French Polynesia. CPS, CST, etc.
    """,

    'description': """
Payroll in French Polynesia. CPS, CST, etc.
    """,

    'author': "Fenua Software",
    'website': "http://www.fenuasoftware.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Localization',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['l10n_pf', 'hr_payroll', 'hr_payroll_account'],

    # always loaded
    'data': [
        #data
        'data/hr_salary.xml',
        'data/hr_salary_rule_allocations.xml',
        'data/hr_salary_rule_cotisations.xml',
        'data/hr_salary_rule_patronales.xml',
        'data/hr_salary_structure.xml',

        #reports
        'reports/declaration_prealable_a_l_embauche.xml',
        
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'qweb' : [
        'static/src/xml/*.xml',
    ],
}
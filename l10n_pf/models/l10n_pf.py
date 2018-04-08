# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    tahiti_num = fields.Char(related='partner_id.tahiti_num', string='N°Tahiti', size=14)
    rcs_num = fields.Char(related='partner_id.rcs_num', string='N°RC', size=14)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    tahiti_num = fields.Char(string='N°Tahiti', size=14)
    rcs_num = fields.Char(string='N°RC', size=14)

class ChartTemplate(models.Model):
    _inherit = 'account.chart.template'

    def _prepare_all_journals(self, acc_template_ref, company, journals_dict=None):
        journals = super(ChartTemplate, self)._prepare_all_journals(acc_template_ref, company, journals_dict)
        if company.country_id == self.env.ref('base.pf'):
            #For France, sale/purchase journals must have a dedicated sequence for refunds
            for journal in journals:
                if journal['type'] in ['sale', 'purchase']:
                    journal['refund_sequence'] = True
        return journals

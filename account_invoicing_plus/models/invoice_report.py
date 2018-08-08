# -*- coding: utf-8 -*-


from odoo import fields, models


class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'

    raw_margin = fields.Float(string='Marge brute')

    def _select(self):
        return super(AccountInvoiceReport, self)._select() + ", sub.raw_margin as raw_margin"

    def _sub_select(self):
        return super(AccountInvoiceReport, self)._sub_select() + ", ail.raw_margin as raw_margin"

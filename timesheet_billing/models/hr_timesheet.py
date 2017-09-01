# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'
    
    billed = fields.Boolean()
    billed_amount = fields.Float()
    invoice = fields.Many2one(comodel_name='account.invoice', string='Facture')
    
    # @override AccountAnalyticLine.create(self, vals)
    # @see hr_timesheet.hr_timesheet: AccountAnalyticLine
    @api.model
    def create(self, vals):
        if vals.get('account_id'):
            selected_account_id = vals['account_id']
            result = super(AccountAnalyticLine, self).create(vals)
            result.write({'account_id': selected_account_id})        
            return result
        else:
            return super(AccountAnalyticLine, self).create(vals)

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    timesheets = fields.One2many(comodel_name='account.analytic.line', inverse_name='invoice', string='Feuilles de temps facturées')
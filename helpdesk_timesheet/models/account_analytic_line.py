'''
Created on 1 mai 2017

@author: Heifara MATAPO
'''

from odoo import fields, models

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'
    
    helpdesk_ticket = fields.Many2one('helpdesk_ticket', 'Ticket')



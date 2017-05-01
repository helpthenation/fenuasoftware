'''
Created on 1 mai 2017

@author: Heifara MATAPO
'''

from odoo import fields, models

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    description = fields.Html()
    timesheets = fields.One2many(comodel_name='account.analytic.line', inverse_name='helpdesk_ticket', string='Activities')

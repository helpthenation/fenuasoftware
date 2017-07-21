# -*- coding: utf-8 -*-

from odoo import models, fields, api

class FishingCampaign(models.Model):
    _name = 'fishing.campaign'
    _description = 'Fishing campaign'

    name = fields.Char(string='Name', required=True)
    shipname = fields.Char(string='Ship Name', required=True)
    shipowner = fields.Many2one('res.partner', 'Shipowner')
    tahiti_num = fields.Char(string="N°Tahiti") #Voir res_company.py dans fsw_base
    date = fields.Date(string="Fishing campaign date")
    sea_duration = fields.Integer(string='Sea duration (days)')
    departure_preparation_duration = fields.Integer(string='Departure preparation (days)')
    works_on_boat_returned_duration = fields.Integer(string='Works return boat (days)')
    total_duration = fields.Integer(string='Total sea (days)')
    invoice_line_ids = fields.One2many(comodel_name='account.invoice.line', inverse_name='fishing_campaign', string='Invoice Lines', readonly=True, )
    total_revenue_amount = fields.Float(string='Total revenue')
    total_expense_amount = fields.Float(string='Total expense')
    total_net_amount = fields.Float(string='Total to share')
    crew_percentage = fields.Float(string='Crew percentage')
    crew_amount = fields.Float(string='Crew amount', readonly=True)
    shipowner_percentage = fields.Float(string='Shipowner percentage')
    shipowner_amount = fields.Float(string='Shipowner amount', readonly=True)
    sailors = fields.Many2many(comodel_name='hr.employee', string='Crew')

    @api.multi
    def calcul(self):
    	print "calcul"

class ResPartner(models.Model):
    _inherit = 'res.partner'

    fishing_campaigns = fields.One2many(comodel_name='fishing.campaign', inverse_name='shipowner', string='Fishing Campaign')

class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    fishing_campaign = fields.Many2one('fishing.campaign', 'Fishing Campaign', ondelete='set null', index=True, readonly=True)

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    fishing_campaigns = fields.Many2many(comodel_name='fishing.campaign')
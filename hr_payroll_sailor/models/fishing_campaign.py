# -*- coding: utf-8 -*-

from odoo import models, fields, api

class FishingCampaign(models.Model):
    _name = 'fishing.campaign'
    _description = 'Fishing campaign'

    name = fields.Char(string='Name', required=True)
    shipname = fields.Char(string='Ship Name')
    shipowner = fields.Many2one('res.partner', 'Shipowner')
    tahiti_num = fields.Char(related='shipowner.name') #Voir res_company.py dans fsw_base
    date = fields.Date(string="Fishing campaign date")
    sea_duration = fields.Integer(string='Sea duration (days)')
    departure_preparation_duration = fields.Integer(string='Departure preparation (days)')
    works_on_boat_returned_duration = fields.Integer(string='Works return boat (days)')
    total_duration = fields.Integer(string='Total sea (days)', compute='_compute_total_duration')
    customer_invoice_line_ids = fields.One2many(comodel_name='account.invoice.line', inverse_name='fishing_campaign', string='Customer Invoice Lines', domain=[('invoice_id.state', '=', 'open'), ('invoice_id.type', '=', 'out_invoice')], readonly=True, )
    supplier_invoice_line_ids = fields.One2many(comodel_name='account.invoice.line', inverse_name='fishing_campaign', string='Supplier Invoice Lines', domain=[('invoice_id.state', '=', 'open'), ('invoice_id.type', '=', 'in_invoice')], readonly=True, )
    total_revenue_amount = fields.Float(string='Total revenue', readonly=True, compute='_compute_total_revenue_amount')
    total_expense_amount = fields.Float(string='Total expense', readonly=True, compute='_compute_total_expense_amount')
    total_net_amount = fields.Float(string='Total to share', readonly=True, compute='_compute_total_net_amount')
    crew_percentage = fields.Float(string='Crew percentage')
    crew_amount = fields.Float(string='Crew amount', readonly=True, compute='_compute_crew_amount')
    shipowner_percentage = fields.Float(string='Shipowner percentage')
    shipowner_amount = fields.Float(string='Shipowner amount', readonly=True, compute='_compute_shipowner_amount')
    sailors = fields.Many2many(comodel_name='hr.employee', string='Crew')

    @api.multi
    def calcul(self):
    	self._compute_total_revenue_amount()
        self._compute_total_expense_amount()
        self._compute_total_net_amount()

    @api.onchange('sea_duration', 'departure_preparation_duration','works_on_boat_returned_duration')
    def _compute_total_duration(self):
        self.total_duration = self.sea_duration + self.departure_preparation_duration + self.works_on_boat_returned_duration

    @api.model
    def _customer_invoice_line_ids(self):
        for invoice_line_id in self.invoice_line_ids:
            print invoice_line_id
            if invoice_line_id.type == 'out_invoice' or invoice_line_id.type == 'out_refund':
                print invoice_line_id.display_name

    def _compute_total_revenue_amount(self):
        self.total_revenue_amount = 0
        for invoice_line in self.customer_invoice_line_ids:
            self.total_revenue_amount += invoice_line.price_subtotal

    def _compute_total_expense_amount(self):
        self.total_expense_amount = 0
        for invoice_line in self.supplier_invoice_line_ids:
            self.total_expense_amount += invoice_line.price_subtotal

    def _compute_total_net_amount(self):
        self.total_net_amount = self.total_revenue_amount - self.total_expense_amount

    def _compute_crew_amount(self):
        self.crew_amount = (self.total_net_amount * self.crew_percentage) / 100

    def _compute_shipowner_amount(self):
        self.shipowner_amount = (self.total_net_amount * self.shipowner_percentage) / 100

class ResPartner(models.Model):
    _inherit = 'res.partner'

    fishing_campaigns = fields.One2many(comodel_name='fishing.campaign', inverse_name='shipowner', string='Fishing Campaign')

class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    fishing_campaign = fields.Many2one('fishing.campaign', 'Fishing Campaign', ondelete='set null', index=True)

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    fishing_campaigns = fields.Many2many(comodel_name='fishing.campaign')
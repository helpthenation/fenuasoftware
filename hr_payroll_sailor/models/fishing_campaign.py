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
    fishing_campaign_share_distributions = fields.One2many(comodel_name='fishing.campaign.share.distribution',inverse_name='fishing_campaign')
    total_share_weight = fields.Float(string='Calcul de la part', compute='_compute_total_share_weight')

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

    def _compute_total_share_weight(self):
        for fishing_campaign_share_distribution in self.fishing_campaign_share_distributions:
            self.total_share_weight += fishing_campaign_share_distribution.share_weight

        if self.total_share_weight > 0:
            self.total_share_weight = self.crew_amount / self.total_share_weight

class FishingCampaignShareDistribution(models.Model):
    _name = 'fishing.campaign.share.distribution'
    _description ='Fishing Campaign Share Distribution'

    sailor = fields.Many2one(comodel_name='hr.employee', string='Sailor/Employee')
    job = fields.Char(string='Job Title')
    fishing_campaign = fields.Many2one(comodel_name='fishing.campaign', string='Fishing Campaign')
    share_weight = fields.Float(string='Share Distribution')
    wage = fields.Float(string='Wage',readonly=True, compute='_compute_wage')
    deposit = fields.Float(string='Deposit')
    residual = fields.Float(string='Amount Due', readonly=True, compute="_compute_residual")

    @api.one
    def _compute_wage(self):
        self.wage = self.fishing_campaign.total_share_weight * self.share_weight;

    @api.onchange('wage', 'deposit')
    def _compute_residual(self):
        for item in self:
            item.residual = item.wage - item.deposit


class ResPartner(models.Model):
    _inherit = 'res.partner'

    fishing_campaigns = fields.One2many(comodel_name='fishing.campaign', inverse_name='shipowner', string='Fishing Campaign')

class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    fishing_campaign = fields.Many2one('fishing.campaign', 'Fishing Campaign', ondelete='set null', index=True)

class HrEmployee(models.Model): 
    _inherit = 'hr.employee'

    fishing_campaign_share_distributions = fields.One2many(comodel_name='fishing.campaign.share.distribution',inverse_name='sailor')

# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import Warning

class FishingCampaign(models.Model):
    _name = 'fishing.campaign'
    _description = 'Fishing campaign'

    name = fields.Char(string='Name', required=True, readonly=True, states={'draft': [('readonly', False)]})
    shipname = fields.Char(string='Ship Name', readonly=True, states={'draft': [('readonly', False)]})
    shipowner = fields.Many2one('res.partner', 'Shipowner', readonly=True, states={'draft': [('readonly', False)]})
    tahiti_num = fields.Char(related='shipowner.name', readonly=True) #Voir res_company.py dans fsw_base
    date = fields.Date(string="Fishing campaign date", readonly=True, states={'draft': [('readonly', False)]})
    sea_duration = fields.Integer(string='Sea duration (days)', readonly=True, states={'draft': [('readonly', False)]})
    departure_preparation_duration = fields.Integer(string='Departure preparation (days)', readonly=True, states={'draft': [('readonly', False)]})
    works_on_boat_returned_duration = fields.Integer(string='Works return boat (days)', readonly=True, states={'draft': [('readonly', False)]})
    total_duration = fields.Integer(string='Total sea (days)', compute='_compute_total_duration', readonly=True, states={'draft': [('readonly', False)]})
    customer_invoice_line_ids = fields.One2many(comodel_name='account.invoice.line', inverse_name='fishing_campaign', string='Customer Invoice Lines', domain=[('invoice_id.state', '=', 'open'), ('invoice_id.type', '=', 'out_invoice')], readonly=True, )
    supplier_invoice_line_ids = fields.One2many(comodel_name='account.invoice.line', inverse_name='fishing_campaign', string='Supplier Invoice Lines', domain=[('invoice_id.state', '=', 'open'), ('invoice_id.type', '=', 'in_invoice')], readonly=True, )
    total_revenue_amount = fields.Float(string='Total revenue', readonly=True, compute='_compute_total_revenue_amount')
    total_expense_amount = fields.Float(string='Total expense', readonly=True, compute='_compute_total_expense_amount')
    total_net_amount = fields.Float(string='Total to share', readonly=True, compute='_compute_total_net_amount')
    crew_percentage = fields.Float(string='Crew percentage', readonly=True, states={'draft': [('readonly', False)]})
    crew_amount = fields.Float(string='Crew amount', readonly=True, compute='_compute_crew_amount')
    shipowner_percentage = fields.Float(string='Shipowner percentage', readonly=True, states={'draft': [('readonly', False)]})
    shipowner_amount = fields.Float(string='Shipowner amount', readonly=True, compute='_compute_shipowner_amount')
    fishing_campaign_share_distributions = fields.One2many(comodel_name='fishing.campaign.share.distribution',inverse_name='fishing_campaign', readonly=True, states={'draft': [('readonly', False)]})
    total_share_weight = fields.Float(string='Calcul de la part', readonly=True, compute='_compute_total_share_weight')
    state = fields.Selection([
            ('draft', 'Draft'),
            ('valid', 'Validated'),
            ('cancel', 'Canceled'),
            ],default='draft')

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

    def action_valid(self):
        for item in self.fishing_campaign_share_distributions:
            print item.sailor.display_name
            if item.sailor.contract_id:
                self.env['hr.payslip'].create({
                        'employee_id': item.sailor.id,
                        'contract_id': item.sailor.contract_id.id,
                        'struct_id': item.sailor.contract_id.struct_id.id,
                        'fishing_campaign_wage': item.residual
                        })
            else:
                raise Warning(_('Aucun contrat pour '+ item.sailor.display_name))

        self.state = 'valid'

    def action_cancel(self):
        self.state = 'cancel'

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

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    fishing_campaign_wage = fields.Float(string='Salaire brut')
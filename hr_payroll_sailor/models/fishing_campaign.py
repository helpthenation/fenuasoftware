# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import Warning
from odoo.exceptions import UserError, RedirectWarning, ValidationError

class FishingCampaign(models.Model):
    _name = 'fishing.campaign'
    _description = 'Fishing campaign'

    name = fields.Char(string='Name', readonly=True)
    ship = fields.Many2one(comodel_name='fleet.ship', string='Ship', readonly=True, states={'draft': [('readonly', False)]})
    shipowner = fields.Many2one(related='ship.shipowner', string='Shipowner', readonly=True)
    tahiti_num = fields.Char(related='ship.shipowner.tahiti_num', string='Tahiti Number', readonly=True) #Voir res_company.py dans fsw_base
    date = fields.Date(string="Fishing campaign date", readonly=True, states={'draft': [('readonly', False)]})
    sea_duration = fields.Integer(string='Sea duration (days)', readonly=True, states={'draft': [('readonly', False)]})
    departure_preparation_duration = fields.Integer(string='Departure preparation (days)', readonly=True, states={'draft': [('readonly', False)]})
    works_on_boat_returned_duration = fields.Integer(string='Works return boat (days)', readonly=True, states={'draft': [('readonly', False)]})
    total_duration = fields.Integer(string='Total sea (days)', compute='_compute_total_duration', readonly=True)
    customer_invoice_line_ids = fields.One2many(comodel_name='account.invoice.line', inverse_name='fishing_campaign', string='Customer Invoice Lines', domain=[('invoice_id.state', 'in', ('open', 'paid')), ('invoice_id.type', '=', 'out_invoice')], readonly=True, )
    supplier_invoice_line_ids = fields.One2many(comodel_name='account.invoice.line', inverse_name='fishing_campaign', string='Supplier Invoice Lines', domain=[('invoice_id.state', 'in', ('open', 'paid')), ('invoice_id.type', '=', 'in_invoice')], readonly=True, )
    total_revenue_amount = fields.Float(string='Total revenue', readonly=True, compute='_compute_total_revenue_amount', store=True,)
    total_expense_amount = fields.Float(string='Total expense', readonly=True, compute='_compute_total_expense_amount', store=True,)
    total_net_amount = fields.Float(string='Total to share', readonly=True, compute='_compute_total_net_amount', store=True,)
    crew_percentage = fields.Float(string='Crew percentage', readonly=True, states={'draft': [('readonly', False)]})
    crew_amount = fields.Float(string='Crew amount', readonly=True, compute='_compute_crew_amount', store=True,)
    shipowner_percentage = fields.Float(string='Shipowner percentage', readonly=True, states={'draft': [('readonly', False)]})
    shipowner_amount = fields.Float(string='Shipowner amount', readonly=True, compute='_compute_shipowner_amount', store=True,)
    fishing_campaign_share_distributions = fields.One2many(comodel_name='fishing.campaign.share.distribution',inverse_name='fishing_campaign', readonly=True, states={'draft': [('readonly', False)]})
    total_share_weight = fields.Float(string='Calcul de la part', readonly=True, compute='_compute_total_share_weight')
    state = fields.Selection([
            ('draft', 'Draft'),
            ('valid', 'Validated'),
            ('cancel', 'Canceled'),
            ],default='draft')
    payslip_count = fields.Integer(compute='_compute_payslip_count')

    @api.model
    def create(self, vals):
        print "create"
        res = super(FishingCampaign, self).create(vals)
        res.name = self.env['ir.sequence'].sudo().next_by_code('fishing.campaign') 
        print res.display_name
        return res

    @api.depends('customer_invoice_line_ids', 'supplier_invoice_line_ids', )
    def compute_sheet(self):
        print "compute_sheet"
    	self._compute_total_revenue_amount()
        self._compute_total_expense_amount()
        self._compute_total_net_amount()

        self._compute_crew_amount()
        self._compute_shipowner_amount()

        self._compute_total_share_weight()

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

    def _compute_payslip_count(self):
        self.payslip_count = self.env['hr.payslip'].search_count([['fishing_campaign_share_distribution.name', '=', self.name]])


    def action_valid(self):
        if not self.fishing_campaign_share_distributions:
            raise UserError(_('Please add employees first'))
        if self.total_revenue_amount == 0:
            raise UserError(_('Total revenue can not be 0'))
        if self.total_expense_amount == 0:
            raise UserError(_('Total expense can not be 0'))
        if self.crew_amount == 0:
            raise UserError(_('Crew amount can not be 0'))
        if self.shipowner_amount == 0:
            raise UserError(_('Shipowner amount can not be 0'))
        if self.total_share_weight == 0:
            raise UserError(_('Share amount can not be 0'))

        for item in self.fishing_campaign_share_distributions:
            if item.wage == 0:
                raise UserError(_('Employee ' + str(item.sailor.display_name) + " can not have a wage of 0"))
            if item.sailor.contract_id:
                payslip = self.env['hr.payslip'].create({
                        'employee_id': item.sailor.id,
                        'contract_id': item.sailor.contract_id.id,
                        'struct_id': item.sailor.contract_id.struct_id.id,
                        'fishing_campaign_share_distribution': item.id,
                        })
                payslip.compute_sheet()
            else:
                raise Warning(_('Aucun contrat pour '+ str(item.sailor.display_name)))

        self.state = 'valid'

    def action_cancel(self):
        self.state = 'cancel'

    def action_draft(self):
        self.state = 'draft';

    def action_sequence(self):
        print "action_sequence"
        res = self.env['ir.sequence'].sudo().next_by_code('fishing.campaign') 
        print res

    def action_view_payslip(self):
        action = self.env.ref('hr_payroll.action_view_hr_payslip_form')
        result = action.read()[0]
        result['domain'] = "[('fishing_campaign_share_distribution.name','=', '" + self.name + "')]"
        return result

class FishingCampaignShareDistribution(models.Model):
    _name = 'fishing.campaign.share.distribution'
    _description ='Fishing Campaign Share Distribution'

    name = fields.Char(related='fishing_campaign.name', readonly=True, )
    sailor = fields.Many2one(comodel_name='hr.employee', string='Sailor/Employee', required=True,)
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


class FleetShip(models.Model):
    _inherit = 'fleet.ship'

    fishing_campaigns = fields.One2many(comodel_name='fishing.campaign', inverse_name='ship', string='Fishing Campaign')    

class ResPartner(models.Model):
    _inherit = 'res.partner'

    fishing_campaigns = fields.One2many(comodel_name='fishing.campaign', inverse_name='shipowner', string='Fishing Campaign')
    tahiti_num = fields.Char(string='Tahiti Number')

class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    fishing_campaign = fields.Many2one('fishing.campaign', 'Fishing Campaign', ondelete='set null', index=True)

class HrEmployee(models.Model): 
    _inherit = 'hr.employee'

    fishing_campaign_share_distributions = fields.One2many(comodel_name='fishing.campaign.share.distribution',inverse_name='sailor')

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    fishing_campaign_wage = fields.Float(related='fishing_campaign_share_distribution.residual', string='Salaire brut')
    fishing_campaign_share_distribution = fields.Many2one(comodel_name='fishing.campaign.share.distribution', string='Fishing Campaign Share Distribution', readonly=True, ondelete='set null', index=True)

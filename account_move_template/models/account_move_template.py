# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    quick_account_move_template = fields.Many2one(compute='get_quick_account_move_template')

    @api.model
    def get_quick_account_move_template(self):
        for this in self:
            res = self.env['account.move.template'].search([('partner_id', '=', this.id)])
            if len(res) > 0:
                this.quick_account_move_template = res[0].id

class AccountMoveTemplate(models.Model):
    _name = 'account.move.template'
    _description = "Journal Item Template"

    @api.multi
    def _get_default_journal(self):
        if self.env.context.get('default_journal_type'):
            return self.env['account.journal'].search([('company_id', '=', self.env.user.company_id.id),
                                                       ('type', '=', self.env.context['default_journal_type'])],
                                                      limit=1).id

    @api.model
    def _get_currency(self):
        currency = False
        context = self._context or {}
        if context.get('default_journal_id', False):
            currency = self.env['account.journal'].browse(context['default_journal_id']).currency_id
        return currency

    account_move = fields.One2many('account.move', 'account_move_template', string='Pièces Comptable')

    name = fields.Char(string="Nom")
    journal_id = fields.Many2one('account.journal', string='Journal', required=True, default=_get_default_journal)
    journal_type = fields.Selection(related='journal_id.type', string="Type de journal", readonly=True)
    partner_id = fields.Many2one('res.partner')

    company_id = fields.Many2one('res.company', related='journal_id.company_id', string='Company', store=True,
                                 readonly=True, default=lambda self: self.env.user.company_id)
    currency_id = fields.Many2one('res.currency', string='Currency', default=_get_currency,
                                  help="The optional other currency if it is a multi-currency entry.")
    company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency",
                                          readonly=True, help='Utility field to express amount currency', store=True)

    line_ids = fields.One2many('account.move.line.template', 'account_move_template', string='Journal Items', copy=True)

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        for line in self.line_ids:
            line.update({'partner_id': self.partner_id})

    def generate_line_ids(self, base_amount_0, base_amount_1, base_amount_2, base_amount_3):
        line_ids = []

        total = 0.0 # used for total aomount_type
        for line in self.line_ids:

            price_unit = 0.0
            if line.amount_type == '0':
                price_unit = base_amount_0
            elif line.amount_type =='1':
                price_unit = base_amount_1
            elif line.amount_type =='2':
                price_unit = base_amount_2
            elif line.amount_type =='3':
                price_unit = base_amount_3
            elif line.amount_type =='total':
                price_unit = total
            else:
                raise UserError(_("No Amount Type match"))

            debit_credit_amount = price_unit
            if line.tax_line_id:#Originator Taxe
                tax_infos = line.tax_line_id.compute_all(price_unit,
                                                         currency=self.currency_id,
                                                         quantity=1.0, product=None, partner=None)
                if len(tax_infos['taxes']) > 0:
                    debit_credit_amount = tax_infos['taxes'][0].get('amount')

            if line.tax_ids:#Taxes
                tax_infos = line.tax_ids.compute_all(price_unit,
                                                     currency=self.currency_id,
                                                     quantity=1.0, product=None, partner=None)
                debit_credit_amount = tax_infos['total_excluded']

            if debit_credit_amount != 0:
                total = total + debit_credit_amount;
                line_ids.append((0, 0, ({
                    'partner_id': line.partner_id,
                    'name': line.name,
                    'account_id': line.account_id,
                    'tax_line_id': line.tax_line_id,
                    'tax_ids': line.tax_ids,
                    'debit_credit': line.debit_credit,
                    'debit': debit_credit_amount if line.debit_credit == 'debit' else 0,
                    'credit': debit_credit_amount if line.debit_credit == 'credit' else 0,
                })))
        return line_ids

class AccountMoveLineTemplate(models.Model):
    _name = 'account.move.line.template'
    _description = "Journal Entries Template"

    @api.model
    def _get_currency(self):
        currency = False
        context = self._context or {}
        if context.get('default_journal_id', False):
            currency = self.env['account.journal'].browse(context['default_journal_id']).currency_id
        return currency

    sequence = fields.Integer('Sequence', default=0)
    name = fields.Char(string="Label")
    account_move_template = fields.Many2one('account.move.template', 'Modèle')
    account_id = fields.Many2one('account.account', string='Account', required=True, index=True, ondelete="cascade",
                                 domain=[('deprecated', '=', False)],
                                 default=lambda self: self._context.get('account_id', False))
    partner_id = fields.Many2one('res.partner', string="Partner")

    tax_ids = fields.Many2many('account.tax', string='Taxes')
    tax_line_id = fields.Many2one('account.tax', string='Originator tax')

    amount_type = fields.Selection([('0', 'H.T 0'), ('1', 'H.T 1'), ('2', 'H.T 2'), ('3', 'H.T 3'), ('total', 'Total T.T.C')], default=False)

    debit_credit = fields.Selection([('debit', 'Au débit'), ('credit', 'Au crédit')], default='debit')
    debit = fields.Monetary(default=0.0, currency_field='company_currency_id')
    credit = fields.Monetary(default=0.0, currency_field='company_currency_id')

    currency_id = fields.Many2one('res.currency', string='Currency', default=_get_currency,
                                  help="The optional other currency if it is a multi-currency entry.")
    company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency",
                                          readonly=True, help='Utility field to express amount currency', store=True)
    company_id = fields.Many2one('res.company', related='account_id.company_id', string='Company', store=True,
                                 readonly=True)

    @api.onchange('account_id')
    def onchange_account_id(self):
        self.name = self.account_id.name
        self.partner_id = self.account_move_template.partner_id
        self.tax_ids = self.account_id.tax_ids

# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


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
    type = fields.Selection([('simple', 'Modèle simple'), ('product', 'Généré depuis un produit')], default="simple",
                            required=True)

    company_id = fields.Many2one('res.company', related='journal_id.company_id', string='Company', store=True,
                                 readonly=True, default=lambda self: self.env.user.company_id)
    currency_id = fields.Many2one('res.currency', string='Currency', default=_get_currency,
                                  help="The optional other currency if it is a multi-currency entry.")
    company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency",
                                          readonly=True, help='Utility field to express amount currency', store=True)

    product = fields.Many2one('product.template', string='Product')
    amount_with_taxes = fields.Monetary(default=0.0, string="Montant T.T.C", currency_field='company_currency_id')
    other_amount = fields.Monetary(default=0.0, string="Autres Montant", currency_field='company_currency_id')

    line_ids = fields.One2many('account.move.line.template', 'account_move_template', string='Journal Items', copy=True)

    @api.onchange('journal_id')
    def onchange_journal_id(self):
        line_ids = self.generate_line_ids(self.amount_with_taxes, self.other_amount)
        self.update({'line_ids': line_ids})

    @api.onchange('type')
    def onchange_type(self):
        if self.type == 'simple':
            self.line_ids = False
            self.product = False
            self.amount_with_taxes = False

    @api.onchange('product')
    def onchange_product(self):
        line_ids = []
        if self.product and self.journal_id.type == 'purchase':
            self.amount_with_taxes = self.product.standard_price
            line_ids = self._generate_purchase_line_ids(self.amount_with_taxes, self.other_amount)

        elif self.product and self.journal_id.type == 'sale':
            self.amount_with_taxes = self.product.lst_price
            line_ids = self._generate_sale_line_ids(self.amount_with_taxes, self.other_amount)

        self.update({'line_ids': line_ids})

    @api.onchange('amount_with_taxes', 'other_amount')
    def onchange_amount_with_taxes(self):
        line_ids = self.generate_line_ids(self.amount_with_taxes, self.other_amount)
        self.update({'line_ids': line_ids})

    def generate_line_ids(self, amount_with_taxes, other_amount):
        '''
            Génère les lignes en fonction des données du modèle
        '''
        line_ids = []

        if self.type == 'simple':
            line_ids = self._generate_simple_line_ids(amount_with_taxes, other_amount)

        elif self.type == 'product':
            if self.product and self.journal_id.type == 'purchase':
                line_ids = self._generate_purchase_line_ids(amount_with_taxes)

            elif self.product and self.journal_id.type == 'sale':
                line_ids = self._generate_sale_line_ids(amount_with_taxes)

        return line_ids

    def _generate_simple_line_ids(self, amount_with_taxes, other_amount):
        line_ids = []
        for line in self.line_ids:

            debit_credit_amount = amount_with_taxes
            if line.tax_line_id:#Originator Taxe
                tax_infos = line.tax_line_id.compute_all(amount_with_taxes - other_amount,
                                                         currency=self.currency_id,
                                                         quantity=1.0, product=self.product, partner=None)
                if len(tax_infos['taxes']) > 0:
                    debit_credit_amount = tax_infos['taxes'][0].get('amount')

            if line.tax_ids:#Taxes
                tax_infos = line.tax_ids.compute_all(amount_with_taxes - other_amount,
                                                     currency=self.currency_id,
                                                     quantity=1.0, product=self.product, partner=None)
                debit_credit_amount = tax_infos['total_excluded']

            if line.other_amount:#Autres montant
                debit_credit_amount = other_amount

            line_ids.append((0, 0, ({
                'partner_id': line.partner_id,
                'name': line.name,
                'account_id': line.account_id,
                'tax_line_id': line.tax_line_id,
                'tax_ids': line.tax_ids,
                'other_amount': line.other_amount,
                'debit_credit': line.debit_credit,
                'debit': debit_credit_amount if line.debit_credit == 'debit' else 0,
                'credit': debit_credit_amount if line.debit_credit == 'credit' else 0,
            })))
        return line_ids

    def _generate_purchase_line_ids(self, amount_with_taxes):
        line_ids = []
        tax_infos = self.product.supplier_taxes_id.compute_all(amount_with_taxes, currency=self.currency_id,
                                                               quantity=1.0, product=self.product, partner=None)

        # Ligne de l'article au crédit
        account_id = self.product.property_account_expense_id
        if account_id is False or len(account_id) == 0:
            account_id = self.product.categ_id.property_account_expense_categ_id
        line_ids.append((0, 0, ({
            'account_move_template': self.id,
            'partner_id': self.partner_id,
            'name': self.product.display_name,
            'account_id': account_id.id,
            'debit': 0,
            'credit': tax_infos['total_excluded'],
        })))

        # Ligne de tax au crédit
        if len(tax_infos['taxes']) > 0:
            line_ids.append((0, 0, ({
                'account_move_template': self.id,
                'partner_id': self.partner_id,
                'name': tax_infos['taxes'][0].get('name'),
                'account_id': tax_infos['taxes'][0].get('account_id'),
                'tax_line_id': tax_infos['taxes'][0].get('id'),
                'debit': 0,
                'credit': tax_infos['taxes'][0].get('amount'),
            })))

        # Ligne du vendor au débit
        line_ids.append((0, 0, ({
            'account_move_template': self.id,
            'partner_id': self.partner_id,
            'name': self.journal_id.default_debit_account_id.display_name,
            'account_id': self.journal_id.default_debit_account_id,
            'debit': tax_infos['total_included'],
            'credit': 0,
        })))

        return line_ids

    def _generate_sale_line_ids(self, amount_with_taxes):
        line_ids = []
        tax_infos = self.product.taxes_id.compute_all(amount_with_taxes, currency=self.currency_id, quantity=1.0,
                                                      product=self.product, partner=None)

        # Ligne de l'article au débit
        account_id = self.product.property_account_income_id
        if account_id is False or len(account_id) == 0:
            account_id = self.product.categ_id.property_account_income_categ_id
        line_ids.append((0, 0, ({
            'account_move_template': self.id,
            'partner_id': self.partner_id,
            'name': self.product.display_name,
            'account_id': account_id.id,
            'debit': tax_infos['total_excluded'],
            'credit': 0,
        })))

        # Ligne de tax au débit
        if len(tax_infos['taxes']) > 0:
            line_ids.append((0, 0, ({
                'account_move_template': self.id,
                'partner_id': self.partner_id,
                'name': tax_infos['taxes'][0].get('name'),
                'account_id': tax_infos['taxes'][0].get('account_id'),
                'tax_line_id': tax_infos['taxes'][0].get('id'),
                'debit': tax_infos['taxes'][0].get('amount'),
                'credit': 0,
            })))

        # Ligne du client au crédit
        line_ids.append((0, 0, ({
            'account_move_template': self.id,
            'partner_id': self.partner_id,
            'name': self.journal_id.default_credit_account_id.display_name,
            'account_id': self.journal_id.default_credit_account_id,
            'debit': 0,
            'credit': tax_infos['total_included'],
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

    name = fields.Char(string="Label")
    account_move_template = fields.Many2one('account.move.template', 'Modèle')
    account_id = fields.Many2one('account.account', string='Account', required=True, index=True, ondelete="cascade",
                                 domain=[('deprecated', '=', False)],
                                 default=lambda self: self._context.get('account_id', False))
    partner_id = fields.Many2one('res.partner', string="Partner")

    tax_ids = fields.Many2many('account.tax', string='Taxes')
    tax_line_id = fields.Many2one('account.tax', string='Originator tax')

    other_amount = fields.Boolean(default=False, string="Autres montant")

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
        if self.account_move_template.type == 'simple':
            self.name = self.account_id.name

        self.partner_id = self.account_move_template.partner_id
        self.tax_ids = self.account_id.tax_ids

# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    account_move_template = fields.Many2one('account.move.template', 'Modèle')
    account_move_template_type = fields.Selection(related='account_move_template.type', readonly=True)
    amount_with_taxes = fields.Monetary(default=0.0, currency_field='currency_id')

    @api.onchange('account_move_template')
    def onchange_account_move_template(self):
        self.ref = self.account_move_template.name
        self.journal_id = self.account_move_template.journal_id
        self.amount_with_taxes = self.account_move_template.amount_with_taxes
        self.update({'line_ids': self.account_move_template.generate_line_ids(self.amount_with_taxes)})

    @api.onchange('amount_with_taxes')
    def onchange_amount_with_taxes(self):
        self.update({'line_ids': self.account_move_template.generate_line_ids(self.amount_with_taxes)})

    @api.onchange('amount')
    def onchange_amount(self):
        if self.account_move_template_type == 'simple':
            self.amount_with_taxes = self.amount

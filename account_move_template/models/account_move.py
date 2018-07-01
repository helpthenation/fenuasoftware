# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    account_move_template = fields.Many2one('account.move.template', 'Modèle')
    account_move_template_type = fields.Selection(related='account_move_template.type', readonly=True)
    amount_with_taxes = fields.Monetary(default=0.0, string="T.T.C", currency_field='currency_id')
    other_amount = fields.Monetary(default=0.0, string="Autres Montant", currency_field='currency_id')
    base_tva0_amount = fields.Monetary(default=0.0, string="H.T 0", currency_field='currency_id')
    base_tva1_amount = fields.Monetary(default=0.0, string="H.T 1", currency_field='currency_id')
    base_tva2_amount = fields.Monetary(default=0.0, string="H.T 2", currency_field='currency_id')
    base_tva3_amount = fields.Monetary(default=0.0, string="H.T 3", currency_field='currency_id')

    @api.onchange('account_move_template')
    def onchange_account_move_template(self):
        self.ref = self.account_move_template.name
        self.journal_id = self.account_move_template.journal_id
        self.amount_with_taxes = False
        self.other_amount = False
        self.update({'line_ids': self.account_move_template.generate_line_ids(self.amount_with_taxes, self.other_amount, self.base_tva0_amount, self.base_tva1_amount, self.base_tva2_amount, self.base_tva3_amount)})

    @api.onchange('amount_with_taxes', 'other_amount', 'base_tva0_amount', 'base_tva1_amount', 'base_tva2_amount', 'base_tva3_amount')
    def update_line_ids(self):
        self.update({'line_ids': self.account_move_template.generate_line_ids(self.amount_with_taxes, self.other_amount, self.base_tva0_amount, self.base_tva1_amount, self.base_tva2_amount, self.base_tva3_amount)})

    @api.onchange('amount')
    def onchange_amount(self):
        if self.account_move_template_type == 'simple':
            self.amount_with_taxes = self.amount

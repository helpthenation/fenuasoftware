# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    account_move_template = fields.Many2one('account.move.template', 'Modèle')
    base_tva0_amount = fields.Monetary(default=0.0, string="H.T 0", currency_field='currency_id')
    base_tva1_amount = fields.Monetary(default=0.0, string="H.T 1", currency_field='currency_id')
    base_tva2_amount = fields.Monetary(default=0.0, string="H.T 2", currency_field='currency_id')
    base_tva3_amount = fields.Monetary(default=0.0, string="H.T 3", currency_field='currency_id')

    @api.onchange('account_move_template')
    def onchange_account_move_template(self):
        self.ref = self.account_move_template.name
        self.journal_id = self.account_move_template.journal_id
        self.update({'line_ids': self.account_move_template.generate_line_ids(self.base_tva0_amount, self.base_tva1_amount, self.base_tva2_amount, self.base_tva3_amount)})

    @api.onchange('base_tva0_amount', 'base_tva1_amount', 'base_tva2_amount', 'base_tva3_amount')
    def update_line_ids(self):
        self.update({'line_ids': self.account_move_template.generate_line_ids(self.base_tva0_amount, self.base_tva1_amount, self.base_tva2_amount, self.base_tva3_amount)})

    @api.onchange('amount')
    def onchange_amount(self):
        self.update({'line_ids': self.account_move_template.generate_line_ids(self.base_tva0_amount, self.base_tva1_amount, self.base_tva2_amount, self.base_tva3_amount)})

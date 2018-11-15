# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from .account_payment import account_abstract_payment


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_account_move_template = fields.Boolean("Modèle de Pièce Comptable")
    enable_schedule_payment_when_register_payment = fields.Boolean("Activer l'échéancier client lors de l'enregistrement d'un paiement partiel d'une facture")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            enable_schedule_payment_when_register_payment=self.env['ir.config_parameter'].sudo().get_param('account_invoicing_plus.enable_schedule_payment_when_register_payment'),
        )
        return res

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('account_invoicing_plus.enable_schedule_payment_when_register_payment', self.enable_schedule_payment_when_register_payment)
        view = self.env.ref('account_invoicing_plus.account_invoice_form_inherited')
        view.update({'active': self.enable_schedule_payment_when_register_payment})
        if self.enable_schedule_payment_when_register_payment:
            account_abstract_payment.SELECTION.append(('schedule', 'Scheduled Payment'))
        else:
            for item in account_abstract_payment.SELECTION:
                if 'schedule' in item:
                    account_abstract_payment.SELECTION.remove(item)

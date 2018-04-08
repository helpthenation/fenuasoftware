# -*- coding: utf-8 -*-
import time
import threading

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, Warning


class MembershipCheckWizard(models.TransientModel):
    _name = "membership.check.wizard"

    ref = fields.Char()
    state = fields.Char(readonly=True)
    partner_name = fields.Char(readonly=True)
    error = fields.Boolean(default=False)
    error_message = fields.Char()

    @api.onchange('ref')
    def onchange_ref(self):
        self.ok_action()

    def ok_action(self):
        print("REF: " + str(self.ref))
        if not self.state and self.ref:
            res_partner = self.env['res.partner'].search([('membership_barcode', '=', self.ref)])
            print("res_partner: " + str(res_partner))
            if len(res_partner) == 0:
                self.ref = False
                self.error = True
                self.error_message = 'Mot de passe incorrecte!'
            else:
                self.ref = res_partner.ref
                self.state = res_partner.membership_state
                self.partner_name = res_partner.display_name
        else:
            self.ref = ""
            self.partner_name = ""
            self.state = ""
            self.error = False
            self.error_message = False

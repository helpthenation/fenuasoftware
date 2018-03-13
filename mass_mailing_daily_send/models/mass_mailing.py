# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models, _


class MassMailing(models.Model):
    _inherit = 'mail.mass_mailing'

    state = fields.Selection([('draft', 'Draft'), ('in_queue', 'In Queue'), ('sending', 'Sending'), ('daily', 'Daily'), ('done', 'Sent')],
                             string='Status', required=True, copy=False, default='draft')

    @api.multi
    def put_in_daily(self):
        self.write({'state': 'daily'})

    @api.model
    def _process_mass_mailing_daily(self):
        mass_mailings = self.search([('state', '=', 'daily'), ])
        for mass_mailing in mass_mailings:
            if len(mass_mailing.get_remaining_recipients()) > 0:
                mass_mailing.state = 'daily'
                mass_mailing.send_mail()
            else:
                mass_mailing.state = 'done'
            break  # only execute once a day

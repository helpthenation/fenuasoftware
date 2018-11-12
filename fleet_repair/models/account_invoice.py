# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    vehicle = fields.Many2one('fleet.vehicle', string='Vehicle', readonly=True, states={'draft': [('readonly', False)]})

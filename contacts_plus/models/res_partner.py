# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    birthdate = fields.Date(string="Date de naissance")
    facebook_url = fields.Char(string="Facebook")
    facebook_url_enable = fields.Boolean(compute='_compute_facebook_url_enable', default=False, readonly=False)

    @api.depends('facebook_url_enable')
    @api.one
    def _compute_facebook_url_enable(self):
        self.facebook_url_enable = self.env['ir.config_parameter'].sudo().get_param('contacts_plus.facebook_url_enable')

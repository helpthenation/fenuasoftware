# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import timedelta, datetime, date


class ResPartner(models.Model):
    _inherit = "res.partner"

    birthdate = fields.Date(string="Date de naissance")
    facebook_url = fields.Char(string="Facebook")
    facebook_url_enable = fields.Boolean(compute='_compute_facebook_url_enable', default=False, readonly=False)

    @api.depends('facebook_url_enable')
    @api.one
    def _compute_facebook_url_enable(self):
        self.facebook_url_enable = self.env['ir.config_parameter'].sudo().get_param('contacts_plus.facebook_url_enable')

    @api.model
    def send_happy_birthday(self):
        domain = [('birthdate', '=', date.today())]
        partners = self.env['res.partner'].search(domain)
        for partner in partners:
            template = self.env.ref('contacts_plus.mail_template_happy_birthday')
            self.env['mail.template'].browse(template.id).send_mail(self.id)
            partner.message_post_with_template(template.id)

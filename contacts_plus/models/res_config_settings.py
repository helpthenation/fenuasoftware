# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    facebook_url_enable = fields.Boolean(string='Ajouter le champ Facebook', help='Key is : contacts_plus.facebook_url_enable')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            facebook_url_enable=self.env['ir.config_parameter'].sudo().get_param('contacts_plus.facebook_url_enable'),
        )
        return res

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('contacts_plus.facebook_url_enable', self.facebook_url_enable)

# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    customize_background = fields.Boolean(string='', help='Key is : web_plus.customize_background')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            customize_background=self.env['ir.config_parameter'].sudo().get_param('web_plus.customize_background'),
        )
        return res

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('web_plus.customize_background', self.read_price_from_template)
        view = self.env.ref('web_plus.report_assets_common_inherited')
        view.update({'active': self.customize_background})

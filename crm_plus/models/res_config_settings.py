# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    disable_merge_check = fields.Boolean(string='Désactiver contrôles sur fusion de contacts', help='Key is : crm_plus.disable_merge_check')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            disable_merge_check=self.env['ir.config_parameter'].sudo().get_param('crm_plus.disable_merge_check'),
        )
        return res

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('crm_plus.disable_merge_check', self.disable_merge_check)

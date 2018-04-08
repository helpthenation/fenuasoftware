# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    example = fields.Boolean(text='Un exemple')
    module_sample = fields.Boolean("Installe le module sample")
    module_account_invoicing_plus = fields.Boolean("Installer")
    module_calendar_plus = fields.Boolean("Installer")
    module_l10n_pf = fields.Boolean("Installer")
    module_l10n_pf_hr_payroll = fields.Boolean("Installer")
    module_contacts_plus = fields.Boolean("Installer")
    module_crm_plus = fields.Boolean("Installer")
    module_point_of_sale_plus = fields.Boolean("Installer")
    module_fleet_plus = fields.Boolean("Installer")
    module_sale_management_plus = fields.Boolean("Installer")
    module_membership_plus = fields.Boolean("Installer")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            example=self.env['ir.config_parameter'].sudo().get_param('fsw_base.example'),
        )
        return res

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('fsw_base.example', self.example)

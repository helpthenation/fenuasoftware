# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    example = fields.Boolean(text='Un exemple')
    module_account_invoicing_plus = fields.Boolean("Invoicing+")
    module_calendar_plus = fields.Boolean("Calendar+")
    module_l10n_pf = fields.Boolean("Comptabilité Polynésie Française")
    module_l10n_pf_hr_payroll = fields.Boolean("Paie Polynésie Française")
    module_contacts_plus = fields.Boolean("Contact+")
    module_crm_plus = fields.Boolean("CRM+")
    module_point_of_sale_plus = fields.Boolean("Point de Vente+")
    module_fleet_plus = fields.Boolean("Parc Automobile+")
    module_sale_management_plus = fields.Boolean("Ventes+")
    module_membership_plus = fields.Boolean("Adhérent+")

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

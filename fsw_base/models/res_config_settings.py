# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_account_invoicing_plus = fields.Boolean("Invoicing+")
    module_calendar_plus = fields.Boolean("Calendar+")
    module_contacts_plus = fields.Boolean("Contact+")
    module_crm_plus = fields.Boolean("CRM+")
    module_l10n_pf = fields.Boolean("Comptabilité Polynésie Française")
    module_purchase_plus = fields.Boolean("Achats+")
    module_repair_plus = fields.Boolean("Repair+")
    module_sale_management_plus = fields.Boolean("Ventes+")

    #NOT MIGRATE
    module_l10n_pf_hr_payroll = fields.Boolean("Paie Polynésie Française")
    module_point_of_sale_plus = fields.Boolean("Point de Vente+")
    module_fleet_plus = fields.Boolean("Parc Automobile+")
    module_membership_plus = fields.Boolean("Adhérent+")

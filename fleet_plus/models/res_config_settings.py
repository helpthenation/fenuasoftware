# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_fleet_contacts = fields.Boolean('Liée parc automobile avec les contacts')
    module_fleet_mrp_repair = fields.Boolean('Liée parc automobile avec la réparation')

# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_point_of_sale_fiscal_position_with_fixed_selling_price = fields.Boolean("Point of Sale Fiscal Position With Fixed Selling Price")

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

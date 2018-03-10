# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('template_id')
    def onchange_template_id(self):
        '''
        Disable pricelist to enable reading price from template instead of pricelist
        :return:
        '''
        read_price_from_template = self.env['ir.config_parameter'].sudo().get_param('sale_management_plus.read_price_from_template')
        if read_price_from_template:
            pricelist_id = self.pricelist_id
            self.pricelist_id = False
            super(SaleOrder, self).onchange_template_id()
            self.pricelist_id = pricelist_id
        else:
            super(SaleOrder, self).onchange_template_id()

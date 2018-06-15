# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    read_price_from_template = fields.Boolean(string='Lire le prix de vente dans le modèle de devis', help='Key is : sale_management_plus.read_price_from_template')
    module_sale_order_html_documentation = fields.Boolean("Ajouter des documents aux devis et bon de commandes")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            read_price_from_template=self.env['ir.config_parameter'].sudo().get_param('sale_management_plus.read_price_from_template'),
        )
        return res

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('sale_management_plus.read_price_from_template', self.read_price_from_template)
        view = self.env.ref('sale_management_plus.view_sale_quote_template_form')
        view.update({'active': self.read_price_from_template})

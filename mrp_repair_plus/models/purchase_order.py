# -*- coding: utf-8 -*-


from odoo import api, fields, models, _


class purchase_order(models.Model):
    _inherit = "purchase.order"

    mrp_repair = fields.One2many('mrp.repair', 'purchase_order', string='Order de réparation', copy=False, readonly=True, track_visibility="onchange")

    @api.multi
    def action_mrp_repair(self):
        self.ensure_one()
        return {
            'name': _('Ordre de réparation'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mrp.repair',
            'view_id': self.env.ref('mrp_repair.view_repair_order_form').id,
            'target': 'current',
            'res_id': self.mrp_repair.id,
        }

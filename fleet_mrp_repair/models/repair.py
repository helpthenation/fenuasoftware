# -*- coding: utf-8 -*-


from odoo import api, fields, models, _


class Repair(models.Model):
    _inherit = 'repair.order'

    vehicle = fields.Many2one('fleet.vehicle', string='Vehicle', readonly=True, states={'draft': [('readonly', False)]})

    @api.multi
    def action_invoice_create(self, group=False):
        res = super(Repair, self).action_invoice_create(group)
        if res[self.id]:
            invoice = self.env['account.invoice'].browse([res[self.id]])
            if invoice:
                invoice.write({'vehicle': self.vehicle.id})
        return res

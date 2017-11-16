# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    vehicle_counts = fields.Integer(compute="_compute_vehicle_counts")

    @api.depends('vehicle_counts')
    @api.one
    def _compute_vehicle_counts(self):
        self.vehicle_counts = self.env['fleet.vehicle'].search_count([('driver_id', '=', self.id)]);

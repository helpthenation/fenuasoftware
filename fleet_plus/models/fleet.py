# -*- coding: utf-8 -*-

from odoo import models, fields, api

class FleetShip(models.Model):
	_inherit = 'fleet.vehicle'
	_name = 'fleet.ship'
	_description = 'Information on a ship'

	shipname = fields.Char(string='Ship name', required=True,)
	shipowner = fields.Many2one('res.partner', 'Armateur', help="L'armateur, le propriétaire du bateau", required=True,)

	@api.depends('model_id', 'license_plate', 'shipname')
	def _compute_vehicle_name(self):
		for record in self:
			record.name = record.shipname

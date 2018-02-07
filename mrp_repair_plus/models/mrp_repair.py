# -*- coding: utf-8 -*-


from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime


class Repair(models.Model):
    _inherit = 'mrp.repair'

    repairer = fields.Many2one('res.users', string='Réparateur', index=True)
    intervention_date = fields.Datetime(string="Date d'intervention")
    intervention_duration = fields.Float(string="Durée")

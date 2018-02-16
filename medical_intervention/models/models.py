# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Partner(models.Model):
    _inherit = "res.partner"

    medical_interventions = fields.One2many('medical.intervention', 'patient', string="Interventions médicales")
    medical_intervention_count = fields.Integer(string="Nombre d'intervetion médicale", compute='_compute_medical_intervention_count')

    def _compute_medical_intervention_count(self):
        for partner in self:
            partner.medical_intervention_count = self.env['medical.intervention'].search_count([('patient', '=', partner.id)])


class MedicalIntervention(models.Model):
    _description = 'Intervention Médicale'
    _name = "medical.intervention"

    def _default_date(self):
        return fields.Date.context_today(self)

    date = fields.Date(string="Date d'intervention", default=_default_date)
    patient = fields.Many2one('res.partner', string="Patient")
    description = fields.Char(string="Description")

# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Partner(models.Model):
    _inherit = "res.partner"

    medical_consultation = fields.One2many('medical.consultation', 'patient', string="Consultations médicales")
    medical_consultation_count = fields.Integer(string="Nombre de consultations médicales", compute='_compute_medical_consultation_count')

    def _compute_medical_consultation_count(self):
        for partner in self:
            partner.medical_consultation_count = self.env['medical.consultation'].search_count([('patient', '=', partner.id)])


class MedicalConsultation(models.Model):
    _description = 'Consultation Médicale'
    _name = "medical.consultation"

    def _default_date(self):
        return fields.Date.context_today(self)

    date = fields.Date(string="Date de consultation médicale", default=_default_date)
    patient = fields.Many2one('res.partner', string="Patient")
    description = fields.Text(string="Description")

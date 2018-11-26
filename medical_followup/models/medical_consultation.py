# -*- coding: utf-8 -*-
import time
from datetime import datetime, timedelta
from dateutil import relativedelta

import babel

from odoo import api, fields, models, tools, _


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
    _inherit = ['mail.thread']

    def _default_date(self):
        return fields.Date.context_today(self)

    medical_consultation_template = fields.Many2one('medical.consultation.template', string="Modèle")
    name = fields.Char(readonly=True, compute="_compute_name")
    date = fields.Date(string="Date de consultation médicale", default=_default_date)
    patient = fields.Many2one('res.partner', string="Patient")
    description = fields.Text(string="Description")
    user_id = fields.Many2one('res.users', default=lambda self: self._uid)

    type = fields.Selection([
        ('crop', 'Compte Rendu Opératoire'),
    ], string="Type", default=None,
        help="Détermine si c'est un type particulier.")
    operator = fields.Many2one('res.partner', string="Opérateur")
    anesthetist = fields.Many2one('res.partner', string="Anesthésiste")
    reason = fields.Char(string="Motif d'hospitalisation")

    @api.onchange('medical_consultation_template')
    def onchange_medical_consultation_template(self):
        self.update({
            'type': self.medical_consultation_template.type,
            'operator': self.medical_consultation_template.operator,
            'anesthetist': self.medical_consultation_template.anesthetist,
            'reason': self.medical_consultation_template.reason,
            'description': self.medical_consultation_template.description,
        })

    @api.onchange('type', 'date')
    def _compute_name(self):
        if self.type == 'crop':
            self.name = "COMPTE RENDU OPERATOIRE"
        else:
            locale = self.env.context.get('lang') or 'en_US'
            ttyme = datetime.fromtimestamp(time.mktime(time.strptime(self.date, "%Y-%m-%d")))
            self.name = "Intervention du " + tools.ustr(babel.dates.format_date(date=ttyme, format='dd MMMM y', locale=locale))

    def _get_printed_report_name(self):
        return "INTERVENTIONS_MEDICAL"


class MedicalConsultationTemplate(models.Model):
    _description = 'Modèle de Consultation Médicale'
    _name = "medical.consultation.template"

    name = fields.Char()
    type = fields.Selection([
        ('crop', 'Compte Rendu Opératoire'),
    ], string="Type", default=None,
        help="Détermine si c'est un type particulier.")
    operator = fields.Many2one('res.partner', string="Opérateur")
    anesthetist = fields.Many2one('res.partner', string="Anesthésiste")
    reason = fields.Char(string="Motif d'hospitalisation")
    description = fields.Text(string="Description")

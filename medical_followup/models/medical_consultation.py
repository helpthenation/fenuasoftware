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

    def _default_date(self):
        return fields.Date.context_today(self)

    name = fields.Char(readonly=True, compute="_compute_name")
    date = fields.Date(string="Date de consultation médicale", default=_default_date)
    patient = fields.Many2one('res.partner', string="Patient")
    description = fields.Text(string="Description")
    user_id = fields.Many2one('res.users', compute="_compute_user_id")

    type = fields.Selection([
        ('crop', 'Compte Rendu Opératoire'),
    ], string="Type", default=None,
        help="Détermine si c'est un type particulier.")
    operator = fields.Many2one('res.partner', string="Opérateur")
    anesthetist = fields.Many2one('res.partner', string="Anesthésiste")
    reason = fields.Char(string="Motif d'hospitalisation")

    @api.onchange('type', 'date')
    def _compute_name(self):
        if self.type == 'crop':
            self.name = "COMPTE RENDU OPERATOIRE"
        else:
            locale = self.env.context.get('lang') or 'en_US'
            ttyme = datetime.fromtimestamp(time.mktime(time.strptime(self.date, "%Y-%m-%d")))
            self.name = "Intervention du " + tools.ustr(babel.dates.format_date(date=ttyme, format='dd MMMM y', locale=locale))

    def _compute_user_id(self):
        self.user_id = self.env.user

    def _get_printed_report_name(self):
        return "INTERVENTIONS_MEDICAL"

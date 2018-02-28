# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Partner(models.Model):
    _inherit = "res.partner"

    prescriptions = fields.One2many('prescription', 'patient', string="Interventions médicales")
    prescriptions_count = fields.Integer(string="Nombre d'ordonnance", compute='_compute_prescription_count')

    def _compute_prescription_count(self):
        for partner in self:
            partner.prescriptions_count = self.env['prescription'].search_count([('patient', '=', partner.id)])

    def _get_printed_report_name(self):
        return "INTERVENTIONS_MEDICAL"


class ResUsers(models.Model):
    _inherit = 'res.users'

    prescriptions = fields.One2many('prescription', 'contributor', string="Interventions médicales")


class Prescription(models.Model):
    _description = 'Prescription'
    _name = "prescription"

    def _default_date(self):
        return fields.Date.context_today(self)

    date = fields.Date(string="Date d'intervention", default=_default_date)
    patient = fields.Many2one('res.partner', string="Patient")
    contributor = fields.Many2one('res.users', string="Contributeur")
    prescription_template = fields.Many2one('prescription.template')
    prescription_lines = fields.One2many('prescription.line', 'prescription', string='Prescription lines')

    def _get_printed_report_name(self):
        return "PRINTED_REPORT"


class PrescriptionLine(models.Model):
    _description = 'Prescription Line'
    _name = "prescription.line"

    prescription = fields.Many2one('prescription')
    product = fields.Many2one('product.template', string='Produit')
    description = fields.Char()
    quantity = fields.Float()

    @api.onchange('product')
    def onchange_product(self):
        self.description = self.product.description_sale


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    prescription_line = fields.One2many('prescription.line', 'product')


class PrescriptionTemplate(models.Model):
    _description = 'Prescription Model'
    _name = "prescription.template"

    name = fields.Char()
    prescription_lines_template = fields.One2many('prescription.line.template', 'prescription_template', string='Prescription lines')


class PrescriptionLineTemplate(models.Model):
    _description = 'Prescription Line Template'
    _name = 'prescription.line.template'

    prescription_template = fields.Many2one('prescription.template')
    product = fields.Many2one('product.template', string='Produit')
    description = fields.Char()
    quantity = fields.Float()

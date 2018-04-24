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


class Prescription(models.Model):
    _description = 'Prescription'
    _name = "prescription"

    def _default_date(self):
        return fields.Date.context_today(self)

    date = fields.Date(string="Date d'intervention", default=_default_date)
    patient = fields.Many2one('res.partner', string="Patient")
    prescription_template = fields.Many2one('prescription.template')
    prescription_lines = fields.One2many('prescription.line', 'prescription', string='Prescription lines')
    prescription_lines_count = fields.Integer()

    def _get_printed_report_name(self):
        return "PRINTED_REPORT"

    @api.onchange('prescription_template')
    def onchange_prescription_template(self):
        self.prescription_lines = False

        prescription_line_ids = []
        for prescription_line_template in self.prescription_template.prescription_lines_template:
            prescription_line = self.env['prescription.line'].create({
                'product': prescription_line_template.product.id,
                'quantity': prescription_line_template.quantity,
                'description': prescription_line_template.description,
            })
            prescription_line_ids.append(prescription_line.id)

        self.update({'prescription_lines': [(6, 0, prescription_line_ids)]})

    @api.onchange('prescription_lines')
    def onchange_lines(self):
        self.prescription_lines_count = len(self.prescription_lines)


class PrescriptionLine(models.Model):
    _description = 'Prescription Line'
    _name = "prescription.line"
    _order = 'sequence'

    prescription = fields.Many2one('prescription')
    product = fields.Many2one('product.template', string='Produit', required=True)
    quantity = fields.Float()
    description = fields.Char()
    sequence = fields.Integer()
    prescription_lines_count = fields.Integer(related='prescription.prescription_lines_count')

    @api.onchange('product')
    def onchange_product(self):
        self.description = self.product.description_sale
        self.sequence = self.prescription_lines_count + 1


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
    product = fields.Many2one('product.template', string='Produit', required=True)
    description = fields.Char()
    quantity = fields.Float()

    @api.onchange('product')
    def onchange_product(self):
        self.description = self.product.description_sale

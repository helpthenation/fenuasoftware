# -*- coding: utf-8 -*-
import time
from datetime import datetime, timedelta
from dateutil import relativedelta

import babel

from odoo import api, fields, models, tools, _


class MedicalInformationDocument(models.Model):
    _description = "Formulaire d'Information Médical"
    _name = "medical.information.document"
    _inherit = ['mail.thread']

    name = fields.Char(string="Nom du document")
    title = fields.Char(string="Titre du document")
    content = fields.Html(string="Contenu")
    sale_order = fields.Many2one('sale.order')


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    medical_information_documents = fields.Many2many(comodel_name="medical.information.document", inverse_name="sale_order")

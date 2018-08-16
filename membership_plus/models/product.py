# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Product(models.Model):
    _inherit = 'product.template'

    membership_counter = fields.Integer(string="Compteur")
    membership_recurring_interval = fields.Selection([('month', 'Mois'), ('year', 'Année')], string="Récurrence", help="Se répète tous les (Mois/Année)", default=False)

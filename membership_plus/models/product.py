# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Product(models.Model):
    _inherit = 'product.template'

    membership_counter = fields.Integer(string="Compteur")

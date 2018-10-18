# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64
import os
import re

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError


class Company(models.Model):
    _inherit = "res.company"

    fax = fields.Char(string="Fax")
    mobile = fields.Char(string="Mobile")


class ResCompany(models.Model):
    _inherit = 'res.company'

    tahiti_num = fields.Char(related='partner_id.tahiti_num', string='N°Tahiti', size=14)
    rcs_num = fields.Char(related='partner_id.rcs_num', string='N°RC', size=14)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    tahiti_num = fields.Char(string='N°Tahiti', size=14)
    rcs_num = fields.Char(string='N°RC', size=14)

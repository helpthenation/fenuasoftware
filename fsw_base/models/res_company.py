# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64
import os
import re

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError


class Company(models.Model):
    _inherit = "res.company"

    fax = fields.Integer(string="Fax")
    tahiti_num = fields.Char()
    rcs_num = fields.Char()

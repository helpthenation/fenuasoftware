# -*- coding: utf-8 -*-

from odoo import models, fields, api

class TinyMCE(models.Model):
    _name = 'tinymce.tinymce'

    name = fields.Char();
    html = fields.Html();
    tinymce = fields.Html();
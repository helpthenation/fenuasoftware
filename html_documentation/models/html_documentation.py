# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HtmlDocument(models.Model):
    _name = 'html.document'
    _inherit = ['mail.thread']
    _description = 'Document'

    name = fields.Char(string="Nom")
    version = fields.Integer(string="Version", readonly=True)
    html_content = fields.Html(string="Contenus")

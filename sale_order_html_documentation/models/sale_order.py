# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HtmlDocument(models.Model):
    _name = 'html.document'
    _inherit = ['mail.thread']


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    html_documents = fields.Many2many(comodel_name='html.document')

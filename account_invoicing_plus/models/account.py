# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountReconcileModel(models.Model):
    _inherit = "account.reconcile.model"
    _order = 'sequence'
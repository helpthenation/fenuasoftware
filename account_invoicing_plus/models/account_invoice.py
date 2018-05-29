# -*- coding: utf-8 -*-
import time
from datetime import datetime, timedelta
from dateutil import relativedelta

import babel

from odoo import api, fields, models, tools, _


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    period = fields.Char(compute='_compute_period', help='Période calculée sur la date de facture')

    @api.depends('date_invoice')
    def _compute_period(self):
        locale = self.env.context.get('lang') or 'en_US'
        ttyme = datetime.fromtimestamp(time.mktime(time.strptime(self.date_invoice, "%Y-%m-%d")))
        self.period = tools.ustr(babel.dates.format_date(date=ttyme, format='MMMM y', locale=locale))

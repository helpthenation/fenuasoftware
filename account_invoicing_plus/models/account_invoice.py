# -*- coding: utf-8 -*-
import time
from datetime import datetime, timedelta
from dateutil import relativedelta

import babel
import logging

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError

logger = logging.getLogger(__name__)


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    raw_margin = fields.Float(compute="_compute_margin",
                              store=True,
                              help="La somme de toutes les marges générés par les lignes.")
    period = fields.Char(compute='_compute_period', help='Période calculée sur la date de facture')

    @api.depends('date_invoice')
    def _compute_period(self):
        if self.date_invoice:
            locale = self.env.context.get('lang') or 'en_US'
            ttyme = datetime.fromtimestamp(time.mktime(time.strptime(self.date_invoice, "%Y-%m-%d")))
            self.period = tools.ustr(babel.dates.format_date(date=ttyme, format='MMMM y', locale=locale))

    @api.depends('invoice_line_ids')
    def _compute_margin(self):
        for this in self:
            this.raw_margin = 0
            for invoice_line in this.invoice_line_ids:
                this.raw_margin += invoice_line.raw_margin


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    def _default_price_cost(self):
        if self.product_id:
            self.price_cost = self.product_id.standard_price

    price_cost = fields.Float(default=_default_price_cost)
    raw_margin = fields.Float(compute="_compute_margin",
                              store=True,
                              help="La marge brute correspond à la différente entre le prix de vente HT et le prix d’achat HT des marchandises vendues. Formule : Prix de vente HT - Prix d’achat HT = Marge Brute HT")
    margin_rate = fields.Float(compute="_compute_margin",
                               store=True,
                               help="Le taux de marge brute est l’indicateur le plus couramment utilisé pour les entreprises commerciales. Il présente la marge brute en pourcentage du coût d’achat. Formule : Marge brute HT / Coût d’achat HT x 100 = Taux de marge (%)")
    marque_rate = fields.Float(compute="_compute_margin",
                               store=True,
                               help="Le taux de marque compare la marge brute au prix de vente. Formule : Marge Brute HT / Prix de vente HT x 100 = Taux de marque")
    multiplier = fields.Float(compute="_compute_margin", store=True, string="Coefficient multiplicateur",
                              help="De nombreux commerçants utilisent le coefficient multiplicateur pour déterminer leur prix de vente TTC à partir du prix d’achat HT de leurs marchandises.")

    @api.onchange('product_id')
    def _assign_standard_price(self):
        self._default_price_cost()

    @api.depends('price_unit', 'quantity', 'price_cost')
    def _compute_margin(self):
        for this in self:
            if this.product_id:
                price_unit = this.price_unit * this.quantity
                price_cost = this.price_cost * this.quantity
                if price_unit > 0 and price_cost > 0:
                    this.raw_margin = price_unit - price_cost
                    this.margin_rate = (this.raw_margin / price_cost) * 100
                    this.marque_rate = (this.raw_margin / price_unit) * 100
                    this.multiplier = this.price_unit / this.price_cost
                else:
                    logger.error('Price Unit or Price Cost is 0')

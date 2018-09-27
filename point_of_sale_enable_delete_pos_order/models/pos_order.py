# -*- coding: utf-8 -*-

import logging
from datetime import timedelta
from functools import partial

import psycopg2
import pytz

from odoo import api, fields, models, tools, _
from odoo.tools import float_is_zero
from odoo.exceptions import UserError
from odoo.http import request
import odoo.addons.decimal_precision as dp

_logger = logging.getLogger(__name__)


class PosSession(models.Model):
    _inherit = 'pos.session'

    order_count = fields.Integer(compute='_compute_order_count')

    @api.multi
    def _compute_order_count(self):
        for session in self:
            session.order_count = len(session.order_ids)


class PosOrder(models.Model):
    _inherit = "pos.order"

    @api.multi
    def action_pos_order_cancel(self):
        self.statement_ids = False
        return self.write({'state': 'cancel'})

    @api.multi
    def unlink(self):
        session_ids = []
        for pos_order in self.filtered(lambda pos_order: pos_order.state not in ['draft', 'cancel']):
            pos_order.action_pos_order_cancel()
            session_ids.append(pos_order.session_id)
        res = super(PosOrder, self).unlink()
        return res

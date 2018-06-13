# -*- coding: utf-8 -*-
import logging
from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT

from odoo.addons.calendar.models.calendar import get_real_ids

_logger = logging.getLogger(__name__)


class Meeting(models.Model):
    _inherit = 'calendar.event'

    @api.model
    def search(self, args, offset=0, limit=0, order=None, count=False):
        """
        Corriger un bug dans le calendrier lorsqu'on est en affichage par Jour, tous les événements ne s'affichent pas.
        Un ticket à été remonté sur le repos d'Odoo : [11.0] Calendar Event not showing in Calendar's Day Mode #23246
        """
        self._fixargs(args)
        res = super(Meeting, self).search(args, offset, limit, order, count)
        return res

    def _fixargs(self, args):
        """
        Méthode qui ajoute 2 jours à l'argument start. Probablement due au Timezone.
        :param args: liste d'arguement à traiter
        :customer concerns: Cyrille SERRA
        """
        index = -1
        for arg in args:
            index += 1
            if 'start' in arg:
                start = datetime.strptime(arg[2], DEFAULT_SERVER_DATETIME_FORMAT)
                start = (start + timedelta(days=2)).strftime('%Y-%m-%d 00:00:00')
                args[index] = ('start', arg[1], start)

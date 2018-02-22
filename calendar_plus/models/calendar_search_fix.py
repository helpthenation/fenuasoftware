# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api

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
        _logger.info("search(" + str(args) + ")")
        res = super(Meeting, self).search(args, offset, limit, order, count)
        return res

    def _fixargs(self, args):
        """
        Méthode qui enlève l'argument start car génère un bug d'affichage. Probablement due au Timezone.
        :param args: liste d'arguement à traiter
        :customer concerns: Cyrille SERRA
        """
        for arg in args:
            if 'start' in arg:
                args.remove(arg)

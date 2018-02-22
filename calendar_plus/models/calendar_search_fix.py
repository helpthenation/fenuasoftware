# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Meeting(models.Model):
    _inherit = 'calendar.event'

    @api.model
    def search(self, args, offset=0, limit=0, order=None, count=False):
        """
        Corriger un bug dans le calendrier lorsqu'on est en affichage par Jour, tous les événements ne s'affichent pas.
        Un ticket à été remonté sur le repos d'Odoo : [11.0] Calendar Event not showing in Calendar's Day Mode #23246
        """
        args = []
        res = super(Meeting, self).search(args, offset, limit, order, count)
        return res

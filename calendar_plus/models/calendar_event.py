# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    partner_details = fields.Char(compute='_get_partner_details', string='Attendees')

    @api.multi
    def _get_partner_details(self):
        for event in self:
            event.partner_details = ""
            for partner_id in event.partner_ids:
                event.partner_details += (partner_id.name if partner_id.name else "") + " " + (str(partner_id.mobile) if partner_id.mobile else "") + " " + (str(partner_id.birthdate) if partner_id.birthdate else "")
                event.partner_details += ", "

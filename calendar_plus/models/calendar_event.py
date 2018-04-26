# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    partner_details = fields.Char(compute='_get_partner_details', string='Attendees')

    @api.model
    def create(self, values):
        if 'appointment_type_id' in values:
            for item in values.get('partner_ids'):
                # item = ([0,id,False])
                # item[1] return partner's id
                user = self.env['res.users'].search([('partner_id', '=', item[1])])
                if user:
                    values['user_id'] = user.id
                    break;

        event = super(CalendarEvent, self).create(values)
        return event

    @api.multi
    def _get_partner_details(self):
        for event in self:
            event.partner_details = ""
            for partner_id in event.partner_ids:
                event.partner_details += (partner_id.name if partner_id.name else "") + " " + (str(partner_id.mobile) if partner_id.mobile else "") + " " + (str(partner_id.birthdate) if partner_id.birthdate else "")
                event.partner_details += ", "

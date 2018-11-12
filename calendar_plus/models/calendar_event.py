# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    partner_details = fields.Char(compute='_get_partner_details', string='Participants')

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

    @api.onchange('user_id')
    def onchange_user_id(self):
        ids = []
        for i in range(0, len(self.partner_ids)):
            ids.append(self.partner_ids[i].id)

        if self.user_id.partner_id not in self.partner_ids:
            ids.append(self.user_id.partner_id.id)
            self.update({'partner_ids': [(6, 0, ids)]})

    @api.multi
    def _get_partner_details(self):
        for event in self:
            event.partner_details = ""
            hide_user_in_calendar_event = self.env['ir.config_parameter'].sudo().get_param('calendar_plus.hide_user_in_calendar_event')
            if hide_user_in_calendar_event:
                for partner_id in event.partner_ids:
                    is_a_user = self.env['res.users'].search_count([('partner_id', '=', partner_id.id)])
                    if is_a_user == 0:
                        event.partner_details += (partner_id.name if partner_id.name else "") + " " + (str(partner_id.mobile) if partner_id.mobile else "") + " " + (str(partner_id.birthdate) if partner_id.birthdate else "")
                        event.partner_details += ", "
            else:
                for partner_id in event.partner_ids:
                    event.partner_details += (partner_id.name if partner_id.name else "") + " " + (str(partner_id.mobile) if partner_id.mobile else "") + " " + (str(partner_id.birthdate) if partner_id.birthdate else "")
                    event.partner_details += ", "

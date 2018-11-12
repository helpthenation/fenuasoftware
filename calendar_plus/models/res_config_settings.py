# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_web_calendar_config_mac5 = fields.Boolean("Web Calendar Configuration")
    show_attendees_details = fields.Boolean("Masque les photos des participants et affiche des détails à la place")
    hide_user_in_calendar_event = fields.Boolean("Masquer utilisateur dans les événements de calendrier ")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            show_attendees_details=self.env['ir.config_parameter'].sudo().get_param('calendar_plus.show_attendees_details'),
            hide_user_in_calendar_event=self.env['ir.config_parameter'].sudo().get_param('calendar_plus.hide_user_in_calendar_event'),
        )
        return res

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('calendar_plus.show_attendees_details', self.show_attendees_details)
        view = self.env.ref('calendar_plus.view_calendar_event_display_form')
        view.update({'active': self.show_attendees_details})

        self.env['ir.config_parameter'].sudo().set_param('calendar_plus.hide_user_in_calendar_event', self.hide_user_in_calendar_event)

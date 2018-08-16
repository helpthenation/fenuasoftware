# -*- coding: utf-8 -*-

import random
from dateutil.relativedelta import relativedelta
from datetime import date
from odoo import api, fields, models, _

STATE = [
    ('none', 'Non Member'),
    ('canceled', 'Cancelled Member'),
    ('old', 'Old Member'),
    ('waiting', 'Waiting Member'),
    ('invoiced', 'Invoiced Member'),
    ('free', 'Free Member'),
    ('paid', 'Paid Member'),
]


class MembershipInvoice(models.TransientModel):
    _inherit = "membership.invoice"

    date_from = fields.Date(string='From')
    date_to = fields.Date(string='To')
    membership_counter = fields.Integer(string="Compteur")

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.membership_counter = self.product_id.membership_counter
        self.date_from = fields.date.today()
        self.onchange_date_from()

    @api.onchange('date_from')
    def onchange_date_from(self):
        if self.product_id.membership_recurring_interval:
            if self.product_id.membership_recurring_interval == 'month':
                self.date_to = fields.Date.to_string(fields.Date.from_string(self.date_from) + relativedelta(months=+1, days=-1))
            elif self.product_id.membership_recurring_interval == 'year':
                self.date_to = fields.Date.to_string(fields.Date.from_string(self.date_from) + relativedelta(years=+1, days=-1))

    @api.multi
    def membership_invoice(self):
        if self:
            datas = {
                'membership_product_id': self.product_id.id,
                'amount': self.member_price,
                'date_from': self.date_from,
                'date_to': self.date_to,
                'membership_counter': self.membership_counter,
            }
        invoice_list = self.env['res.partner'].browse(self._context.get('active_ids')).create_membership_invoice(datas=datas)

        search_view_ref = self.env.ref('account.view_account_invoice_filter', False)
        form_view_ref = self.env.ref('account.invoice_form', False)
        tree_view_ref = self.env.ref('account.invoice_tree', False)

        return {
            'domain': [('id', 'in', invoice_list)],
            'name': 'Membership Invoices',
            'res_model': 'account.invoice',
            'type': 'ir.actions.act_window',
            'views': [(tree_view_ref.id, 'tree'), (form_view_ref.id, 'form')],
            'search_view_id': search_view_ref and search_view_ref.id,
        }


class MembershipLine(models.Model):
    _inherit = 'membership.membership_line'

    date_from = fields.Date(string='From', readonly=False)
    date_to = fields.Date(string='To', readonly=False)
    membership_counter = fields.Integer(string="Compteur")
    display_warning = fields.Boolean(compute='_compute_display_warning')

    @api.depends('date_from', 'date_to', 'membership_counter')
    def _compute_display_warning(self):
        for this in self:
            if this.date_from is not False and this.date_to is not False and this.membership_counter:
                this.display_warning = True
            else:
                this.display_warning = False


class Partner(models.Model):
    _inherit = 'res.partner'

    membership_barcode = fields.Char()
    membership_attendances = fields.One2many('membership.attendance', 'member')

    def generate_membership_barcode(self):
        # self.membership_barcode = "".join(random.sample("abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?", 12))
        self.membership_barcode = "".join(random.sample("01234567890", 4))
        print(self.membership_barcode)

    @api.multi
    def create_membership_invoice(self, product_id=None, datas=None):
        invoice_list = super(Partner, self).create_membership_invoice(product_id, datas)
        for invoice in invoice_list:
            for invoice_line in self.env['account.invoice'].browse([invoice]).invoice_line_ids:
                member_lines = self.env['membership.membership_line'].search([('account_invoice_line', '=', invoice_line.id)])
                if member_lines:
                    for member_line in member_lines:
                        member_line.date_from = datas.get('date_from')
                        member_line.date_to = datas.get('date_to')
                        member_line.membership_counter = datas.get('membership_counter')

        return invoice_list


class MembershipAttendance(models.Model):
    _name = 'membership.attendance'
    _description = 'Fréquentation'

    name = fields.Char()
    date = fields.Datetime()
    member = fields.Many2one('res.partner')
    membership_state = fields.Selection(STATE,
                                        string='Current Membership Status', store=True,
                                        help='It indicates the membership state.\n'
                                             '-Non Member: A partner who has not applied for any membership.\n'
                                             '-Cancelled Member: A member who has cancelled his membership.\n'
                                             '-Old Member: A member whose membership date has expired.\n'
                                             '-Waiting Member: A member who has applied for the membership and whose invoice is going to be created.\n'
                                             '-Invoiced Member: A member whose invoice has been created.\n'
                                             '-Paying member: A member who has paid the membership fee.')

    @api.model
    def check_code(self, code):
        domain = [('membership_barcode', '=', code)]
        results = self.env['res.partner'].search(domain)
        res = {}
        membership_counter = 0
        if len(results) == 1:
            member = results[0]
            for mline in member.member_lines:
                if mline.membership_counter > 0:
                    mline.update({'membership_counter': mline.membership_counter - 1})
                    membership_counter = mline.membership_counter

            self.create(self.prepare_data(member))
            res = {
                'name': member.name,
                'membership_start': member.membership_start,
                'membership_stop': member.membership_stop,
                'membership_counter': membership_counter,
                'status': member.membership_state,
            }
            member._compute_membership_state()
        else:
            res = {
                'status': 'unknown',
            }

        return res

    def prepare_data(self, member):
        data = {
            'name': '',
            'date': fields.datetime.now(),
            'member': member.id,
            'membership_state': member.membership_state,
        }
        return data

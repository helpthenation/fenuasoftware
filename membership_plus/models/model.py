# -*- coding: utf-8 -*-

import random
from odoo import api, fields, models, _


class MembershipInvoice(models.TransientModel):
    _inherit = "membership.invoice"

    date_from = fields.Date(string='From')
    date_to = fields.Date(string='To')

    @api.multi
    def membership_invoice(self):
        if self:
            datas = {
                'membership_product_id': self.product_id.id,
                'amount': self.member_price,
                'date_from': self.date_from,
                'date_to': self.date_to,
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


class Partner(models.Model):
    _inherit = 'res.partner'

    membership_barcode = fields.Char()
    membership_inscriptions = fields.One2many('membership.inscription', 'member')

    def generate_membership_barcode(self):
        self.membership_barcode = "".join(random.sample("abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?", 12))
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

        return invoice_list


class MembershipInscription(models.Model):
    _name = 'membership.inscription'

    name = fields.Char()
    date = fields.Datetime()
    member = fields.Many2one('res.partner')

    @api.model
    def check_code(self, code):
        domain = [('membership_barcode', '=', code)]
        results = self.env['res.partner'].search(domain)
        res = {}
        if len(results) == 1:
            member = results[0]
            res = {
                'name': member.name,
                'membership_start': member.membership_state,
                'membership_stop': member.membership_stop,
                'status': member.membership_state,
            }
        else:
            res = {
                'status': 'unknown',
            }
        return res

# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class Partner(models.Model):
    _inherit = 'res.partner'

    def _compute_membership_stop(self):
        MemberLine = self.env['membership.membership_line']
        for partner in self:
            partner.membership_stop = self.env['membership.membership_line'].search([
                ('partner', '=', partner.associate_member.id or partner.id), ('date_cancel', '=', False), ('date_from', '!=', False), ('date_to', '!=', False)
            ], limit=1, order='date_to desc').date_to

    def _membership_state(self):
        res = super(Partner, self)._membership_state()

        s = 4
        for partner in self:
            if partner.member_lines:
                for mline in partner.member_lines:
                    if mline.membership_counter > 0:
                        if mline.account_invoice_line.invoice_id:
                            mstate = mline.account_invoice_line.invoice_id.state
                        if mstate == 'paid':
                            s = 0
                            inv = mline.account_invoice_line.invoice_id
                            for payment in inv.payment_ids:
                                if any(payment.invoice_ids.filtered(lambda inv: inv.type == 'out_refund')):
                                    s = 2
                            break
                        elif mstate == 'open' and s != 0:
                            s = 1
                        elif mstate == 'cancel' and s != 0 and s != 1:
                            s = 2
                        elif mstate == 'draft' and s != 0 and s != 1:
                            s = 3
                if s == 0:
                    res[partner.id] = 'paid'
                elif s == 1:
                    res[partner.id] = 'invoiced'
                elif s == 2:
                    res[partner.id] = 'canceled'
                elif s == 3:
                    res[partner.id] = 'waiting'

        return res

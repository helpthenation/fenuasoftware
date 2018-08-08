# -*- coding: utf-8 -*-

import logging
import datetime
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT

from odoo import api, fields, models, _
from odoo.exceptions import UserError

logger = logging.getLogger(__name__)


class AccountPayment(models.Model):
    _inherit = "account.payment"

    invoiced_schedule = fields.Many2one('account.invoice')

    def action_validate_and_schedule_payments(self):
        self.action_validate_invoice_payment()
        return {
            "type": "ir.actions.act_window",
            "res_model": "account.payment.schedule",
            "views": [[False, "form"]],
            "target": "new",
            "context": {'active_id': self.id}
        }

    @api.multi
    def action_assign_invoiced_schedule(self):
        for move_line in self.move_line_ids:
            if move_line.account_id == self.invoiced_schedule.account_id:
                self.invoiced_schedule.register_payment(move_line)
                return True

        raise UserError(_("No move line matching current payment!"))

class AccountPaymentSchedule(models.TransientModel):
    _name = "account.payment.schedule"
    _description = "Payment Schedule"

    def _default_amount(self):
        account_payment = self.env['account.payment'].browse(self._context['active_id'])
        return account_payment.invoice_ids[0].residual if len(account_payment.invoice_ids) > 0 else False

    amount = fields.Float(default=_default_amount, required=True)
    day_of_month = fields.Selection([('5', '5'), ('30', '30'), ], default='5', required=True)
    split_number = fields.Integer(required=True)
    start_this_month = fields.Boolean(default=False)

    def action_test(self):
        account_payment = self.env['account.payment'].browse(self._context['active_id'])
        self.update({'invoices_payment_scheduled': (6, False, account_payment.invoice_ids)})

    def action_schedule_payments(self):
        if self.split_number == 0:
            raise UserError(_("Split Number can not be 0"))

        if self.start_this_month and self.day_of_month == '5':
            now = datetime.date.today()
            payment_date = datetime.date.today() + relativedelta(day=5, months=0)
            if now > payment_date:
                raise UserError(_("Current date : " + now.strftime(
                    DEFAULT_SERVER_DATE_FORMAT) + " exceed next payment date: " + payment_date.strftime(
                    DEFAULT_SERVER_DATE_FORMAT)))

        account_payment = self.env['account.payment'].browse(self._context['active_id'])
        amount = self.amount / self.split_number
        count = 0
        iteration = 1
        max_count = self.split_number
        while count < max_count:
            count += 1

            # PAYMENT DATE
            if self.start_this_month:
                if self.day_of_month == '5':
                    if count == 1:  # START THIS MONTH
                        payment_date = datetime.date.today() + relativedelta(day=5)
                    else:  # THEN GOES NEXT MONTH
                        payment_date = datetime.date.today() + relativedelta(day=5, months=+(count - 1))

                    payment_date = payment_date.strftime(DEFAULT_SERVER_DATE_FORMAT)
                elif self.day_of_month == '30':
                    payment_date = datetime.date.today() + relativedelta(day=1, months=+count, days=-1)
                    payment_date = payment_date.strftime(DEFAULT_SERVER_DATE_FORMAT)
                else:
                    raise UserError(_("Day of month not recognize"))
            else:
                if self.day_of_month == '5':
                    payment_date = datetime.date.today() + relativedelta(day=5, months=+count)
                    payment_date = payment_date.strftime(DEFAULT_SERVER_DATE_FORMAT)
                elif self.day_of_month == '30':
                    if count == 1:  # START NEXT MONTH NOT THIS MONTH
                        count += 1
                        max_count += 1
                    payment_date = datetime.date.today() + relativedelta(day=1, months=+count, days=-1)
                    payment_date = payment_date.strftime(DEFAULT_SERVER_DATE_FORMAT)
                else:
                    raise UserError(_("Day of month not recognize"))

            # COMMUNICATION
            iteration += 1
            communication = account_payment.communication + "RGLT: " + str(iteration) + "/" + str(self.split_number)

            #INVOICED_SCHEDULE
            invoice = account_payment.invoice_ids[0]

            # RECORD
            new_account_payment = account_payment.copy({
                'payment_date': payment_date,
                'amount': amount,
                'communication': communication,
                'invoiced_schedule': invoice.id
            })
            new_account_payment.post()
        return True

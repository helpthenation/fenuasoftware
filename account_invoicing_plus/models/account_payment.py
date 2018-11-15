# -*- coding: utf-8 -*-
import logging
import datetime
from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.exceptions import UserError

logger = logging.getLogger(__name__)

class account_abstract_payment(models.AbstractModel):
    _inherit = "account.payment"

    SELECTION = [('open', 'Keep open'), ('reconcile', 'Mark invoice as fully paid')]

    payment_difference_handling = fields.Selection(SELECTION, default='open', string="Payment Difference", copy=False)

    day_of_month = fields.Selection([('5', '5'), ('30', '30'), ], default='5', required=True)
    split_number = fields.Integer()
    start_this_month = fields.Boolean(default=False)
    invoiced_schedule = fields.Many2one('account.invoice')

    def _schedule_payments(self, amount):
        if self.split_number == 0:
            raise UserError(_("Split Number can not be 0"))

        if self.start_this_month and self.day_of_month == '5':
            now = datetime.date.today()
            payment_date = datetime.date.today() + relativedelta(day=5, months=0)
            if now > payment_date:
                raise UserError(_("Current date : " + now.strftime(
                    DEFAULT_SERVER_DATE_FORMAT) + " exceed next payment date: " + payment_date.strftime(
                    DEFAULT_SERVER_DATE_FORMAT)))

        amount = amount / self.split_number
        count = 0
        iteration = 0
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
            communication = self.communication + " RGLT: " + str(iteration) + "/" + str(self.split_number)

            # INVOICE
            active_ids = self._context.get('active_ids')
            invoices = self.env['account.invoice'].browse(active_ids)

            # RECORD
            new_account_payment = self.copy({
                'payment_date': payment_date,
                'amount': amount,
                'communication': communication,
                'invoiced_schedule': invoices[0].id,
                'invoice_ids': False,
            })
            new_account_payment.post()
        return True


class AccountPayment(models.Model):
    _inherit = "account.payment"

    invoiced_schedule = fields.Many2one('account.invoice')

    def action_validate_invoice_payment(self):
        amount = self.payment_difference  # hack to avoid having difference after action_validate_invoice_payment()
        super(AccountPayment, self).action_validate_invoice_payment()
        if self.payment_difference_handling == 'schedule':
            self._schedule_payments(amount)

    @api.multi
    def action_assign_invoiced_schedule(self):
        for move_line in self.move_line_ids:
            if move_line.account_id == self.invoiced_schedule.account_id:
                self.invoiced_schedule.register_payment(move_line)
                return True

        raise UserError(_("No move line matching current payment!"))

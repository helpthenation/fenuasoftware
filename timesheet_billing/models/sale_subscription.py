# -*- coding: utf-8 -*-

import logging

from odoo import models, api, fields
from time import sleep

_logger = logging.getLogger(__name__)

class SaleSubscription(models.Model):
    _inherit = "sale.subscription"
    
    # @override SaleSubscription.recurring_invoice()
    # @see sale_contract.models.sale_subscription: SaleSubscription.recurring_invoice()
    @api.multi
    def recurring_invoice(self):
        invoice_ids = self._recurring_create_invoice()

        for invoice_id in invoice_ids:
            invoice_lines = self.env['account.invoice.line'].search([('invoice_id', '=', invoice_id)])
            for invoice_line in invoice_lines:
                if invoice_line.product_id.invoice_policy == 'order':
                    _logger.info("nothing to do for now")
                    
                elif invoice_line.product_id.invoice_policy == 'delivery':
                    _logger.info("is a delivery")
                    invoice_line.quantity = 0;
                    billable_timesheet_ids = self.env['account.analytic.line'].search([('project_id','!=', False), ('account_id', '=', self.analytic_account_id.id), ('product_id', '=', invoice_line.product_id.id), ('billed', '=', False)])
                    for billable_timesheet in billable_timesheet_ids:
                        billable_timesheet.invoice = invoice_id
                        billable_timesheet.billed = True;
                        billable_timesheet.billed_amount = billable_timesheet.unit_amount;
                        if invoice_line.uom_id == billable_timesheet.product_uom_id:
                            invoice_line.quantity += billable_timesheet.billed_amount
                        else :
                            invoice_line.quantity += billable_timesheet.product_uom_id._compute_quantity(billable_timesheet.billed_amount, invoice_line.uom_id)

                        if self.template_id.reset_timesheet_duration_on_invoice:
                            billable_timesheet.unit_amount = 0.0
                else:
                    _logger.warn("Product is either not on order or delivery")
            
            invoice = self.env['account.invoice'].browse([invoice_id])
            invoice.compute_taxes()
            invoice._compute_amount()

        return self.action_subscription_invoice()


class SaleSubscriptionTemplate(models.Model):
    _inherit = "sale.subscription.template"

    reset_timesheet_duration_on_invoice = fields.Boolean(String='Reset timesheet duration on invoice', help='if checkd, when invoice is generated, the duration of all timesheet is set to 0', default=True)
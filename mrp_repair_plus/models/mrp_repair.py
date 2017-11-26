# -*- coding: utf-8 -*-


from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime


class Repair(models.Model):
    _inherit = 'mrp.repair'

    repairer = fields.Many2one('res.users', string='Réparateur', index=True)
    purchase_order = fields.Many2one('purchase.order', 'Bon de commande', copy=False, readonly=True, track_visibility="onchange")

    @api.multi
    def action_created_purchase_order(self):
        self.ensure_one()
        return {
            'name': _('Création de bon de commande'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'purchase.order',
            'view_id': self.env.ref('purchase.purchase_order_form').id,
            'target': 'current',
            'res_id': self.purchase_order.id,
        }

    def action_repair_purchase_order_create(self):
        for repair in self:
            repair.action_purchase_order_create()
        return True

    @api.multi
    def action_purchase_order_create(self):
        """ Creates purchase order for repair order.
        @return: purchase order id.
        """
        print(fields.Datetime.now())
        PurchaseOrder = self.env['purchase.order']
        PurchaseOrderLine = self.env['purchase.order.line']
        for repair in self.filtered(lambda repair: repair.state not in ('draft', 'cancel') and not repair.purchase_order):
            if not repair.partner_id.id and not repair.partner_invoice_id.id:
                raise UserError(_('You have to select a Partner Invoice Address in the repair form!'))
            purchase_order = PurchaseOrder.create({
                'partner_id': repair.partner_invoice_id.id or repair.partner_id.id,
                'currency_id': repair.pricelist_id.currency_id.id,
                'date_planned': fields.Datetime.now(),
            })
            purchase_order.write({'date_planned': purchase_order.date_order})
            repair.write({'purchase_order': purchase_order.id})
            for operation in repair.operations:
                if operation.type == 'add':
                    name = operation.name

                    if operation.product_id.property_account_income_id:
                        account_id = operation.product_id.property_account_income_id.id
                    elif operation.product_id.categ_id.property_account_income_categ_id:
                        account_id = operation.product_id.categ_id.property_account_income_categ_id.id
                    else:
                        raise UserError(_('No account defined for product "%s".') % operation.product_id.name)

                    purchase_order_line = PurchaseOrderLine.create({
                        'order_id': purchase_order.id,
                        'date_planned': purchase_order.date_planned,
                        'name': name,
                        'origin': repair.name,
                        'account_id': account_id,
                        'product_qty': operation.product_uom_qty,
                        'invoice_line_tax_ids': [(6, 0, [x.id for x in operation.tax_id])],
                        'product_uom': operation.product_uom.id,
                        'price_unit': operation.price_unit,
                        'price_subtotal': operation.product_uom_qty * operation.price_unit,
                        'product_id': operation.product_id and operation.product_id.id or False
                    })
                    operation.write({'purchase_order_line': purchase_order_line.id})


class RepairLine(models.Model):
    _inherit = 'mrp.repair.line'

    purchase_order_line = fields.Many2one('purchase.order.line', 'Purchase Order Line', copy=False, readonly=True)

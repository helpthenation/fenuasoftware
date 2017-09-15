# -*- coding: utf-8 -*-

import time
import tempfile
import base64
import contextlib
import cStringIO
import babel
from dateutil import parser
from datetime import datetime, timedelta
from dateutil import relativedelta
from odoo import fields, models, _, api, tools
from odoo.exceptions import Warning
from odoo.exceptions import UserError, RedirectWarning, ValidationError

class VatRealReport(models.TransientModel):
    _name = "vat.real.report"
    _description = "Vat Real Report"

    user_id = fields.Many2one('res.users', string='Owner', default=lambda self: self.env.uid)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id)
    type = fields.Selection([('monthly', 'Mensuel'), ('quarterly', 'Trimestrielle')], 'Reporting Period', default='monthly', required=True)
    monthly = fields.Selection([('1','Janvier'), ('2','Février'), ('3','Mars'),
                                ('4','Avril'), ('5','Mai'), ('6','Juin'),
                                ('7','Juillet'), ('8','Août'), ('9','Septembre'),
                                ('10','Octobre'), ('11','Novembre'), ('12','Décembre')],
                               "Mois")
    quarterly = fields.Selection([('1','Janver-Mars'),('2','Avril-Juin'),('3','Juillet-Septembre'),('4','Octobre-Décembre')], 'Trimestre')
    date_from = fields.Date(string="Start date", required=True, default=time.strftime('%Y-%m-01'))
    date_to = fields.Date(string="End date", required=True, default=str(datetime.now() + relativedelta.relativedelta(months=+1, day=1, days=-1))[:10])
    payment_method = fields.Selection([('check',"Chèque(à l'ordre du Trésor Public)"), ('cash','Espèces'), ('wire_transfert','Virement bancaire (Préciser le N°TAHITI, la taxe payée et la période concernée')])

    sales = fields.Float()
    services = fields.Float()
    exportations = fields.Float()
    others = fields.Float()

    reduced_rate_base_amount = fields.Float()
    intermediate_rate_base_amount = fields.Float()
    normal_rate_base_amount = fields.Float()
    other_rate_base_amount = fields.Float()
    reduced_rate_amount = fields.Float()
    intermediate_rate_amount = fields.Float()
    normal_rate_amount = fields.Float()
    other_rate_amount = fields.Float()

    VAT_on_assets_constituting_fixed_assets = fields.Float()
    VAT_on_other_goods_and_services = fields.Float()

    @api.onchange('monthly')
    def onchange_monthly(self):
        current_year = int(datetime.strftime(datetime.now(), '%Y'))
        from_date = time.strftime('%Y-%m-01');
        if self.monthly:
            from_date = str(current_year) + "-" + str(self.monthly) + "-01"
        self.date_from = datetime.strptime(from_date, '%Y-%m-%d')
        self.date_to = str(datetime.strptime(from_date, '%Y-%m-%d') + relativedelta.relativedelta(months=+1, day=1, days=-1))[:10]

    @api.onchange('quarterly')
    def onchange_quarterly(self):
        current_year = int(datetime.strftime(datetime.now(), '%Y'))
        from_date = time.strftime('%Y-%m-01');
        if self.quarterly:
            if self.type == 'quarterly' and self.quarterly == '1':
                from_date = str(current_year) + "-01-01"
            elif self.type == 'quarterly' and self.quarterly == '2':
                from_date = str(current_year) + "-04-01"
            elif self.type == 'quarterly' and self.quarterly == '3':
                from_date = str(current_year) + "-07-01"
            elif self.type == 'quarterly' and self.quarterly == '4':
                from_date = str(current_year) + "-10-01"

        self.date_from = datetime.strptime(from_date, '%Y-%m-%d')
        self.date_to = str(datetime.strptime(from_date, '%Y-%m-%d') + relativedelta.relativedelta(months=+3, day=1, days=-1))[:10]

    def prepare_report(self):
        model = self.env['account.move.line']
        account_move_lines = self.env['account.move.line'].search([('date', '>=', self.date_from),('date', '<=', self.date_to)])

        self.prepare_a(account_move_lines)

        self.prepare_b(account_move_lines)

        self.prepare_c(account_move_lines)

    def prepare_a(self, account_move_lines):

        #A - OPERATIONS REALISEES
        self.sales = 0.0
        self.services = 0.0
        self.exportations = 0.0
        self.others = 0.0
        for account_move_line in account_move_lines:
            #VENTES
            if account_move_line.account_id.code.startswith('7071'):
                self.sales += account_move_line.credit
            elif account_move_line.account_id.code.startswith('7072'):
                self.sales += account_move_line.credit

            #PRESTATIONS DE SERVICES
            elif account_move_line.account_id.code.startswith('706'):
                self.services += account_move_line.credit
            elif account_move_line.account_id.code.startswith('708'):
                self.services += account_move_line.credit
            elif account_move_line.account_id.code.startswith('709'):
                self.services += account_move_line.credit
            elif account_move_line.account_id.code.startswith('713450'):
                self.services += account_move_line.credit

            #EXPORTATIONS
            elif account_move_line.account_id.code.startswith('7073'):
                self.exportations += account_move_line.credit

            #AUTRES OPERATIONS NON TAXABLES
            elif account_move_line.account_id.code.startswith('7'):
                self.others += account_move_line.credit

    def prepare_b(self, account_move_lines):
        #B - TVA EXIGIBLE
        self.reduced_rate_base_amount = 0.0
        self.reduced_rate_amount = 0.0
        self.intermediate_rate_base_amount = 0.0
        self.intermediate_rate_amount = 0.0
        self.normal_rate_base_amount = 0.0
        self.normal_rate_amount = 0.0
        self.other_rate_base_amount=0.0
        self.other_rate_amount=0.0
        for account_move_line in account_move_lines:

            income_type = self.env.ref('account.data_account_type_revenue')

            if income_type.id == account_move_line.account_id.user_type_id:
                if self.tax_account_code_startswith(account_move_line.tax_ids, '445710'):
                    self.reduced_rate_base_amount += account_move_line.credit
                elif self.tax_account_code_startswith(account_move_line.tax_ids, '445711'):
                    self.normal_rate_base_amount += account_move_line.credit
                elif self.tax_account_code_startswith(account_move_line.tax_ids, '445712'):
                    self.intermediate_rate_base_amount += account_move_line.credit
                elif self.tax_account_code_startswith(account_move_line.tax_ids, '445780'):
                    self.other_rate_base_amount += account_move_line.credit

            # TVA due Taux Réduit
            elif account_move_line.account_id.code.startswith('445710'):
                self.reduced_rate_amount += account_move_line.credit
            # TVA due Taux Normal
            elif account_move_line.account_id.code.startswith('445711'):
                self.normal_rate_amount += account_move_line.credit
            # TVA due Taux Intermédiaire
            elif account_move_line.account_id.code.startswith('445712'):
                self.intermediate_rate_amount += account_move_line.credit
            # TVA due Taux Réduit
            elif account_move_line.account_id.code.startswith('445780'):
                self.other_rate_amount += account_move_line.credit

    def prepare_c(self, account_move_lines):
        self.VAT_on_assets_constituting_fixed_assets = 0.0
        self.VAT_on_other_goods_and_services = 0.0
        for account_move_line in account_move_lines:

            if account_move_line.account_id.code.startswith('445620'):
                self.VAT_on_assets_constituting_fixed_assets += account_move_line.debit
            elif account_move_line.account_id.code.startswith('445660'):
                self.VAT_on_other_goods_and_services += account_move_line.debit

    def tax_account_code_startswith(self, tax_ids, code):
        for tax in tax_ids:
            if tax.account_id.code.startswith(code):
                return True
        return False

    @api.multi
    def print_report(self):
        self.ensure_one()
        self.prepare_report()
        return self.env['report'].get_action(self, 'l10n_pf.vat_real_template')

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


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    report_sage = fields.Many2one(commodel_name="report.sage", string="Report SAGE")

class ReportSAGE(models.TransientModel):
    _name = "report.sage"
    _description = "Report account.move in a FILE"
    _inherit = ['mail.thread']

    name=fields.Char(string="Reference", readonly=True)
    date_from = fields.Date(string="Date de début", readonly=True, required=True, default=time.strftime('%Y-%m-01'), states={'draft': [('readonly', False)]}, track_visibility='always')
    date_to = fields.Date(string="Date de fin", readonly=True, required=True, default=str(datetime.now() + relativedelta.relativedelta(months=+1, day=1, days=-1))[:10], states={'draft': [('readonly', False)]}, track_visibility='always')
    account_move_lines = fields.One2many(comodel_name="account.move.line", inverse_name="report_sage", string="Ecriture comptable", readonly=True, states={'draft': [('readonly', False)]} )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('valid', 'Validated'),
        ('cancel', 'Canceled'),
    ], string='Status', index=True, readonly=True, copy=False, default='draft', track_visibility='always')
    filename = fields.Char('File Name', readonly=True, track_visibility='always')
    filedata = fields.Binary('File', readonly=True)

    @api.model
    def create(self, vals):
        res = super(ReportSAGE, self).create(vals)
        if (not res.date_from) or (not res.date_to):
            return

        ttyme = datetime.fromtimestamp(time.mktime(time.strptime(res.date_from, "%Y-%m-%d")))
        locale = self.env.context.get('lang', 'en_US')
        res.name = _('%s') % (tools.ustr(babel.dates.format_date(date=ttyme, format='MMMM-y', locale=locale)))
        return res

    def compute(self):
        self.message_post(body='Calcul sur la période ' + str(self.date_from) + ' à ' + str(self.date_to))
        account_move_lines = self.env['account.move.line'].search([('date', '<=', self.date_to), ('date', '>', self.date_from)])
        for account_move_line in account_move_lines:
            account_move_line.report_sage = self.id

    def action_validate(self):
        self.message_post(body='Validation du report avec génération du fichier')
        with contextlib.closing(cStringIO.StringIO()) as buf:
            self.reportSage(buf)
            out = base64.encodestring(buf.getvalue())

        filename = self.name
        name = "%s.%s" % (filename, "prn")
        self.write({'state': 'valid', 'filedata': out, 'filename': name})

    def reportSage(self, buffer):
        writer = PRNFile(buffer)
        writer.start()
        for account_move_line in self.account_move_lines:
            writer.write(account_move_line)
        writer.end()

# class to handle prn files
class PRNFile(object):

    def __init__(self, buffer):
        self.buffer = buffer

    def start(self):
        self.buffer.write(str("Jal").ljust(3))
        self.buffer.write(str("Date").ljust(6))
        self.buffer.write(str("T").ljust(2))
        self.buffer.write(str("Compte Gen.").ljust(13))
        self.buffer.write("X")
        self.buffer.write(str("Compte tiers").ljust(13))
        self.buffer.write(str("Reference").ljust(13))
        self.buffer.write(str("Libelle").ljust(25))
        self.buffer.write(str("P").ljust(1))
        self.buffer.write(str("Ech.").ljust(6))
        self.buffer.write(str("S").ljust(1))
        self.buffer.write(str("Montant").ljust(20))
        self.buffer.write(str("Z").ljust(1))
        self.buffer.write("\n")

    def write_data(self, text, size, align='<'):
        self.buffer.write('{text:{fill}{align}{width}.{size}}'.format(text=text, fill=' ', align=align, width=size, size=size))

    def write(self, account_move_line):
        self.write_data(account_move_line.journal_id.code, 3)
        self.buffer.write(parser.parse(account_move_line.date).strftime('%d%m%y'))
        self.write_data("OD", 2)
        self.write_data(account_move_line.account_id.code.encode('latin-1'), 13)
        if account_move_line.journal_id.type in 'purchase':
            self.buffer.write("A")
            self.write_data(account_move_line.partner_id.name.encode('latin-1'), 13)
        else:
            if account_move_line.partner_id:
                self.buffer.write("X")
                self.write_data(account_move_line.partner_id.name.encode('latin-1'), 13)
            else:
                self.buffer.write(''.ljust(13))
        self.write_data(account_move_line.move_id.name, 13)
        self.write_data(account_move_line.name.encode('latin-1'), 25)
        self.buffer.write("S")
        self.write_data(parser.parse(account_move_line.date_maturity).strftime('%d%m%y'), 6)
        if account_move_line.debit and account_move_line.debit > 0:
            self.buffer.write("D")
            self.write_data(account_move_line.debit, 20, '>')
        elif account_move_line.credit and account_move_line.credit > 0:
            self.buffer.write("C")
            self.write_data(account_move_line.credit, 20, '>')
        else:
            raise UserError(_('Cannot generate file.'))
        self.buffer.write("N")
        self.buffer.write("\n")

    def end(self):
        self.buffer.write("\n\n")
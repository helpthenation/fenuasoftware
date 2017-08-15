from odoo import fields, models, api, _
from odoo.exceptions import UserError
import tempfile
import base64
import contextlib
import cStringIO
from dateutil import parser

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

    def write(self, account_move_line):
        self.buffer.write(account_move_line.journal_id.code.ljust(3))
        self.buffer.write(parser.parse(account_move_line.date).strftime('%d%m%y'))
        self.buffer.write(str("OD").ljust(2))
        self.buffer.write(str(account_move_line.account_id.code.encode('utf-8')).ljust(13))
        if account_move_line.partner_id:
            self.buffer.write("X")
            self.buffer.write(str(account_move_line.partner_id.name.encode('utf-8')).ljust(13))
        else:
            self.buffer.write(''.ljust(13))
        self.buffer.write(account_move_line.move_id.name.ljust(13))
        self.buffer.write(str(account_move_line.name.encode('utf-8')).ljust(25))
        self.buffer.write(str("S").ljust(1))
        self.buffer.write(str(parser.parse(account_move_line.date_maturity).strftime('%d%m%y')).ljust(6))

        if account_move_line.debit and account_move_line.debit > 0:
            self.buffer.write("D")
            self.buffer.write(str(account_move_line.debit).rjust(20))
        elif account_move_line.credit and account_move_line.credit > 0:
            self.buffer.write("C")
            self.buffer.write(str(account_move_line.credit).rjust(20))
        else:
            raise UserError(_('Cannot generate file.'))
        self.buffer.write("N")
        self.buffer.write("\n")

    def end(self):
        self.buffer.write("\n\n")

class ReportSAGE(models.TransientModel):
    _name = "report.sage"
    _description = "Report account.move in a FILE"

    state = fields.Selection([('choose', 'choose'), ('get', 'get')], default='choose')
    name = fields.Char('File Name', readonly=True)
    data = fields.Binary('File', readonly=True)

    @api.multi
    def act_getfile(self):
        #this = self[0]

        with contextlib.closing(cStringIO.StringIO()) as buf:
            self.reportSage(buf)
            out = base64.encodestring(buf.getvalue())

        filename = 'new'
        name = "%s.%s" % (filename, "prn")
        self.write({'state': 'get', 'data': out, 'name': name})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'report.sage',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
        }

    def check_constraints(self, item):
        if len(item.journal_id.code) > 3:
                raise UserError(_('Journal code ' + item.journal_id.code + ' length greater than 3'.encode('utf-8')))

    def reportSage(self, buffer):
        account_move_lines = self.env['account.move.line'].search([])
        writer = PRNFile(buffer)
        writer.start()
        for account_move_line in account_move_lines:
            writer.write(account_move_line)
        writer.end()
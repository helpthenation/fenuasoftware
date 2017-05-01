# -*- coding: utf-8 -*-

'''
Created on 30 janv. 2017

@author: Heifara MATAPO
'''

from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    tahiti_num = fields.Char(string="N°Tahiti")
    rcs_num = fields.Char(string="N°RCS")
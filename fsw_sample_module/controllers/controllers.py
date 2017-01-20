# -*- coding: utf-8 -*-
from odoo import http

# class VctSampleModule(http.Controller):
#     @http.route('/fsw_sample_module/fsw_sample_module/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/fsw_sample_module/fsw_sample_module/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('fsw_sample_module.listing', {
#             'root': '/fsw_sample_module/fsw_sample_module',
#             'objects': http.request.env['fsw_sample_module.fsw_sample_module'].search([]),
#         })

#     @http.route('/fsw_sample_module/fsw_sample_module/objects/<model("fsw_sample_module.fsw_sample_module"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('fsw_sample_module.object', {
#             'object': obj
#         })
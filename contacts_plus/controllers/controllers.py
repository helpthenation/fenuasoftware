# -*- coding: utf-8 -*-
from odoo import http

# class ThemeBackend(http.Controller):
#     @http.route('/theme_backend/theme_backend/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/theme_backend/theme_backend/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('theme_backend.listing', {
#             'root': '/theme_backend/theme_backend',
#             'objects': http.request.env['theme_backend.theme_backend'].search([]),
#         })

#     @http.route('/theme_backend/theme_backend/objects/<model("theme_backend.theme_backend"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('theme_backend.object', {
#             'object': obj
#         })
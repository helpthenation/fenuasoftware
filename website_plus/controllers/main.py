# -*- coding: utf-8 -*-
from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request


class WebsiteSale(WebsiteSale):
    @http.route(['/shop/address'], type='http', methods=['GET', 'POST'], auth="public", website=True)
    def address(self, **kw):
        if 'submitted' in kw:
            kw["country_id"] = request.env.ref('base.pf').id
            kw["street"] = "N/A"
            kw["city"] = "Papeete"
        res = super(WebsiteSale, self).address(**kw)
        return res

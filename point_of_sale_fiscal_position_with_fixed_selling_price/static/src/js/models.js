odoo.define('point_of_sale_fiscal_position_with_fixed_selling_price.models', function (require) {
    "use strict";

    var module = require("point_of_sale.models");

    module.Order.prototype.fix_tax_included_price = function (line) {
        if (this.fiscal_position) {
            var unit_price = line.price;
            var taxes = line.get_taxes();
            var mapped_included_taxes = [];
            _(taxes).each(function (tax) {
                var line_tax = line._map_tax_fiscal_position(tax);
                if (tax.price_include && tax.id != line_tax.id) {

                    mapped_included_taxes.push(tax);
                }
            })

            if (mapped_included_taxes.length > 0) {
                line.compute_all(mapped_included_taxes, unit_price, 1, this.pos.currency.rounding, true).total_excluded;
            }
        }

    }

});

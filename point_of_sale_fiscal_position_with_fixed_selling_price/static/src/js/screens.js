odoo.define('point_of_sale_fiscal_position_with_fixed_selling_price.screens', function (require) {
    "use strict";

    var core = require('web.core');
    var _t = core._t;
    var screens = require('point_of_sale.screens')
    screens.set_fiscal_position_button.include({
        button_click: function () {
            var self = this;

            var no_fiscal_position = [{
                label: _t("None"),
            }];
            var fiscal_positions = _.map(self.pos.fiscal_positions, function (fiscal_position) {
                return {
                    label: fiscal_position.name,
                    item: fiscal_position
                };
            });

            var selection_list = no_fiscal_position.concat(fiscal_positions);
            self.gui.show_popup('selection', {
                title: _t('Select tax'),
                list: selection_list,
                confirm: function (fiscal_position) {
                    var order = self.pos.get_order();
                    order.fiscal_position = fiscal_position;
                    // This will trigger the recomputation of taxes on order lines.
                    // It is necessary to manually do it for the sake of consistency
                    // with what happens when changing a customer.
                    _.each(order.orderlines.models, function (line) {
                        line.set_quantity(line.quantity, true);
                    });
                    order.trigger('change');
                },
                is_selected: function (fiscal_position) {
                    return fiscal_position === self.pos.get_order().fiscal_position;
                }
            });
        },
    });
});
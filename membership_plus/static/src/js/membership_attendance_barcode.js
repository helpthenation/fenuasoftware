odoo.define('membership_plus.MainMenu', function (require) {
    "use strict";

    var core = require('web.core');
    var Widget = require('web.Widget');
    var Dialog = require('web.Dialog');
    var Session = require('web.session');
    var QWeb = core.qweb;


    var _t = core._t;

    var MainMenu = Widget.extend({
        events: {
            "change .o_text_code": function (event) {
                this.check_code($("input[name='code']").val());
            },

            "click .button_check_code": function (event) {
                this.check_code($("input[name='code']").val());
            }
        },

        init: function (parent, action) {
            // Yet, "_super" must be present in a function for the class mechanism to replace it with the actual parent method.
            this._super.apply(this, arguments);
        },

        start: function () {
            var self = this;
            self.session = Session;
            var def = this._rpc({
                model: 'res.company',
                method: 'search_read',
                args: [[['id', '=', this.session.company_id]], ['name']],
            }).then(function (companies) {
                self.company_name = companies[0].name;
                self.company_image_url = self.session.url('/web/image', {model: 'res.company', id: self.session.company_id, field: 'logo',});
                self.$el.html(QWeb.render("membership_attendance_barcode", {widget: self}));
                self.start_clock();
            });
            return $.when(def, this._super.apply(this, arguments));
        },

        start_clock: function () {
            this.clock_start = setInterval(function () {
                this.$(".o_membership_attendance_clock").text(new Date().toLocaleTimeString(navigator.language, {hour: '2-digit', minute: '2-digit'}));
            }, 500);
            // First clock refresh before interval to avoid delay
            this.$(".o_membership_attendance_clock").text(new Date().toLocaleTimeString(navigator.language, {hour: '2-digit', minute: '2-digit'}));
        },

        destroy: function () {
            this._super();
        },

        check_code: function (code) {
            var self = this;
            return this._rpc({
                model: 'membership.attendance',
                method: 'check_code',
                args: [code],
            }).then(function (result) {
                console.log(result);

                $('.o_membership_attendance_barcode_main_menu').addClass('hidden');

                $('#member_name').text(result['name']);
                $('#membership_stop').text(result['membership_stop']);
                $('.o_membership_attendance_barcode_result').removeClass('hidden');
                switch (result['status']) {
                    case 'unknown':
                        $('.o_unknown').removeClass('hidden');
                        break;
                    case 'none':
                        $('.o_none').removeClass('hidden');
                        break;
                    case 'canceled':
                        $('.o_canceled').removeClass('hidden');
                        break;
                    case 'old':
                        $('.o_old').removeClass('hidden');
                        break;
                    case 'waiting':
                        $('.o_waiting').removeClass('hidden');
                        break;
                    case 'invoiced':
                        $('.o_invoiced').removeClass('hidden');
                        break;
                    case 'free':
                        $('.o_free').removeClass('hidden');
                        break;
                    case 'paid':
                        $('.o_paid').removeClass('hidden');
                        break;
                }

                setTimeout(function () {
                    self.reset_ui();
                }, 4000)
            })
        },

        reset_ui: function () {
            $('.o_membership_attendance_barcode_result').addClass('hidden');

            $('.o_text_code').val('')
            $('.o_unknown').addClass('hidden');
            $('.o_none').addClass('hidden');
            $('.o_canceled').addClass('hidden');
            $('.o_old').addClass('hidden');
            $('.o_waiting').addClass('hidden');
            $('.o_invoiced').addClass('hidden');
            $('.o_free').addClass('hidden');
            $('.o_paid').addClass('hidden');
            $('.o_text_code').focus();
            $('.o_membership_attendance_barcode_main_menu').removeClass('hidden')
        },
    });

    core.action_registry.add('membership_barcode_attendance', MainMenu);

    return {
        MainMenu: MainMenu,
    };

});

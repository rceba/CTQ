odoo.define('ctq_customs.SwitchCompanyMenu', function(require) {
"use strict";

    var core = require('web.core');
    var SwitchCompanyMenu = require('web.SwitchCompanyMenu');

    var CTQSwitchCompanyMenu = SwitchCompanyMenu.include({
        //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------

        /**
         * @private
         * @param {MouseEvent|KeyEvent} ev
         */
        _onSwitchCompanyClick: function (ev) {
            this._super.apply(this, arguments);
            if (ev.type == 'keydown' && ev.which != $.ui.keyCode.ENTER && ev.which != $.ui.keyCode.SPACE) {
                return;
            }
            var dropdownItem = $(ev.currentTarget).parent();
            var dropdownMenu = dropdownItem.parent();
            var companyID = dropdownItem.data('company-id');
            this._rpc({
                route: '/web/dataset/call_kw/res.users/reload_mx_group',
                params: {
                    "model": "res.users",
                    "method": "reload_mx_group",
                    "args": [companyID],
                    "kwargs": {}
                },
            })
        },

        //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------

        /**
         * @private
         * @param {MouseEvent|KeyEvent} ev
         */
        _onToggleCompanyClick: function (ev) {
            this._super.apply(this, arguments);
            if (ev.type == 'keydown' && ev.which != $.ui.keyCode.ENTER && ev.which != $.ui.keyCode.SPACE) {
                return;
            }
            var dropdownItem = $(ev.currentTarget).parent();
            var companyID = dropdownItem.data('company-id');
            this._rpc({
                route: '/web/dataset/call_kw/res.users/reload_mx_group',
                params: {
                    "model": "res.users",
                    "method": "reload_mx_group",
                    "args": [companyID],
                    "kwargs": {}
                },
            })
        },

    });
    return CTQSwitchCompanyMenu;
});
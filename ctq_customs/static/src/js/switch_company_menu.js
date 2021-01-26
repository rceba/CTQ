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
            var allowed_company_ids = this.allowed_company_ids;
            if (dropdownItem.find('.fa-square-o').length) {
                // 1 enabled company: Stay in single company mode
                if (this.allowed_company_ids.length === 1) {
                    if (this.isMobile) {
                        dropdownMenu = dropdownMenu.parent();
                    }
                    allowed_company_ids = [companyID];
                } else { // Multi company mode
                    allowed_company_ids.push(companyID);
                }
            }
            this._rpc({
                route: '/web/dataset/call_kw/res.users/reload_mx_group',
                params: {
                    "model": "res.users",
                    "method": "reload_mx_group",
                    "args": [allowed_company_ids],
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
            var allowed_company_ids = this.allowed_company_ids;
            var current_company_id = allowed_company_ids[0];
            if (dropdownItem.find('.fa-square-o').length) {
                allowed_company_ids.push(companyID);
            } else {
                allowed_company_ids.splice(allowed_company_ids.indexOf(companyID), 1);
            }
            this._rpc({
                route: '/web/dataset/call_kw/res.users/reload_mx_group',
                params: {
                    "model": "res.users",
                    "method": "reload_mx_group",
                    "args": [allowed_company_ids],
                    "kwargs": {}
                },
            })
        },

    });
    return CTQSwitchCompanyMenu;
});
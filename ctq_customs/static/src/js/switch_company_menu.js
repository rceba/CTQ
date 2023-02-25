odoo.define('ctq_customs.SwitchCompanyMenu', function(require) {
"use strict";

    const { SwitchCompanyMenu } = require("@web/webclient/switch_company_menu/switch_company_menu");
    const { session } =  require("@web/session");
    const rpc  = require('web.rpc');
    const { patch } = require('web.utils');

     //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------

        function _onSwitchCompanyClick(companyID) {
            var self = this;
            var res =  rpc.query({
                route: '/web/dataset/call_kw/res.users/reload_mx_group',
                params: {
                    "model": "res.users",
                    "method": "reload_mx_group",
                    "args": [companyID],
                    "kwargs": {companyID}
                },
            })
            return res
        }
    patch(SwitchCompanyMenu.prototype, 'ctq_customs.SwitchCompanyMenu', {

        logIntoCompany(companyId) {             
            if (companyId){
                _onSwitchCompanyClick(companyId);
            }
            this._super(...arguments);         
        }
    });
});
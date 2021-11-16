odoo.define('ctq_customs.field.html', function (require){
"use strict";
// require original module JS
var FieldHtml = require('web_editor.field.html');

// Extend widget
FieldHtml.include({
    /**
     * @override
     */
    _getWysiwygOptions: function () {
        var self = this;
        return Object.assign({}, this.nodeOptions, {
            recordInfo: {
                context: this.record.getContext(this.recordParams),
                res_model: this.model,
                res_id: this.res_id,
            },
            noAttachment: this.nodeOptions['no-attachment'],
            inIframe: !!this.nodeOptions.cssEdit,
            iframeCssAssets: this.nodeOptions.cssEdit,
            snippets: this.nodeOptions.snippets,

            tabsize: 0,
            height: 180,
            generateOptions: function (options) {
                var toolbar = options.toolbar || options.airPopover || {};
                var para = _.find(toolbar, function (item) {
                    return item[0] === 'para';
                });
                if (para && para[1] && para[1].indexOf('checklist') === -1) {
                    para[1].splice(2, 0, 'checklist');
                }
                options.codeview = true;
                var view = _.find(toolbar, function (item) {
                    return item[0] === 'view';
                });
                if (view) {
                    if (!view[1].includes('codeview')) {
                        view[1].splice(-1, 0, 'codeview');
                    }
                } else {
                    toolbar.splice(-1, 0, ['view', ['codeview']]);
                }
                if (self.model === "mail.compose.message" || self.model === "mailing.mailing") {
                    options.noVideos = true;
                }
                options.prettifyHtml = false;
                return options;
            },
        });
    },
});

});
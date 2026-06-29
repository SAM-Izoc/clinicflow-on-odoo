odoo.define('vet_hospital_merck.merck_button', function (require) {
    'use strict';

    const web = require('web.web_client');
    const Widget = require('web.Widget');

    const MerckButton = Widget.extend({
        template: 'merck_button',

        init: function (parent) {
            this._super.apply(this, arguments);
            this.parent = parent;
        },

        start: function () {
            this._super();
            this._setupMerckLinks();
        },

        _setupMerckLinks: function () {
            // Add smooth transitions to Merck links
            document.addEventListener('click', function (e) {
                if (e.target.classList.contains('merck-link')) {
                    e.preventDefault();
                    const url = e.target.href;
                    window.open(url, '_blank');
                }
            });
        },

        openMerckSearch: function (searchTerm) {
            const encodedTerm = encodeURIComponent(searchTerm);
            const url = `https://www.merckvetmanual.com/search?query=${encodedTerm}`;
            window.open(url, '_blank');
        }
    });

    return MerckButton;
});

(window.webpackJsonp=window.webpackJsonp||[]).push([[42],{720:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.r(__webpack_exports__);var _polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(1),_polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(10),_mixins_localize_mixin__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(71);class NotificationManager extends Object(_mixins_localize_mixin__WEBPACK_IMPORTED_MODULE_2__.a)(_polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_1__.a){static get template(){return _polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_0__.a`
      <style>
        paper-toast {
          z-index: 1;
        }
      </style>

      <ha-toast
        id="toast"
        no-cancel-on-outside-click="[[_cancelOnOutsideClick]]"
      ></ha-toast>
    `}static get properties(){return{hass:Object,_cancelOnOutsideClick:{type:Boolean,value:!1}}}ready(){super.ready();Promise.all([__webpack_require__.e(2),__webpack_require__.e(43)]).then(__webpack_require__.bind(null,370))}showDialog({message}){this.$.toast.show(message)}}customElements.define("notification-manager",NotificationManager)}}]);
//# sourceMappingURL=58a487488618d82072e4.chunk.js.map
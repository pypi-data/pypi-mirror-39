(window.webpackJsonp=window.webpackJsonp||[]).push([[59],{726:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.r(__webpack_exports__);var _polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(57),lit_html_directives_classMap__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(194),js_yaml__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(367),js_yaml__WEBPACK_IMPORTED_MODULE_2___default=__webpack_require__.n(js_yaml__WEBPACK_IMPORTED_MODULE_2__),_polymer_app_layout_app_header_layout_app_header_layout__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(180),_polymer_app_layout_app_header_app_header__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(172),_polymer_app_layout_app_toolbar_app_toolbar__WEBPACK_IMPORTED_MODULE_5__=__webpack_require__(108),_polymer_paper_button_paper_button__WEBPACK_IMPORTED_MODULE_6__=__webpack_require__(72),_polymer_paper_icon_button_paper_icon_button__WEBPACK_IMPORTED_MODULE_7__=__webpack_require__(99),_polymer_paper_spinner_paper_spinner__WEBPACK_IMPORTED_MODULE_8__=__webpack_require__(111),_mixins_lit_localize_mixin__WEBPACK_IMPORTED_MODULE_9__=__webpack_require__(154),_components_ha_icon__WEBPACK_IMPORTED_MODULE_10__=__webpack_require__(159);const TAB_INSERT="  ";class LovelaceFullConfigEditor extends Object(_mixins_lit_localize_mixin__WEBPACK_IMPORTED_MODULE_9__.a)(_polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__.a){static get properties(){return{lovelace:{},_saving:{},_changed:{}}}render(){return _polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__.c`
      ${this.renderStyle()}
      <app-header-layout>
        <app-header>
          <app-toolbar>
            <paper-icon-button
              icon="hass:close"
              @click="${this.closeEditor}"
            ></paper-icon-button>
            <div main-title>Edit Config</div>
            <paper-button @click="${this._handleSave}">Save</paper-button>
            <ha-icon class="save-button ${Object(lit_html_directives_classMap__WEBPACK_IMPORTED_MODULE_1__.a)({saved:!1===this._saving&&!this._changed})}" icon="hass:check">
          </app-toolbar>
        </app-header>
        <div class="content">
          <textarea
            autocomplete="off"
            autocorrect="off"
            autocapitalize="off"
            spellcheck="false"
            @input="${this._yamlChanged}"
          ></textarea>
        </div>
      </app-header-layout>
    `}firstUpdated(){const textArea=this.textArea;textArea.value=js_yaml__WEBPACK_IMPORTED_MODULE_2___default.a.safeDump(this.lovelace.config);textArea.addEventListener("keydown",e=>{if(9!==e.keyCode){return}e.preventDefault();const val=textArea.value,start=textArea.selectionStart,end=textArea.selectionEnd;textArea.value=val.substring(0,start)+TAB_INSERT+val.substring(end);textArea.selectionStart=textArea.selectionEnd=start+TAB_INSERT.length})}renderStyle(){if(!this._haStyle){this._haStyle=document.importNode(document.getElementById("ha-style").children[0].content,!0)}return _polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__.c`
      ${this._haStyle}
      <style>
        app-header-layout {
          height: 100vh;
        }
        paper-button {
          font-size: 16px;
        }
        app-toolbar {
          background-color: var(--dark-background-color, #455a64);
          color: var(--dark-text-color);
        }

        .content {
          height: calc(100vh - 68px);
        }

        textarea {
          box-sizing: border-box;
          height: 100%;
          width: 100%;
          resize: none;
          border: 0;
          outline: 0;
          font-size: 12pt;
          font-family: "Courier New", Courier, monospace;
          padding: 8px;
        }

        .save-button {
          opacity: 0;
          margin-left: -16px;
          margin-top: -4px;
          transition: opacity 1.5s;
        }

        .saved {
          opacity: 1;
        }
      </style>
    `}async _handleSave(){this._saving=!0;let value;try{value=js_yaml__WEBPACK_IMPORTED_MODULE_2___default.a.safeLoad(this.textArea.value)}catch(err){alert(`Unable to parse YAML: ${err}`);this._saving=!1;return}try{await this.lovelace.saveConfig(value)}catch(err){alert(`Unable to save YAML: ${err}`)}this._saving=!1;this._changed=!1}_yamlChanged(){if(this._changed){return}this._changed=!0}get textArea(){return this.shadowRoot.querySelector("textarea")}}customElements.define("hui-editor",LovelaceFullConfigEditor)}}]);
//# sourceMappingURL=eccd80b8b05e2e644645.chunk.js.map
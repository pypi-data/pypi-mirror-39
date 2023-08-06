(window.webpackJsonp=window.webpackJsonp||[]).push([[60],{722:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.r(__webpack_exports__);var _polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(57),js_yaml__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(365),js_yaml__WEBPACK_IMPORTED_MODULE_1___default=__webpack_require__.n(js_yaml__WEBPACK_IMPORTED_MODULE_1__),_polymer_app_layout_app_header_layout_app_header_layout__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(176),_polymer_app_layout_app_header_app_header__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(173),_polymer_app_layout_app_toolbar_app_toolbar__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(108),_polymer_paper_button_paper_button__WEBPACK_IMPORTED_MODULE_5__=__webpack_require__(72),_polymer_paper_icon_button_paper_icon_button__WEBPACK_IMPORTED_MODULE_6__=__webpack_require__(99),_mixins_lit_localize_mixin__WEBPACK_IMPORTED_MODULE_7__=__webpack_require__(164);const TAB_INSERT="  ";class LovelaceFullConfigEditor extends Object(_mixins_lit_localize_mixin__WEBPACK_IMPORTED_MODULE_7__.a)(_polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__.a){static get properties(){return{lovelace:{}}}render(){return _polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__.c`
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
          </app-toolbar>
        </app-header>
        <div class="content">
          <textarea
            autocomplete="off"
            autocorrect="off"
            autocapitalize="off"
            spellcheck="false"
          ></textarea>
        </div>
      </app-header-layout>
    `}firstUpdated(){const textArea=this.textArea;textArea.value=js_yaml__WEBPACK_IMPORTED_MODULE_1___default.a.safeDump(this.lovelace.config);textArea.addEventListener("keydown",e=>{if(9!==e.keyCode){return}e.preventDefault();const val=textArea.value,start=textArea.selectionStart,end=textArea.selectionEnd;textArea.value=val.substring(0,start)+TAB_INSERT+val.substring(end);textArea.selectionStart=textArea.selectionEnd=start+TAB_INSERT.length})}renderStyle(){if(!this._haStyle){this._haStyle=document.importNode(document.getElementById("ha-style").children[0].content,!0)}return _polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__.c`
      ${this._haStyle}
      <style>
        app-header-layout {
          height: 100vh;
        }

        .content {
          height: calc(100vh - 64px);
        }

        textarea {
          height: calc(100% - 16px);
          width: 100%;
          border: 0;
          outline: 0;
          font-size: 12pt;
          font-family: "Courier New", Courier, monospace;
          padding: 8px;
        }
      </style>
    `}_handleSave(){let value;try{value=js_yaml__WEBPACK_IMPORTED_MODULE_1___default.a.safeLoad(this.textArea.value)}catch(err){alert(`Unable to parse YAML: ${err}`);return}this.lovelace.saveConfig(value)}get textArea(){return this.shadowRoot.querySelector("textarea")}}customElements.define("hui-editor",LovelaceFullConfigEditor)}}]);
//# sourceMappingURL=574234da65003839f478.chunk.js.map
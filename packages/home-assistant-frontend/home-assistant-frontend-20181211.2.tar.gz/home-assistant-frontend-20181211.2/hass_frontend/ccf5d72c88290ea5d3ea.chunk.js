(window.webpackJsonp=window.webpackJsonp||[]).push([[68],{168:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.d(__webpack_exports__,"b",function(){return PaperDialogBehaviorImpl});__webpack_require__.d(__webpack_exports__,"a",function(){return PaperDialogBehavior});var _polymer_polymer_polymer_legacy_js__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(3),_polymer_iron_overlay_behavior_iron_overlay_behavior_js__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(73),_polymer_polymer_lib_legacy_polymer_dom_js__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(0);/**
@license
Copyright (c) 2015 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at
http://polymer.github.io/LICENSE.txt The complete set of authors may be found at
http://polymer.github.io/AUTHORS.txt The complete set of contributors may be
found at http://polymer.github.io/CONTRIBUTORS.txt Code distributed by Google as
part of the polymer project is also subject to an additional IP rights grant
found at http://polymer.github.io/PATENTS.txt
*/const PaperDialogBehaviorImpl={hostAttributes:{role:"dialog",tabindex:"-1"},properties:{modal:{type:Boolean,value:!1},__readied:{type:Boolean,value:!1}},observers:["_modalChanged(modal, __readied)"],listeners:{tap:"_onDialogClick"},ready:function(){this.__prevNoCancelOnOutsideClick=this.noCancelOnOutsideClick;this.__prevNoCancelOnEscKey=this.noCancelOnEscKey;this.__prevWithBackdrop=this.withBackdrop;this.__readied=!0},_modalChanged:function(modal,readied){if(!readied){return}if(modal){this.__prevNoCancelOnOutsideClick=this.noCancelOnOutsideClick;this.__prevNoCancelOnEscKey=this.noCancelOnEscKey;this.__prevWithBackdrop=this.withBackdrop;this.noCancelOnOutsideClick=!0;this.noCancelOnEscKey=!0;this.withBackdrop=!0}else{this.noCancelOnOutsideClick=this.noCancelOnOutsideClick&&this.__prevNoCancelOnOutsideClick;this.noCancelOnEscKey=this.noCancelOnEscKey&&this.__prevNoCancelOnEscKey;this.withBackdrop=this.withBackdrop&&this.__prevWithBackdrop}},_updateClosingReasonConfirmed:function(confirmed){this.closingReason=this.closingReason||{};this.closingReason.confirmed=confirmed},_onDialogClick:function(event){for(var path=Object(_polymer_polymer_lib_legacy_polymer_dom_js__WEBPACK_IMPORTED_MODULE_2__.b)(event).path,i=0,l=path.indexOf(this),target;i<l;i++){target=path[i];if(target.hasAttribute&&(target.hasAttribute("dialog-dismiss")||target.hasAttribute("dialog-confirm"))){this._updateClosingReasonConfirmed(target.hasAttribute("dialog-confirm"));this.close();event.stopPropagation();break}}}},PaperDialogBehavior=[_polymer_iron_overlay_behavior_iron_overlay_behavior_js__WEBPACK_IMPORTED_MODULE_1__.a,PaperDialogBehaviorImpl]},180:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_polymer_polymer_legacy_js__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(3),_polymer_iron_flex_layout_iron_flex_layout_js__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(33),_polymer_paper_styles_default_theme_js__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(39),_polymer_paper_styles_typography_js__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(50),_polymer_paper_styles_shadow_js__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(61);/**
@license
Copyright (c) 2015 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at
http://polymer.github.io/LICENSE.txt The complete set of authors may be found at
http://polymer.github.io/AUTHORS.txt The complete set of contributors may be
found at http://polymer.github.io/CONTRIBUTORS.txt Code distributed by Google as
part of the polymer project is also subject to an additional IP rights grant
found at http://polymer.github.io/PATENTS.txt
*/const $_documentContainer=document.createElement("template");$_documentContainer.setAttribute("style","display: none;");$_documentContainer.innerHTML=`<dom-module id="paper-dialog-shared-styles">
  <template>
    <style>
      :host {
        display: block;
        margin: 24px 40px;

        background: var(--paper-dialog-background-color, var(--primary-background-color));
        color: var(--paper-dialog-color, var(--primary-text-color));

        @apply --paper-font-body1;
        @apply --shadow-elevation-16dp;
        @apply --paper-dialog;
      }

      :host > ::slotted(*) {
        margin-top: 20px;
        padding: 0 24px;
      }

      :host > ::slotted(.no-padding) {
        padding: 0;
      }

      
      :host > ::slotted(*:first-child) {
        margin-top: 24px;
      }

      :host > ::slotted(*:last-child) {
        margin-bottom: 24px;
      }

      /* In 1.x, this selector was \`:host > ::content h2\`. In 2.x <slot> allows
      to select direct children only, which increases the weight of this
      selector, so we have to re-define first-child/last-child margins below. */
      :host > ::slotted(h2) {
        position: relative;
        margin: 0;

        @apply --paper-font-title;
        @apply --paper-dialog-title;
      }

      /* Apply mixin again, in case it sets margin-top. */
      :host > ::slotted(h2:first-child) {
        margin-top: 24px;
        @apply --paper-dialog-title;
      }

      /* Apply mixin again, in case it sets margin-bottom. */
      :host > ::slotted(h2:last-child) {
        margin-bottom: 24px;
        @apply --paper-dialog-title;
      }

      :host > ::slotted(.paper-dialog-buttons),
      :host > ::slotted(.buttons) {
        position: relative;
        padding: 8px 8px 8px 24px;
        margin: 0;

        color: var(--paper-dialog-button-color, var(--primary-color));

        @apply --layout-horizontal;
        @apply --layout-end-justified;
      }
    </style>
  </template>
</dom-module>`;document.head.appendChild($_documentContainer.content)},181:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_polymer_polymer_legacy_js__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(3),_polymer_paper_dialog_behavior_paper_dialog_shared_styles_js__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(180),_polymer_neon_animation_neon_animation_runner_behavior_js__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(107),_polymer_paper_dialog_behavior_paper_dialog_behavior_js__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(168),_polymer_polymer_lib_legacy_polymer_fn_js__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(4),_polymer_polymer_lib_utils_html_tag_js__WEBPACK_IMPORTED_MODULE_5__=__webpack_require__(1);/**
@license
Copyright (c) 2015 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at
http://polymer.github.io/LICENSE.txt The complete set of authors may be found at
http://polymer.github.io/AUTHORS.txt The complete set of contributors may be
found at http://polymer.github.io/CONTRIBUTORS.txt Code distributed by Google as
part of the polymer project is also subject to an additional IP rights grant
found at http://polymer.github.io/PATENTS.txt
*/Object(_polymer_polymer_lib_legacy_polymer_fn_js__WEBPACK_IMPORTED_MODULE_4__.a)({_template:_polymer_polymer_lib_utils_html_tag_js__WEBPACK_IMPORTED_MODULE_5__.a`
    <style include="paper-dialog-shared-styles"></style>
    <slot></slot>
`,is:"paper-dialog",behaviors:[_polymer_paper_dialog_behavior_paper_dialog_behavior_js__WEBPACK_IMPORTED_MODULE_3__.a,_polymer_neon_animation_neon_animation_runner_behavior_js__WEBPACK_IMPORTED_MODULE_2__.a],listeners:{"neon-animation-finish":"_onNeonAnimationFinish"},_renderOpened:function(){this.cancelAnimation();this.playAnimation("entry")},_renderClosed:function(){this.cancelAnimation();this.playAnimation("exit")},_onNeonAnimationFinish:function(){if(this.opened){this._finishRenderOpened()}else{this._finishRenderClosed()}}})},726:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.r(__webpack_exports__);__webpack_require__.d(__webpack_exports__,"HuiSaveConfig",function(){return HuiSaveConfig});var _polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(57),_polymer_paper_spinner_paper_spinner__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(111),_polymer_paper_dialog_paper_dialog__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(181),_polymer_paper_button_paper_button__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(72),_mixins_lit_localize_mixin__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(164);class HuiSaveConfig extends Object(_mixins_lit_localize_mixin__WEBPACK_IMPORTED_MODULE_4__.a)(_polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__.a){static get properties(){return{hass:{},_params:{},_saving:{}}}constructor(){super();this._saving=!1}async showDialog(params){this._params=params;await this.updateComplete;this._dialog.open()}get _dialog(){return this.shadowRoot.querySelector("paper-dialog")}render(){return _polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__.c`
      ${this.renderStyle()}
      <paper-dialog with-backdrop>
        <h2>${this.localize("ui.panel.lovelace.editor.save_config.header")}</h2>
        <paper-dialog-scrollable>
          <p>${this.localize("ui.panel.lovelace.editor.save_config.para")}</p>
          <p>
            ${this.localize("ui.panel.lovelace.editor.save_config.para_sure")}
          </p>
        </paper-dialog-scrollable>
        <div class="paper-dialog-buttons">
          <paper-button @click="${this._closeDialog}"
            >${this.localize("ui.panel.lovelace.editor.save_config.cancel")}</paper-button
          >
          <paper-button
            ?disabled="${this._saving}"
            @click="${this._saveConfig}"
          >
            <paper-spinner
              ?active="${this._saving}"
              alt="Saving"
            ></paper-spinner>
            ${this.localize("ui.panel.lovelace.editor.save_config.save")}</paper-button
          >
        </div>
      </paper-dialog>
    `}renderStyle(){return _polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__.c`
      <style>
        paper-dialog {
          width: 650px;
        }
        paper-spinner {
          display: none;
        }
        paper-spinner[active] {
          display: block;
        }
        paper-button paper-spinner {
          width: 14px;
          height: 14px;
          margin-right: 20px;
        }
      </style>
    `}_closeDialog(){this._dialog.close()}async _saveConfig(){if(!this.hass||!this._params){return}this._saving=!0;try{const lovelace=this._params.lovelace;await lovelace.saveConfig(lovelace.config);this._saving=!1;this._closeDialog()}catch(err){alert(`Saving failed: ${err.message}`);this._saving=!1}}}customElements.define("hui-dialog-save-config",HuiSaveConfig)}}]);
//# sourceMappingURL=ccf5d72c88290ea5d3ea.chunk.js.map
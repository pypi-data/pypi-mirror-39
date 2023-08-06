(window.webpackJsonp=window.webpackJsonp||[]).push([[66],{185:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_paper_icon_button_paper_icon_button__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(98),_polymer_paper_input_paper_input__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(78),_polymer_paper_item_paper_icon_item__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(194),_polymer_paper_item_paper_item_body__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(161),_polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(1),_polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_5__=__webpack_require__(10),_vaadin_vaadin_combo_box_vaadin_combo_box_light__WEBPACK_IMPORTED_MODULE_6__=__webpack_require__(212),_state_badge__WEBPACK_IMPORTED_MODULE_7__=__webpack_require__(163),_common_entity_compute_state_name__WEBPACK_IMPORTED_MODULE_8__=__webpack_require__(104),_mixins_localize_mixin__WEBPACK_IMPORTED_MODULE_9__=__webpack_require__(71),_mixins_events_mixin__WEBPACK_IMPORTED_MODULE_10__=__webpack_require__(48);class HaEntityPicker extends Object(_mixins_events_mixin__WEBPACK_IMPORTED_MODULE_10__.a)(Object(_mixins_localize_mixin__WEBPACK_IMPORTED_MODULE_9__.a)(_polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_5__.a)){static get template(){return _polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_4__.a`
      <style>
        paper-input > paper-icon-button {
          width: 24px;
          height: 24px;
          padding: 2px;
          color: var(--secondary-text-color);
        }
        [hidden] {
          display: none;
        }
      </style>
      <vaadin-combo-box-light
        items="[[_states]]"
        item-value-path="entity_id"
        item-label-path="entity_id"
        value="{{value}}"
        opened="{{opened}}"
        allow-custom-value="[[allowCustomEntity]]"
        on-change="_fireChanged"
      >
        <paper-input
          autofocus="[[autofocus]]"
          label="[[_computeLabel(label, localize)]]"
          class="input"
          autocapitalize="none"
          autocomplete="off"
          autocorrect="off"
          spellcheck="false"
          value="[[value]]"
          disabled="[[disabled]]"
        >
          <paper-icon-button
            slot="suffix"
            class="clear-button"
            icon="hass:close"
            no-ripple=""
            hidden$="[[!value]]"
            >Clear</paper-icon-button
          >
          <paper-icon-button
            slot="suffix"
            class="toggle-button"
            icon="[[_computeToggleIcon(opened)]]"
            hidden="[[!_states.length]]"
            >Toggle</paper-icon-button
          >
        </paper-input>
        <template>
          <style>
            paper-icon-item {
              margin: -10px;
              padding: 0;
            }
          </style>
          <paper-icon-item>
            <state-badge state-obj="[[item]]" slot="item-icon"></state-badge>
            <paper-item-body two-line="">
              <div>[[_computeStateName(item)]]</div>
              <div secondary="">[[item.entity_id]]</div>
            </paper-item-body>
          </paper-icon-item>
        </template>
      </vaadin-combo-box-light>
    `}static get properties(){return{allowCustomEntity:{type:Boolean,value:!1},hass:{type:Object,observer:"_hassChanged"},_hass:Object,_states:{type:Array,computed:"_computeStates(_hass, domainFilter, entityFilter)"},autofocus:Boolean,label:{type:String},value:{type:String,notify:!0},opened:{type:Boolean,value:!1,observer:"_openedChanged"},domainFilter:{type:String,value:null},entityFilter:{type:Function,value:null},disabled:Boolean}}_computeLabel(label,localize){return label===void 0?localize("ui.components.entity.entity-picker.entity"):label}_computeStates(hass,domainFilter,entityFilter){if(!hass)return[];let entityIds=Object.keys(hass.states);if(domainFilter){entityIds=entityIds.filter(eid=>eid.substr(0,eid.indexOf("."))===domainFilter)}let entities=entityIds.sort().map(key=>hass.states[key]);if(entityFilter){entities=entities.filter(entityFilter)}return entities}_computeStateName(state){return Object(_common_entity_compute_state_name__WEBPACK_IMPORTED_MODULE_8__.a)(state)}_openedChanged(newVal){if(!newVal){this._hass=this.hass}}_hassChanged(newVal){if(!this.opened){this._hass=newVal}}_computeToggleIcon(opened){return opened?"hass:menu-up":"hass:menu-down"}_fireChanged(ev){ev.stopPropagation();this.fire("change")}}customElements.define("ha-entity-picker",HaEntityPicker)},190:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_polymer_polymer_legacy_js__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(3),_polymer_iron_flex_layout_iron_flex_layout_js__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(33),_polymer_paper_styles_default_theme_js__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(39),_polymer_paper_dialog_behavior_paper_dialog_behavior_js__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(172),_polymer_polymer_lib_legacy_polymer_fn_js__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(4),_polymer_polymer_lib_utils_html_tag_js__WEBPACK_IMPORTED_MODULE_5__=__webpack_require__(1);/**
@license
Copyright (c) 2015 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at
http://polymer.github.io/LICENSE.txt The complete set of authors may be found at
http://polymer.github.io/AUTHORS.txt The complete set of contributors may be
found at http://polymer.github.io/CONTRIBUTORS.txt Code distributed by Google as
part of the polymer project is also subject to an additional IP rights grant
found at http://polymer.github.io/PATENTS.txt
*/Object(_polymer_polymer_lib_legacy_polymer_fn_js__WEBPACK_IMPORTED_MODULE_4__.a)({_template:_polymer_polymer_lib_utils_html_tag_js__WEBPACK_IMPORTED_MODULE_5__.a`
    <style>

      :host {
        display: block;
        @apply --layout-relative;
      }

      :host(.is-scrolled:not(:first-child))::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: var(--divider-color);
      }

      :host(.can-scroll:not(.scrolled-to-bottom):not(:last-child))::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: var(--divider-color);
      }

      .scrollable {
        padding: 0 24px;

        @apply --layout-scroll;
        @apply --paper-dialog-scrollable;
      }

      .fit {
        @apply --layout-fit;
      }
    </style>

    <div id="scrollable" class="scrollable" on-scroll="updateScrollState">
      <slot></slot>
    </div>
`,is:"paper-dialog-scrollable",properties:{dialogElement:{type:Object}},get scrollTarget(){return this.$.scrollable},ready:function(){this._ensureTarget();this.classList.add("no-padding")},attached:function(){this._ensureTarget();requestAnimationFrame(this.updateScrollState.bind(this))},updateScrollState:function(){this.toggleClass("is-scrolled",0<this.scrollTarget.scrollTop);this.toggleClass("can-scroll",this.scrollTarget.offsetHeight<this.scrollTarget.scrollHeight);this.toggleClass("scrolled-to-bottom",this.scrollTarget.scrollTop+this.scrollTarget.offsetHeight>=this.scrollTarget.scrollHeight)},_ensureTarget:function(){this.dialogElement=this.dialogElement||this.parentElement;if(this.dialogElement&&this.dialogElement.behaviors&&0<=this.dialogElement.behaviors.indexOf(_polymer_paper_dialog_behavior_paper_dialog_behavior_js__WEBPACK_IMPORTED_MODULE_3__.b)){this.dialogElement.sizingTarget=this.scrollTarget;this.scrollTarget.classList.remove("fit")}else if(this.dialogElement){this.scrollTarget.classList.add("fit")}}})},315:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.d(__webpack_exports__,"a",function(){return processEditorEntities});function processEditorEntities(entities){return entities.map(entityConf=>{if("string"===typeof entityConf){return{entity:entityConf}}return entityConf})}},316:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.d(__webpack_exports__,"a",function(){return configElementStyle});var _polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(57);const configElementStyle=_polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__.c`
  <style>
    paper-toggle-button {
      padding-top: 16px;
    }
    .side-by-side {
      display: flex;
    }
    .side-by-side > * {
      flex: 1;
      padding-right: 4px;
    }
  </style>
`},317:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(57),_polymer_paper_button_paper_button__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(72),_common_dom_fire_event__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(65),_mixins_lit_localize_mixin__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(164);class HuiThemeSelectionEditor extends Object(_mixins_lit_localize_mixin__WEBPACK_IMPORTED_MODULE_3__.a)(_polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__.a){static get properties(){return{hass:{},value:{}}}render(){const themes=["Backend-selected","default"].concat(Object.keys(this.hass.themes.themes).sort());return _polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__.c`
      ${this.renderStyle()}
      <paper-dropdown-menu
        label="Theme"
        dynamic-align
        @value-changed="${this._changed}"
      >
        <paper-listbox
          slot="dropdown-content"
          .selected="${this.value}"
          attr-for-selected="theme"
        >
          ${themes.map(theme=>{return _polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__.c`
                <paper-item theme="${theme}">${theme}</paper-item>
              `})}
        </paper-listbox>
      </paper-dropdown-menu>
    `}renderStyle(){return _polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__.c`
      <style>
        paper-dropdown-menu {
          width: 100%;
        }
      </style>
    `}_changed(ev){if(!this.hass||""===ev.target.value){return}this.value=ev.target.value;Object(_common_dom_fire_event__WEBPACK_IMPORTED_MODULE_2__.a)(this,"theme-changed")}}customElements.define("hui-theme-select-editor",HuiThemeSelectionEditor)},318:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(57),_common_dom_fire_event__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(65),_components_entity_ha_entity_picker__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(185);class HuiEntityEditor extends _polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__.a{static get properties(){return{hass:{},entities:{}}}render(){if(!this.entities){return _polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__.c``}return _polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__.c`
      ${this.renderStyle()}
      <h3>Entities</h3>
      <div class="entities">
        ${this.entities.map((entityConf,index)=>{return _polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__.c`
              <ha-entity-picker
                .hass="${this.hass}"
                .value="${entityConf.entity}"
                .index="${index}"
                @change="${this._valueChanged}"
                allow-custom-entity
              ></ha-entity-picker>
            `})}
        <ha-entity-picker
          .hass="${this.hass}"
          @change="${this._addEntity}"
        ></ha-entity-picker>
      </div>
    `}_addEntity(ev){const target=ev.target;if(""===target.value){return}const newConfigEntities=this.entities.concat({entity:target.value});target.value="";Object(_common_dom_fire_event__WEBPACK_IMPORTED_MODULE_1__.a)(this,"entities-changed",{entities:newConfigEntities})}_valueChanged(ev){const target=ev.target,newConfigEntities=this.entities.concat();if(""===target.value){newConfigEntities.splice(target.index,1)}else{newConfigEntities[target.index]=Object.assign({},newConfigEntities[target.index],{entity:target.value})}Object(_common_dom_fire_event__WEBPACK_IMPORTED_MODULE_1__.a)(this,"entities-changed",{entities:newConfigEntities})}renderStyle(){return _polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__.c`
      <style>
        .entities {
          padding-left: 20px;
        }
      </style>
    `}}customElements.define("hui-entity-editor",HuiEntityEditor)},369:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(57),_polymer_paper_spinner_paper_spinner__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(109),_polymer_paper_dialog_paper_dialog__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(180),_polymer_paper_button_paper_button__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(72),_common_dom_fire_event__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(65),_mixins_lit_localize_mixin__WEBPACK_IMPORTED_MODULE_5__=__webpack_require__(164),_data_lovelace__WEBPACK_IMPORTED_MODULE_6__=__webpack_require__(228);class HuiMigrateConfig extends Object(_mixins_lit_localize_mixin__WEBPACK_IMPORTED_MODULE_5__.a)(_polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__.a){static get properties(){return{_hass:{},_migrating:{}}}get _dialog(){return this.shadowRoot.querySelector("paper-dialog")}async showDialog(){if(null==this._dialog){await this.updateComplete}this._dialog.open()}render(){return _polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__.c`
      ${this.renderStyle()}
      <paper-dialog with-backdrop>
        <h2>${this.localize("ui.panel.lovelace.editor.migrate.header")}</h2>
        <paper-dialog-scrollable>
          <p>${this.localize("ui.panel.lovelace.editor.migrate.para_no_id")}</p>
          <p>
            ${this.localize("ui.panel.lovelace.editor.migrate.para_migrate")}
          </p>
        </paper-dialog-scrollable>
        <div class="paper-dialog-buttons">
          <paper-button @click="${this._closeDialog}"
            >${this.localize("ui.common.cancel")}</paper-button
          >
          <paper-button
            ?disabled="${this._migrating}"
            @click="${this._migrateConfig}"
          >
            <paper-spinner
              ?active="${this._migrating}"
              alt="Saving"
            ></paper-spinner>
            ${this.localize("ui.panel.lovelace.editor.migrate.migrate")}</paper-button
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
    `}_closeDialog(){this._dialog.close()}async _migrateConfig(){this._migrating=!0;try{await Object(_data_lovelace__WEBPACK_IMPORTED_MODULE_6__.g)(this.hass);this._closeDialog();this._migrating=!1;Object(_common_dom_fire_event__WEBPACK_IMPORTED_MODULE_4__.a)(this,"reload-lovelace")}catch(err){alert(`Migration failed: ${err.message}`);this._migrating=!1}}}customElements.define("hui-migrate-config",HuiMigrateConfig)},737:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.r(__webpack_exports__);var lit_element=__webpack_require__(57),paper_spinner=__webpack_require__(109),paper_tab=__webpack_require__(210),paper_tabs=__webpack_require__(239),paper_dialog=__webpack_require__(180),paper_icon_button=__webpack_require__(98),paper_item=__webpack_require__(125),paper_listbox=__webpack_require__(126),paper_menu_button=__webpack_require__(129),paper_button=__webpack_require__(72),paper_dialog_scrollable=__webpack_require__(190),hui_entity_editor=__webpack_require__(318),paper_input=__webpack_require__(78),lit_localize_mixin=__webpack_require__(164),fire_event=__webpack_require__(65),config_elements_style=__webpack_require__(316),hui_theme_select_editor=__webpack_require__(317);class hui_view_editor_HuiViewEditor extends Object(lit_localize_mixin.a)(lit_element.a){static get properties(){return{hass:{},_config:{}}}get _id(){if(!this._config){return""}return"id"in this._config?this._config.id:""}get _title(){if(!this._config){return""}return this._config.title||""}get _icon(){if(!this._config){return""}return this._config.icon||""}get _theme(){if(!this._config){return""}return this._config.theme||"Backend-selected"}set config(config){this._config=config}render(){if(!this.hass){return lit_element.c``}return lit_element.c`
      ${config_elements_style.a}
      <div class="card-config">
        <paper-input
          label="ID"
          value="${this._id}"
          .configValue="${"id"}"
          @value-changed="${this._valueChanged}"
        ></paper-input>
        <paper-input
          label="Title"
          value="${this._title}"
          .configValue="${"title"}"
          @value-changed="${this._valueChanged}"
        ></paper-input>
        <paper-input
          label="Icon"
          value="${this._icon}"
          .configValue="${"icon"}"
          @value-changed="${this._valueChanged}"
        ></paper-input>
        <hui-theme-select-editor
          .hass="${this.hass}"
          .value="${this._theme}"
          .configValue="${"theme"}"
          @theme-changed="${this._valueChanged}"
        ></hui-theme-select-editor>
      </div>
    `}_valueChanged(ev){if(!this._config||!this.hass){return}const target=ev.currentTarget;if(this[`_${target.configValue}`]===target.value){return}let newConfig;if(target.configValue){newConfig=Object.assign({},this._config,{[target.configValue]:target.value})}Object(fire_event.a)(this,"view-config-changed",{config:newConfig})}}customElements.define("hui-view-editor",hui_view_editor_HuiViewEditor);var lovelace=__webpack_require__(228),process_editor_entities=__webpack_require__(315);async function confDeleteView(hass,viewId,reloadLovelace){if(!confirm("Are you sure you want to delete this view?")){return}try{await Object(lovelace.d)(hass,viewId+"");reloadLovelace()}catch(err){alert(`Deleting failed: ${err.message}`)}}var common_navigate=__webpack_require__(119);function _objectWithoutPropertiesLoose(source,excluded){if(null==source)return{};var target={},sourceKeys=Object.keys(source),key,i;for(i=0;i<sourceKeys.length;i++){key=sourceKeys[i];if(0<=excluded.indexOf(key))continue;target[key]=source[key]}return target}class hui_edit_view_HuiEditView extends Object(lit_localize_mixin.a)(lit_element.a){static get properties(){return{hass:{},viewConfig:{},add:{},_config:{},_badges:{},_saving:{},_curTab:{}}}constructor(){super();this._saving=!1;this._curTabIndex=0}async showDialog(){if(null==this._dialog){await this.updateComplete}this._dialog.open()}updated(changedProperties){super.updated(changedProperties);if(!changedProperties.has("viewConfig")&&!changedProperties.has("add")){return}if(this.viewConfig&&(!changedProperties.get("viewConfig")||this.viewConfig.id!==changedProperties.get("viewConfig").id)){const _this$viewConfig=this.viewConfig,{badges}=_this$viewConfig,viewConfig=_objectWithoutPropertiesLoose(_this$viewConfig,["cards","badges"]);this._config=viewConfig;this._badges=badges?Object(process_editor_entities.a)(badges):[]}else if(changedProperties.has("add")){this._config={};this._badges=[]}this._resizeDialog()}get _dialog(){return this.shadowRoot.querySelector("paper-dialog")}render(){let content;switch(this._curTab){case"tab-settings":content=lit_element.c`
          <hui-view-editor
            .hass="${this.hass}"
            .config="${this._config}"
            @view-config-changed="${this._viewConfigChanged}"
          ></hui-view-editor>
        `;break;case"tab-badges":content=lit_element.c`
          <hui-entity-editor
            .hass="${this.hass}"
            .entities="${this._badges}"
            @entities-changed="${this._badgesChanged}"
          ></hui-entity-editor>
        `;break;case"tab-cards":content=lit_element.c`
          Cards
        `;break;}return lit_element.c`
      ${this.renderStyle()}
      <paper-dialog with-backdrop>
        <h2>${this.localize("ui.panel.lovelace.editor.edit_view.header")}</h2>
        <paper-tabs
          scrollable
          hide-scroll-buttons
          .selected="${this._curTabIndex}"
          @selected-item-changed="${this._handleTabSelected}"
        >
          <paper-tab id="tab-settings">Settings</paper-tab>
          <paper-tab id="tab-badges">Badges</paper-tab>
        </paper-tabs>
        <paper-dialog-scrollable> ${content} </paper-dialog-scrollable>
        <div class="paper-dialog-buttons">
          <paper-button @click="${this._closeDialog}"
            >${this.localize("ui.common.cancel")}</paper-button
          >
          <paper-button
            ?disabled="${!this._config||this._saving}"
            @click="${this._save}"
          >
            <paper-spinner
              ?active="${this._saving}"
              alt="Saving"
            ></paper-spinner>
            ${this.localize("ui.common.save")}</paper-button
          >
          <paper-menu-button no-animations>
            <paper-icon-button
              icon="hass:dots-vertical"
              slot="dropdown-trigger"
            ></paper-icon-button>
            <paper-listbox slot="dropdown-content">
              <paper-item @click="${this._delete}">Delete</paper-item>
            </paper-listbox>
          </paper-menu-button>
        </div>
      </paper-dialog>
    `}renderStyle(){return lit_element.c`
      <style>
        paper-dialog {
          width: 650px;
        }
        paper-tabs {
          --paper-tabs-selection-bar-color: var(--primary-color);
          text-transform: uppercase;
          border-bottom: 1px solid rgba(0, 0, 0, 0.1);
        }
        paper-button paper-spinner {
          width: 14px;
          height: 14px;
          margin-right: 20px;
        }
        paper-spinner {
          display: none;
        }
        paper-spinner[active] {
          display: block;
        }
        .hidden {
          display: none;
        }
        .error {
          color: #ef5350;
          border-bottom: 1px solid #ef5350;
        }
      </style>
    `}_save(){this._saving=!0;this._updateConfigInBackend()}_delete(){if(this._config.cards&&0<this._config.cards.length){alert("You can't delete a view that has card in them. Remove the cards first.");return}confDeleteView(this.hass,this._config.id,()=>{this._closeDialog();this.reloadLovelace();Object(common_navigate.a)(this,`/lovelace/0`)})}async _resizeDialog(){await this.updateComplete;Object(fire_event.a)(this._dialog,"iron-resize")}_closeDialog(){this._curTabIndex=0;this._config={};this._badges=[];this.viewConfig=void 0;this._dialog.close()}_handleTabSelected(ev){if(!ev.detail.value){return}this._curTab=ev.detail.value.id;this._resizeDialog()}async _updateConfigInBackend(){if(!this._config){return}if(!this._isConfigChanged()){this._closeDialog();this._saving=!1;return}if(this._badges){this._config.badges=this._badges.map(entityConf=>{return entityConf.entity})}try{if(this.add){this._config.cards=[];await Object(lovelace.b)(this.hass,this._config,"json")}else{await Object(lovelace.j)(this.hass,this.viewConfig.id+"",this._config,"json")}this.reloadLovelace();this._closeDialog();this._saving=!1}catch(err){alert(`Saving failed: ${err.message}`);this._saving=!1}}_viewConfigChanged(ev){if(ev.detail&&ev.detail.config){this._config=ev.detail.config}}_badgesChanged(ev){if(!this._badges||!this.hass||!ev.detail||!ev.detail.entities){return}this._badges=ev.detail.entities}_isConfigChanged(){if(!this.add){return!0}return JSON.stringify(this._config)!==JSON.stringify(this.viewConfig)}}customElements.define("hui-edit-view",hui_edit_view_HuiEditView);__webpack_require__(369);__webpack_require__.d(__webpack_exports__,"HuiDialogEditView",function(){return hui_dialog_edit_view_HuiDialogEditView});class hui_dialog_edit_view_HuiDialogEditView extends lit_element.a{static get properties(){return{hass:{},_params:{}}}async showDialog(params){this._params=params;await this.updateComplete;this.shadowRoot.children[0].showDialog()}render(){if(!this._params){return lit_element.c``}if(!this._params.add&&this._params.viewConfig&&!("id"in this._params.viewConfig)){return lit_element.c`
        <hui-migrate-config
          .hass="${this.hass}"
          @reload-lovelace="${this._params.reloadLovelace}"
        ></hui-migrate-config>
      `}return lit_element.c`
      <hui-edit-view
        .hass="${this.hass}"
        .viewConfig="${this._params.viewConfig}"
        .add="${this._params.add}"
        .reloadLovelace="${this._params.reloadLovelace}"
      >
      </hui-edit-view>
    `}}customElements.define("hui-dialog-edit-view",hui_dialog_edit_view_HuiDialogEditView)}}]);
//# sourceMappingURL=2ff395231795e7eab3b3.chunk.js.map
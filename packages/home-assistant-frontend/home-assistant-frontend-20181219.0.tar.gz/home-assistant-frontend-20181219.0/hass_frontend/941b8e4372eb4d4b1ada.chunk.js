(window.webpackJsonp=window.webpackJsonp||[]).push([[78],{164:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_paper_icon_button_paper_icon_button__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(99),_polymer_paper_input_paper_input__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(78),_polymer_paper_item_paper_icon_item__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(163),_polymer_paper_item_paper_item_body__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(156),_polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(1),_polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_5__=__webpack_require__(10),_vaadin_vaadin_combo_box_vaadin_combo_box_light__WEBPACK_IMPORTED_MODULE_6__=__webpack_require__(185),_state_badge__WEBPACK_IMPORTED_MODULE_7__=__webpack_require__(161),_common_entity_compute_state_name__WEBPACK_IMPORTED_MODULE_8__=__webpack_require__(105),_mixins_localize_mixin__WEBPACK_IMPORTED_MODULE_9__=__webpack_require__(71),_mixins_events_mixin__WEBPACK_IMPORTED_MODULE_10__=__webpack_require__(48);class HaEntityPicker extends Object(_mixins_events_mixin__WEBPACK_IMPORTED_MODULE_10__.a)(Object(_mixins_localize_mixin__WEBPACK_IMPORTED_MODULE_9__.a)(_polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_5__.a)){static get template(){return _polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_4__.a`
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
    `}static get properties(){return{allowCustomEntity:{type:Boolean,value:!1},hass:{type:Object,observer:"_hassChanged"},_hass:Object,_states:{type:Array,computed:"_computeStates(_hass, domainFilter, entityFilter)"},autofocus:Boolean,label:{type:String},value:{type:String,notify:!0},opened:{type:Boolean,value:!1,observer:"_openedChanged"},domainFilter:{type:String,value:null},entityFilter:{type:Function,value:null},disabled:Boolean}}_computeLabel(label,localize){return label===void 0?localize("ui.components.entity.entity-picker.entity"):label}_computeStates(hass,domainFilter,entityFilter){if(!hass)return[];let entityIds=Object.keys(hass.states);if(domainFilter){entityIds=entityIds.filter(eid=>eid.substr(0,eid.indexOf("."))===domainFilter)}let entities=entityIds.sort().map(key=>hass.states[key]);if(entityFilter){entities=entities.filter(entityFilter)}return entities}_computeStateName(state){return Object(_common_entity_compute_state_name__WEBPACK_IMPORTED_MODULE_8__.a)(state)}_openedChanged(newVal){if(!newVal){this._hass=this.hass}}_hassChanged(newVal){if(!this.opened){this._hass=newVal}}_computeToggleIcon(opened){return opened?"hass:menu-up":"hass:menu-down"}_fireChanged(ev){ev.stopPropagation();this.fire("change")}}customElements.define("ha-entity-picker",HaEntityPicker)},175:function(module,__webpack_exports__,__webpack_require__){"use strict";var index_es=__webpack_require__(178);__webpack_require__.d(__webpack_exports__,"a",function(){return struct});const struct=Object(index_es.a)({types:{"entity-id":function(value){if("string"!==typeof value){return"entity id should be a string"}if(!value.includes(".")){return"entity id should be in the format 'domain.entity'"}return!0},icon:function(value){if("string"!==typeof value){return"icon should be a string"}if(!value.includes(":")){return"icon should be in the format 'mdi:icon'"}return!0}}})},179:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.d(__webpack_exports__,"a",function(){return configElementStyle});var _polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(57);const configElementStyle=_polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__.c`
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
`},209:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(57),_polymer_paper_button_paper_button__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(72),_common_dom_fire_event__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(65),_mixins_lit_localize_mixin__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(154);class HuiThemeSelectionEditor extends Object(_mixins_lit_localize_mixin__WEBPACK_IMPORTED_MODULE_3__.a)(_polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__.a){static get properties(){return{hass:{},value:{}}}render(){const themes=["Backend-selected","default"].concat(Object.keys(this.hass.themes.themes).sort());return _polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__.c`
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
    `}_changed(ev){if(!this.hass||""===ev.target.value){return}this.value=ev.target.value;Object(_common_dom_fire_event__WEBPACK_IMPORTED_MODULE_2__.a)(this,"theme-changed")}}customElements.define("hui-theme-select-editor",HuiThemeSelectionEditor)},231:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(57),_common_dom_fire_event__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(65),_components_entity_ha_entity_picker__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(164);class HuiEntityEditor extends _polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__.a{static get properties(){return{hass:{},entities:{}}}render(){if(!this.entities){return _polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__.c``}return _polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__.c`
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
    `}}customElements.define("hui-entity-editor",HuiEntityEditor)},740:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.r(__webpack_exports__);__webpack_require__.d(__webpack_exports__,"HuiGaugeCardEditor",function(){return HuiGaugeCardEditor});var _polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(57),_polymer_paper_input_paper_input__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(78),_polymer_paper_toggle_button_paper_toggle_button__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(190),_common_structs_struct__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(175),_mixins_lit_localize_mixin__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(154),_common_dom_fire_event__WEBPACK_IMPORTED_MODULE_5__=__webpack_require__(65),_config_elements_style__WEBPACK_IMPORTED_MODULE_6__=__webpack_require__(179),_components_hui_theme_select_editor__WEBPACK_IMPORTED_MODULE_7__=__webpack_require__(209),_components_hui_entity_editor__WEBPACK_IMPORTED_MODULE_8__=__webpack_require__(231);const cardConfigStruct=Object(_common_structs_struct__WEBPACK_IMPORTED_MODULE_3__.a)({type:"string",title:"string?",entity:"string?",unit:"string?",min:"number?",max:"number?",severity:"object?",theme:"string?"});class HuiGaugeCardEditor extends Object(_mixins_lit_localize_mixin__WEBPACK_IMPORTED_MODULE_4__.a)(_polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__.a){setConfig(config){config=cardConfigStruct(config);this._useSeverity=config.severity?!0:!1;this._config=config}static get properties(){return{hass:{},_config:{}}}get _title(){return this._config.title||""}get _entity(){return this._config.entity||""}get _unit(){return this._config.unit||""}get _theme(){return this._config.theme||"default"}get _min(){return this._config.number||0}get _max(){return this._config.max||100}get _severity(){return this._config.severity||void 0}render(){if(!this.hass){return _polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__.c``}return _polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__.c`
      ${_config_elements_style__WEBPACK_IMPORTED_MODULE_6__.a} ${this.renderStyle()}
      <div class="card-config">
        <div class="side-by-side">
          <paper-input
            label="Title"
            .value="${this._title}"
            .configValue=${"title"}
            @value-changed="${this._valueChanged}"
          ></paper-input>
          <ha-entity-picker
            .hass="${this.hass}"
            .value="${this._entity}"
            .configValue=${"entity"}
            domain-filter="sensor"
            @change="${this._valueChanged}"
            allow-custom-entity
          ></ha-entity-picker>
        </div>
        <div class="side-by-side">
          <paper-input
            label="Unit"
            .value="${this._unit}"
            .configValue=${"unit"}
            @value-changed="${this._valueChanged}"
          ></paper-input>
          <hui-theme-select-editor
            .hass="${this.hass}"
            .value="${this._theme}"
            .configValue="${"theme"}"
            @theme-changed="${this._valueChanged}"
          ></hui-theme-select-editor>
        </div>
        <div class="side-by-side">
          <paper-input
            type="number"
            label="Minimum"
            .value="${this._min}"
            .configValue=${"min"}
            @value-changed="${this._valueChanged}"
          ></paper-input>
          <paper-input
            type="number"
            label="Maximum"
            .value="${this._max}"
            .configValue=${"max"}
            @value-changed="${this._valueChanged}"
          ></paper-input>
        </div>
        <div class="side-by-side">
          <paper-toggle-button
            ?checked="${!1!==this._useSeverity}"
            @change="${this._toggleSeverity}"
            >Define Severity?</paper-toggle-button
          >
          <div class="severity">
            <paper-input
              type="number"
              label="Green"
              .value="${this._severity?this._severity.green:0}"
              .configValue=${"green"}
              @value-changed="${this._severityChanged}"
            ></paper-input>
            <paper-input
              type="number"
              label="Yellow"
              .value="${this._severity?this._severity.yellow:0}"
              .configValue=${"yellow"}
              @value-changed="${this._severityChanged}"
            ></paper-input>
            <paper-input
              type="number"
              label="Red"
              .value="${this._severity?this._severity.red:0}"
              .configValue=${"red"}
              @value-changed="${this._severityChanged}"
            ></paper-input>
          </div>
        </div>
      </div>
    `}renderStyle(){return _polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__.c`
      <style>
        .severity {
          display: none;
          width: 100%;
          padding-left: 16px;
          flex-direction: row;
          flex-wrap: wrap;
        }
        .severity > * {
          flex: 1 0 30%;
          padding-right: 4px;
        }
        paper-toggle-button[checked] ~ .severity {
          display: flex;
        }
      </style>
    `}_toggleSeverity(ev){if(!this._config||!this.hass){return}const target=ev.target;this._config.severity=target.checked?{green:0,yellow:0,red:0}:void 0;Object(_common_dom_fire_event__WEBPACK_IMPORTED_MODULE_5__.a)(this,"config-changed",{config:this._config})}_severityChanged(ev){if(!this._config||!this.hass){return}const target=ev.target,severity=Object.assign({},this._config.severity,{[target.configValue]:+target.value});this._config=Object.assign({},this._config,{severity});Object(_common_dom_fire_event__WEBPACK_IMPORTED_MODULE_5__.a)(this,"config-changed",{config:this._config})}_valueChanged(ev){if(!this._config||!this.hass){return}const target=ev.target;if(target.configValue){if(""===target.value||"number"===target.type&&isNaN(+target.value)){delete this._config[target.configValue]}else{let value=target.value;if("number"===target.type){value=+value}this._config=Object.assign({},this._config,{[target.configValue]:value})}}Object(_common_dom_fire_event__WEBPACK_IMPORTED_MODULE_5__.a)(this,"config-changed",{config:this._config})}}customElements.define("hui-gauge-card-editor",HuiGaugeCardEditor)}}]);
//# sourceMappingURL=941b8e4372eb4d4b1ada.chunk.js.map
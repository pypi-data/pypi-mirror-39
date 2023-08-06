(window.webpackJsonp=window.webpackJsonp||[]).push([[62],{724:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.r(__webpack_exports__);__webpack_require__.d(__webpack_exports__,"HuiGlanceCardEditor",function(){return HuiGlanceCardEditor});var _polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(57),_common_structs_struct__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(434),_polymer_paper_dropdown_menu_paper_dropdown_menu__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(129),_polymer_paper_item_paper_item__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(126),_polymer_paper_listbox_paper_listbox__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(127),_polymer_paper_toggle_button_paper_toggle_button__WEBPACK_IMPORTED_MODULE_5__=__webpack_require__(187),_process_editor_entities__WEBPACK_IMPORTED_MODULE_6__=__webpack_require__(315),_mixins_lit_localize_mixin__WEBPACK_IMPORTED_MODULE_7__=__webpack_require__(164),_common_dom_fire_event__WEBPACK_IMPORTED_MODULE_8__=__webpack_require__(65),_config_elements_style__WEBPACK_IMPORTED_MODULE_9__=__webpack_require__(316),_components_entity_state_badge__WEBPACK_IMPORTED_MODULE_10__=__webpack_require__(163),_components_hui_theme_select_editor__WEBPACK_IMPORTED_MODULE_11__=__webpack_require__(317),_components_hui_entity_editor__WEBPACK_IMPORTED_MODULE_12__=__webpack_require__(318),_components_ha_card__WEBPACK_IMPORTED_MODULE_13__=__webpack_require__(167),_components_ha_icon__WEBPACK_IMPORTED_MODULE_14__=__webpack_require__(157);const entitiesConfigStruct=_common_structs_struct__WEBPACK_IMPORTED_MODULE_1__.a.union([{entity:"entity-id",name:"string?",icon:"icon?"},"entity-id"]),cardConfigStruct=Object(_common_structs_struct__WEBPACK_IMPORTED_MODULE_1__.a)({type:"string",title:"string|number?",theme:"string?",columns:"number?",show_name:"boolean?",show_state:"boolean?",entities:[entitiesConfigStruct]});class HuiGlanceCardEditor extends Object(_mixins_lit_localize_mixin__WEBPACK_IMPORTED_MODULE_7__.a)(_polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__.a){setConfig(config){config=cardConfigStruct(config);this._config=Object.assign({type:"glance"},config);this._configEntities=Object(_process_editor_entities__WEBPACK_IMPORTED_MODULE_6__.a)(config.entities)}static get properties(){return{hass:{},_config:{},_configEntities:{}}}get _title(){return this._config.title||""}get _theme(){return this._config.theme||"Backend-selected"}get _columns(){return this._config.columns?this._config.columns+"":""}render(){if(!this.hass){return _polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__.c``}return _polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__.c`
      ${_config_elements_style__WEBPACK_IMPORTED_MODULE_9__.a}
      <div class="card-config">
        <paper-input
          label="Title"
          value="${this._title}"
          .configValue="${"title"}"
          @value-changed="${this._valueChanged}"
        ></paper-input>
        <div class="side-by-side">
          <hui-theme-select-editor
            .hass="${this.hass}"
            .value="${this._theme}"
            .configValue="${"theme"}"
            @theme-changed="${this._valueChanged}"
          ></hui-theme-select-editor>
          <paper-input
            label="Columns"
            type="number"
            value="${this._columns}"
            .configValue="${"columns"}"
            @value-changed="${this._valueChanged}"
          ></paper-input>
        </div>
        <div class="side-by-side">
          <paper-toggle-button
            ?checked="${!1!==this._config.show_name}"
            .configValue="${"show_name"}"
            @change="${this._valueChanged}"
            >Show Entity's Name?</paper-toggle-button
          >
          <paper-toggle-button
            ?checked="${!1!==this._config.show_state}"
            .configValue="${"show_state"}"
            @change="${this._valueChanged}"
            >Show Entity's State Text?</paper-toggle-button
          >
        </div>
      </div>
      <hui-entity-editor
        .hass="${this.hass}"
        .entities="${this._configEntities}"
        @entities-changed="${this._valueChanged}"
      ></hui-entity-editor>
    `}_valueChanged(ev){if(!this._config||!this.hass){return}const target=ev.target;if(this[`_${target.configValue}`]===target.value){return}if(ev.detail&&ev.detail.entities){this._config.entities=ev.detail.entities;this._configEntities=Object(_process_editor_entities__WEBPACK_IMPORTED_MODULE_6__.a)(this._config.entities)}else if(target.configValue){let value=target.value;if("number"===target.type){value=+value}this._config=Object.assign({},this._config,{[target.configValue]:target.checked!==void 0?target.checked:value})}Object(_common_dom_fire_event__WEBPACK_IMPORTED_MODULE_8__.a)(this,"config-changed",{config:this._config})}}customElements.define("hui-glance-card-editor",HuiGlanceCardEditor)}}]);
//# sourceMappingURL=264144e91098b746dce1.chunk.js.map
(window.webpackJsonp=window.webpackJsonp||[]).push([[65],{369:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(57),_polymer_paper_spinner_paper_spinner__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(109),_polymer_paper_dialog_paper_dialog__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(180),_polymer_paper_button_paper_button__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(72),_common_dom_fire_event__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(65),_mixins_lit_localize_mixin__WEBPACK_IMPORTED_MODULE_5__=__webpack_require__(164),_data_lovelace__WEBPACK_IMPORTED_MODULE_6__=__webpack_require__(228);class HuiMigrateConfig extends Object(_mixins_lit_localize_mixin__WEBPACK_IMPORTED_MODULE_5__.a)(_polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__.a){static get properties(){return{_hass:{},_migrating:{}}}get _dialog(){return this.shadowRoot.querySelector("paper-dialog")}async showDialog(){if(null==this._dialog){await this.updateComplete}this._dialog.open()}render(){return _polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__.c`
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
    `}_closeDialog(){this._dialog.close()}async _migrateConfig(){this._migrating=!0;try{await Object(_data_lovelace__WEBPACK_IMPORTED_MODULE_6__.g)(this.hass);this._closeDialog();this._migrating=!1;Object(_common_dom_fire_event__WEBPACK_IMPORTED_MODULE_4__.a)(this,"reload-lovelace")}catch(err){alert(`Migration failed: ${err.message}`);this._migrating=!1}}}customElements.define("hui-migrate-config",HuiMigrateConfig)},736:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.r(__webpack_exports__);var lit_element=__webpack_require__(57),classMap=__webpack_require__(234),js_yaml=__webpack_require__(431),js_yaml_default=__webpack_require__.n(js_yaml),paper_spinner=__webpack_require__(109),paper_dialog=__webpack_require__(180),paper_button=__webpack_require__(72),paper_dialog_scrollable=__webpack_require__(190),lovelace=__webpack_require__(228),fire_event=__webpack_require__(65),lit_localize_mixin=__webpack_require__(164),paper_textarea=__webpack_require__(192);class hui_yaml_editor_HuiYAMLEditor extends lit_element.a{static get properties(){return{_yaml:{},cardId:{}}}set yaml(yaml){if(yaml===void 0){this._loading=!0;this._loadConfig()}else{this._yaml=yaml;if(this._loading){this._loading=!1}}}render(){return lit_element.c`
      ${this.renderStyle()}
      <paper-spinner
        ?active="${this._loading}"
        alt="Loading"
        class="center"
      ></paper-spinner>
      <paper-textarea
        max-rows="10"
        .value="${this._yaml}"
        @value-changed="${this._valueChanged}"
      ></paper-textarea>
    `}renderStyle(){return lit_element.c`
      <style>
        paper-textarea {
          --paper-input-container-shared-input-style_-_font-family: monospace;
        }
        .center {
          margin-left: auto;
          margin-right: auto;
        }
        paper-spinner {
          display: none;
        }
        paper-spinner[active] {
          display: block;
        }
      </style>
    `}async _loadConfig(){if(!this.hass||!this.cardId){return}this._yaml=await Object(lovelace.f)(this.hass,this.cardId);if(this._loading){this._loading=!1}}_valueChanged(ev){const target=ev.target;this._yaml=target.value;Object(fire_event.a)(this,"yaml-changed",{yaml:target.value})}}customElements.define("hui-yaml-editor",hui_yaml_editor_HuiYAMLEditor);const CUSTOM_TYPE_PREFIX="custom:";function getCardElementTag(type){return type.startsWith(CUSTOM_TYPE_PREFIX)?type.substr(CUSTOM_TYPE_PREFIX.length):`hui-${type}-card`}function s4(){return Math.floor(65536*(1+Math.random())).toString(16).substring(1)}function uid(){return s4()+s4()+s4()+s4()+s4()}const cards=[{name:"Alarm panel",type:"alarm-panel"},{name:"Conditional",type:"conditional"},{name:"Entities",type:"entities"},{name:"Entity Button",type:"entity-button"},{name:"Entity Filter",type:"entity-filter"},{name:"Gauge",type:"gauge"},{name:"Glance",type:"glance"},{name:"History Graph",type:"history-graph"},{name:"Horizontal Stack",type:"horizontal-graph"},{name:"iFrame",type:"iframe"},{name:"Light",type:"light"},{name:"Map",type:"map"},{name:"Markdown",type:"markdown"},{name:"Media Control",type:"media-control"},{name:"Picture",type:"picture"},{name:"Picture Elements",type:"picture-elements"},{name:"Picture Entity",type:"picture-entity"},{name:"Picture Glance",type:"picture-glance"},{name:"Plant Status",type:"plant-status"},{name:"Sensor",type:"sensor"},{name:"Shopping List",type:"shopping-list"},{name:"Thermostat",type:"thermostat"},{name:"Vertical Stack",type:"vertical-stack"},{name:"Weather Forecast",type:"weather-forecast"}];class hui_card_picker_HuiCardPicker extends Object(lit_localize_mixin.a)(lit_element.a){render(){return lit_element.c`
      ${this.renderStyle()}
      <h3>${this.localize("ui.panel.lovelace.editor.edit_card.pick_card")}</h3>
      <div class="cards-container">
        ${cards.map(card=>{return lit_element.c`
              <paper-button
                raised
                @click="${this._cardPicked}"
                .type="${card.type}"
                >${card.name}</paper-button
              >
            `})}
      </div>
    `}renderStyle(){return lit_element.c`
      <style>
        .cards-container {
          display: flex;
          flex-wrap: wrap;
          margin-bottom: 10px;
        }
        .cards-container paper-button {
          flex: 1 0 25%;
        }
      </style>
    `}_cardPicked(ev){const type=ev.currentTarget.type,tag=getCardElementTag(type),elClass=customElements.get(tag);let config={type,id:uid()};if(elClass&&elClass.getStubConfig){const cardConfig=elClass.getStubConfig(this.hass);config=Object.assign({},config,cardConfig)}Object(fire_event.a)(this,"card-picked",{config})}}customElements.define("hui-card-picker",hui_card_picker_HuiCardPicker);var create_card_element=__webpack_require__(321),create_error_card_config=__webpack_require__(263);class hui_card_preview_HuiCardPreview extends HTMLElement{set hass(value){this._hass=value;if(this._element){this._element.hass=value}}set error(error){const configValue=Object(create_error_card_config.a)(`${error.type}: ${error.message}`,void 0);this._createCard(configValue)}set config(configValue){if(!configValue){return}if(!this._element){this._createCard(configValue);return}const tag=getCardElementTag(configValue.type);if(tag.toUpperCase()===this._element.tagName){try{this._element.setConfig(configValue)}catch(err){this._createCard(Object(create_error_card_config.a)(err.message,configValue))}}else{this._createCard(configValue)}}_createCard(configValue){if(this._element){this.removeChild(this._element)}this._element=Object(create_card_element.a)(configValue);if(this._hass){this._element.hass=this._hass}this.appendChild(this._element)}}customElements.define("hui-card-preview",hui_card_preview_HuiCardPreview);const secretYamlType=new js_yaml_default.a.Type("!secret",{kind:"scalar",construct(data){data=data||"";return"!secret "+data}}),includeYamlType=new js_yaml_default.a.Type("!include",{kind:"scalar",construct(data){data=data||"";return"!include "+data}}),extYamlSchema=js_yaml_default.a.Schema.create([secretYamlType,includeYamlType]);class hui_edit_card_HuiEditCard extends Object(lit_localize_mixin.a)(lit_element.a){static get properties(){return{hass:{},cardConfig:{},viewId:{},_cardId:{},_configElement:{},_configValue:{},_configState:{},_errorMsg:{},_uiEditor:{},_saving:{},_loading:{}}}get _dialog(){return this.shadowRoot.querySelector("paper-dialog")}get _previewEl(){return this.shadowRoot.querySelector("hui-card-preview")}constructor(){super();this._saving=!1}async showDialog(){if(null==this._dialog){await this.updateComplete}this._dialog.open()}updated(changedProperties){super.updated(changedProperties);if(!changedProperties.has("cardConfig")&&!changedProperties.has("viewId")){return}this._configValue={format:"yaml",value:void 0};this._configState="OK";this._uiEditor=!0;this._errorMsg=void 0;this._configElement=void 0;if(this.cardConfig&&this.cardConfig.id+""!==this._cardId){this._loading=!0;this._cardId=this.cardConfig.id+"";this._loadConfigElement(this.cardConfig)}else{this._cardId=void 0}if(this.viewId&&!this.cardConfig){this._resizeDialog()}}render(){let content,preview;if(this._configElement!==void 0){if(this._uiEditor){content=lit_element.c`
          <div class="element-editor">${this._configElement}</div>
        `}else{content=lit_element.c`
          <hui-yaml-editor
            .hass="${this.hass}"
            .cardId="${this._cardId}"
            .yaml="${this._configValue.value}"
            @yaml-changed="${this._handleYamlChanged}"
          ></hui-yaml-editor>
        `}preview=lit_element.c`
        <hr />
        <hui-card-preview .hass="${this.hass}"> </hui-card-preview>
      `}else if(this.viewId&&!this.cardConfig){content=lit_element.c`
        <hui-card-picker
          .hass="${this.hass}"
          @card-picked="${this._handleCardPicked}"
        ></hui-card-picker>
      `}return lit_element.c`
      ${this.renderStyle()}
      <paper-dialog with-backdrop>
        <h2>${this.localize("ui.panel.lovelace.editor.edit_card.header")}</h2>
        <paper-spinner
          ?active="${this._loading}"
          alt="Loading"
          class="center margin-bot"
        ></paper-spinner>
        <paper-dialog-scrollable
          class="${Object(classMap.a)({hidden:this._loading})}"
        >
          ${this._errorMsg?lit_element.c`
                  <div class="error">${this._errorMsg}</div>
                `:""}
          ${content} ${preview}
        </paper-dialog-scrollable>
        ${!this._loading?lit_element.c`
                <div class="paper-dialog-buttons">
                  <paper-button
                    ?hidden="${!this._configValue||!this._configValue.value}"
                    ?disabled="${null===this._configElement||"OK"!==this._configState}"
                    @click="${this._toggleEditor}"
                    >${this.localize("ui.panel.lovelace.editor.edit_card.toggle_editor")}</paper-button
                  >
                  <paper-button @click="${this._closeDialog}"
                    >${this.localize("ui.common.cancel")}</paper-button
                  >
                  <paper-button
                    ?hidden="${!this._configValue||!this._configValue.value}"
                    ?disabled="${this._saving||"OK"!==this._configState}"
                    @click="${this._save}"
                  >
                    <paper-spinner
                      ?active="${this._saving}"
                      alt="Saving"
                    ></paper-spinner>
                    ${this.localize("ui.common.save")}</paper-button
                  >
                </div>
              `:""}
      </paper-dialog>
    `}renderStyle(){return lit_element.c`
      <style>
        paper-dialog {
          width: 650px;
        }
        .center {
          margin-left: auto;
          margin-right: auto;
        }
        .margin-bot {
          margin-bottom: 24px;
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
        .element-editor {
          margin-bottom: 8px;
        }
        .error {
          color: #ef5350;
          border-bottom: 1px solid #ef5350;
        }
        hr {
          color: #000;
          opacity: 0.12;
        }
        hui-card-preview {
          padding-top: 8px;
          margin-bottom: 4px;
          display: block;
        }
      </style>
    `}_save(){this._saving=!0;this._updateConfigInBackend()}_saveDone(){this._saving=!1}async _loadedDialog(){await this.updateComplete;this._loading=!1;this._resizeDialog()}async _resizeDialog(){await this.updateComplete;Object(fire_event.a)(this._dialog,"iron-resize")}_closeDialog(){this.cardConfig=void 0;this.viewId=void 0;Object(fire_event.a)(this,"cancel-edit-card");this._dialog.close()}async _updateConfigInBackend(){if(!this._isConfigValid()){alert("Your config is not valid, please fix your config before saving.");this._saveDone();return}if(!this._isConfigChanged()){this._closeDialog();this._saveDone();return}try{if(this.viewId){await Object(lovelace.a)(this.hass,this.viewId+"",this._configValue.value,this._configValue.format)}else{await Object(lovelace.i)(this.hass,this._cardId,this._configValue.value,this._configValue.format)}Object(fire_event.a)(this,"reload-lovelace");this._closeDialog();this._saveDone()}catch(err){alert(`Saving failed: ${err.message}`);this._saveDone()}}async _handleCardPicked(ev){const succes=await this._loadConfigElement(ev.detail.config);if(!succes){this._configValue={format:"yaml",value:js_yaml_default.a.safeDump(ev.detail.config)}}}_handleYamlChanged(ev){this._configValue={format:"yaml",value:ev.detail.yaml};try{const config=js_yaml_default.a.safeLoad(this._configValue.value,{schema:extYamlSchema});this._updatePreview(config);this._configState="OK"}catch(err){this._configState="YAML_ERROR";this._setPreviewError({type:"YAML Error",message:err})}}_handleUIConfigChanged(value){this._configValue={format:"json",value};this._updatePreview(value)}_updatePreview(config){if(!this._previewEl){return}this._previewEl.config=config;if(this._loading){this._loadedDialog()}else{this._resizeDialog()}}_setPreviewError(error){if(!this._previewEl){return}this._previewEl.error=error;this._resizeDialog()}async _toggleEditor(){if(this._uiEditor&&"json"===this._configValue.format){if(this._isConfigChanged()){this._configValue={format:"yaml",value:js_yaml_default.a.safeDump(this._configValue.value)}}else{this._configValue={format:"yaml",value:void 0}}this._uiEditor=!this._uiEditor}else if(this._configElement&&"yaml"===this._configValue.format){const yamlConfig=this._configValue.value,cardConfig=js_yaml_default.a.safeLoad(yamlConfig,{schema:extYamlSchema});this._uiEditor=!this._uiEditor;if(cardConfig.type!==this._cardType){const succes=await this._loadConfigElement(cardConfig);if(!succes){this._loadedDialog()}this._cardType=cardConfig.type}else{this._configValue={format:"json",value:cardConfig};this._configElement.setConfig(cardConfig)}}this._resizeDialog()}_isConfigValid(){if(!this._configValue||!this._configValue.value){return!1}if("OK"===this._configState){return!0}else{return!1}}_isConfigChanged(){if(this.viewId){return!0}const configValue="yaml"===this._configValue.format?js_yaml_default.a.safeDump(this._configValue.value):this._configValue.value;return JSON.stringify(configValue)!==JSON.stringify(this.cardConfig)}async _loadConfigElement(conf){if(!conf){return!1}this._errorMsg=void 0;this._loading=!0;this._configElement=void 0;const tag=getCardElementTag(conf.type),elClass=customElements.get(tag);let configElement;if(elClass&&elClass.getConfigElement){configElement=await elClass.getConfigElement()}else{this._uiEditor=!1;this._configElement=null;return!1}try{configElement.setConfig(conf)}catch(err){this._errorMsg=lit_element.c`
        Your config is not supported by the UI editor:<br /><b>${err.message}</b
        ><br />Falling back to YAML editor.
      `;this._uiEditor=!1;this._configElement=null;return!1}configElement.hass=this.hass;configElement.addEventListener("config-changed",ev=>this._handleUIConfigChanged(ev.detail.config));this._configValue={format:"json",value:conf};this._configElement=configElement;await this.updateComplete;this._updatePreview(conf);return!0}}customElements.define("hui-edit-card",hui_edit_card_HuiEditCard);__webpack_require__(369);__webpack_require__.d(__webpack_exports__,"HuiDialogEditCard",function(){return hui_dialog_edit_card_HuiDialogEditCard});class hui_dialog_edit_card_HuiDialogEditCard extends lit_element.a{static get properties(){return{hass:{},_params:{}}}async showDialog(params){this._params=params;await this.updateComplete;this.shadowRoot.children[0].showDialog()}render(){if(!this._params){return lit_element.c``}if(!this._params.add&&this._params.cardConfig&&!this._params.cardConfig.id||this._params.add&&!this._params.viewId){return lit_element.c`
        <hui-migrate-config
          .hass="${this.hass}"
          @reload-lovelace="${this._params.reloadLovelace}"
        ></hui-migrate-config>
      `}return lit_element.c`
      <hui-edit-card
        .hass="${this.hass}"
        .viewId="${this._params.viewId}"
        .cardConfig="${this._params.cardConfig}"
        @reload-lovelace="${this._params.reloadLovelace}"
        @cancel-edit-card="${this._cancel}"
      >
      </hui-edit-card>
    `}_cancel(){this._params={add:!1,reloadLovelace:()=>{}}}}customElements.define("hui-dialog-edit-card",hui_dialog_edit_card_HuiDialogEditCard)}}]);
//# sourceMappingURL=3712cd85230fdcb0aeae.chunk.js.map
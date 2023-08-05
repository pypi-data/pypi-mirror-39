(window.webpackJsonp=window.webpackJsonp||[]).push([[49],{153:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.d(__webpack_exports__,"a",function(){return DEFAULT_DOMAIN_ICON});__webpack_require__.d(__webpack_exports__,"f",function(){return DOMAINS_WITH_CARD});__webpack_require__.d(__webpack_exports__,"g",function(){return DOMAINS_WITH_MORE_INFO});__webpack_require__.d(__webpack_exports__,"c",function(){return DOMAINS_HIDE_MORE_INFO});__webpack_require__.d(__webpack_exports__,"d",function(){return DOMAINS_MORE_INFO_NO_HISTORY});__webpack_require__.d(__webpack_exports__,"h",function(){return STATES_OFF});__webpack_require__.d(__webpack_exports__,"e",function(){return DOMAINS_TOGGLE});__webpack_require__.d(__webpack_exports__,"i",function(){return UNIT_C});__webpack_require__.d(__webpack_exports__,"j",function(){return UNIT_F});__webpack_require__.d(__webpack_exports__,"b",function(){return DEFAULT_VIEW_ENTITY_ID});const DEFAULT_DOMAIN_ICON="hass:bookmark",DOMAINS_WITH_CARD=["climate","cover","configurator","input_select","input_number","input_text","lock","media_player","scene","script","timer","vacuum","water_heater","weblink"],DOMAINS_WITH_MORE_INFO=["alarm_control_panel","automation","camera","climate","configurator","cover","fan","group","history_graph","input_datetime","light","lock","media_player","script","sun","updater","vacuum","water_heater","weather"],DOMAINS_HIDE_MORE_INFO=["input_number","input_select","input_text","scene","weblink"],DOMAINS_MORE_INFO_NO_HISTORY=["camera","configurator","history_graph","scene"],STATES_OFF=["closed","locked","off"],DOMAINS_TOGGLE=new Set(["fan","input_boolean","light","switch"]),UNIT_C="\xB0C",UNIT_F="\xB0F",DEFAULT_VIEW_ENTITY_ID="group.default_view"},154:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.d(__webpack_exports__,"a",function(){return domainIcon});var _const__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(153);const fixedIcons={alert:"hass:alert",automation:"hass:playlist-play",calendar:"hass:calendar",camera:"hass:video",climate:"hass:thermostat",configurator:"hass:settings",conversation:"hass:text-to-speech",device_tracker:"hass:account",fan:"hass:fan",group:"hass:google-circles-communities",history_graph:"hass:chart-line",homeassistant:"hass:home-assistant",homekit:"hass:home-automation",image_processing:"hass:image-filter-frames",input_boolean:"hass:drawing",input_datetime:"hass:calendar-clock",input_number:"hass:ray-vertex",input_select:"hass:format-list-bulleted",input_text:"hass:textbox",light:"hass:lightbulb",mailbox:"hass:mailbox",notify:"hass:comment-alert",plant:"hass:flower",proximity:"hass:apple-safari",remote:"hass:remote",scene:"hass:google-pages",script:"hass:file-document",sensor:"hass:eye",simple_alarm:"hass:bell",sun:"hass:white-balance-sunny",switch:"hass:flash",timer:"hass:timer",updater:"hass:cloud-upload",vacuum:"hass:robot-vacuum",water_heater:"hass:thermometer",weblink:"hass:open-in-new"};function domainIcon(domain,state){if(domain in fixedIcons){return fixedIcons[domain]}switch(domain){case"alarm_control_panel":switch(state){case"armed_home":return"hass:bell-plus";case"armed_night":return"hass:bell-sleep";case"disarmed":return"hass:bell-outline";case"triggered":return"hass:bell-ring";default:return"hass:bell";}case"binary_sensor":return state&&"off"===state?"hass:radiobox-blank":"hass:checkbox-marked-circle";case"cover":return"closed"===state?"hass:window-closed":"hass:window-open";case"lock":return state&&"unlocked"===state?"hass:lock-open":"hass:lock";case"media_player":return state&&"off"!==state&&"idle"!==state?"hass:cast-connected":"hass:cast";case"zwave":switch(state){case"dead":return"hass:emoticon-dead";case"sleeping":return"hass:sleep";case"initializing":return"hass:timer-sand";default:return"hass:z-wave";}default:console.warn("Unable to find icon for domain "+domain+" ("+state+")");return _const__WEBPACK_IMPORTED_MODULE_0__.a;}}},155:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.d(__webpack_exports__,"a",function(){return computeDomain});function computeDomain(entityId){return entityId.substr(0,entityId.indexOf("."))}},157:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__(94);const IronIconClass=customElements.get("iron-icon");let loaded=!1;customElements.define("ha-icon",class extends IronIconClass{listen(...args){super.listen(...args);if(!loaded&&"mdi"===this._iconsetName){loaded=!0;__webpack_require__.e(47).then(__webpack_require__.bind(null,210))}}})},168:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_paper_styles_element_styles_paper_material_styles__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(82),_polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(1),_polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(10);class HaCard extends _polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_2__.a{static get template(){return _polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_1__.a`
      <style include="paper-material-styles">
        :host {
          @apply --paper-material-elevation-1;
          display: block;
          border-radius: 2px;
          transition: all 0.3s ease-out;
          background-color: var(--paper-card-background-color, white);
          color: var(--primary-text-color);
        }
        .header {
          @apply --paper-font-headline;
          @apply --paper-font-common-expensive-kerning;
          opacity: var(--dark-primary-opacity);
          padding: 24px 16px 16px;
        }
      </style>

      <template is="dom-if" if="[[header]]">
        <div class="header">[[header]]</div>
      </template>
      <slot></slot>
    `}static get properties(){return{header:String}}}customElements.define("ha-card",HaCard)},170:function(module,__webpack_exports__,__webpack_require__){"use strict";var fecha__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(167);__webpack_exports__.a=function(){try{new Date().toLocaleString("i")}catch(e){return"RangeError"===e.name}return!1}()?(dateObj,locales)=>dateObj.toLocaleString(locales,{year:"numeric",month:"long",day:"numeric",hour:"numeric",minute:"2-digit"}):dateObj=>fecha__WEBPACK_IMPORTED_MODULE_0__.a.format(dateObj,"haDateTime")},172:function(module,__webpack_exports__,__webpack_require__){"use strict";var common_const=__webpack_require__(153),compute_domain=__webpack_require__(155),domain_icon=__webpack_require__(154);const fixedDeviceClassIcons={humidity:"hass:water-percent",illuminance:"hass:brightness-5",temperature:"hass:thermometer",pressure:"hass:gauge"};function sensorIcon(state){const dclass=state.attributes.device_class;if(dclass&&dclass in fixedDeviceClassIcons){return fixedDeviceClassIcons[dclass]}if("battery"===dclass){const battery=+state.state;if(isNaN(battery)){return"hass:battery-unknown"}const batteryRound=10*Math.round(battery/10);if(100<=batteryRound){return"hass:battery"}if(0>=batteryRound){return"hass:battery-alert"}return`${"hass"}:battery-${batteryRound}`}const unit=state.attributes.unit_of_measurement;if(unit===common_const.i||unit===common_const.j){return"hass:thermometer"}return Object(domain_icon.a)("sensor")}__webpack_require__.d(__webpack_exports__,"a",function(){return stateIcon});const domainIcons={binary_sensor:function(state){const activated=state.state&&"off"===state.state;switch(state.attributes.device_class){case"battery":return activated?"hass:battery":"hass:battery-outline";case"cold":return activated?"hass:thermometer":"hass:snowflake";case"connectivity":return activated?"hass:server-network-off":"hass:server-network";case"door":return activated?"hass:door-closed":"hass:door-open";case"garage_door":return activated?"hass:garage":"hass:garage-open";case"gas":case"power":case"problem":case"safety":case"smoke":return activated?"hass:verified":"hass:alert";case"heat":return activated?"hass:thermometer":"hass:fire";case"light":return activated?"hass:brightness-5":"hass:brightness-7";case"lock":return activated?"hass:lock":"hass:lock-open";case"moisture":return activated?"hass:water-off":"hass:water";case"motion":return activated?"hass:walk":"hass:run";case"occupancy":return activated?"hass:home-outline":"hass:home";case"opening":return activated?"hass:square":"hass:square-outline";case"plug":return activated?"hass:power-plug-off":"hass:power-plug";case"presence":return activated?"hass:home-outline":"hass:home";case"sound":return activated?"hass:music-note-off":"hass:music-note";case"vibration":return activated?"hass:crop-portrait":"hass:vibrate";case"window":return activated?"hass:window-closed":"hass:window-open";default:return activated?"hass:radiobox-blank":"hass:checkbox-marked-circle";}},cover:function(state){const open="closed"!==state.state;switch(state.attributes.device_class){case"garage":return open?"hass:garage-open":"hass:garage";default:return Object(domain_icon.a)("cover",state.state);}},sensor:sensorIcon,input_datetime:function(state){if(!state.attributes.has_date){return"hass:clock"}if(!state.attributes.has_time){return"hass:calendar"}return Object(domain_icon.a)("input_datetime")}};function stateIcon(state){if(!state){return common_const.a}if(state.attributes.icon){return state.attributes.icon}const domain=Object(compute_domain.a)(state.entity_id);if(domain in domainIcons){return domainIcons[domain](state)}return Object(domain_icon.a)(domain,state.state)}},181:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(1),_polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(10),_resources_ha_style__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(99);class HaConfigSection extends _polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_1__.a{static get template(){return _polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_0__.a`
      <style include="iron-flex ha-style">
        .content {
          padding: 28px 20px 0;
          max-width: 1040px;
          margin: 0 auto;
        }

        .header {
          @apply --paper-font-display1;
          opacity: var(--dark-primary-opacity);
        }

        .together {
          margin-top: 32px;
        }

        .intro {
          @apply --paper-font-subhead;
          width: 100%;
          max-width: 400px;
          margin-right: 40px;
          opacity: var(--dark-primary-opacity);
        }

        .panel {
          margin-top: -24px;
        }

        .panel ::slotted(*) {
          margin-top: 24px;
          display: block;
        }

        .narrow.content {
          max-width: 640px;
        }
        .narrow .together {
          margin-top: 20px;
        }
        .narrow .header {
          @apply --paper-font-headline;
        }
        .narrow .intro {
          font-size: 14px;
          padding-bottom: 20px;
          margin-right: 0;
          max-width: 500px;
        }
      </style>
      <div class$="[[computeContentClasses(isWide)]]">
        <div class="header"><slot name="header"></slot></div>
        <div class$="[[computeClasses(isWide)]]">
          <div class="intro"><slot name="introduction"></slot></div>
          <div class="panel flex-auto"><slot></slot></div>
        </div>
      </div>
    `}static get properties(){return{hass:{type:Object},narrow:{type:Boolean},showMenu:{type:Boolean,value:!1},isWide:{type:Boolean,value:!1}}}computeContentClasses(isWide){var classes="content ";return isWide?classes:classes+"narrow"}computeClasses(isWide){return"together layout "+(isWide?"horizontal":"vertical narrow")}}customElements.define("ha-config-section",HaConfigSection)},205:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_app_layout_app_header_layout_app_header_layout__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(179),_polymer_app_layout_app_header_app_header__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(174),_polymer_app_layout_app_toolbar_app_toolbar__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(107),_polymer_paper_icon_button_paper_icon_button__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(98),_polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(1),_polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_5__=__webpack_require__(10);class HassSubpage extends _polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_5__.a{static get template(){return _polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_4__.a`
      <style include="ha-style"></style>
      <app-header-layout has-scrolling-region="">
        <app-header slot="header" fixed="">
          <app-toolbar>
            <paper-icon-button
              icon="hass:arrow-left"
              on-click="_backTapped"
            ></paper-icon-button>
            <div main-title="">[[header]]</div>
            <slot name="toolbar-icon"></slot>
          </app-toolbar>
        </app-header>

        <slot></slot>
      </app-header-layout>
    `}static get properties(){return{header:String}}_backTapped(){history.back()}}customElements.define("hass-subpage",HassSubpage)},206:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_paper_button_paper_button__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(72),_polymer_paper_spinner_paper_spinner__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(109),_polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(1),_polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(10);class HaProgressButton extends _polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_3__.a{static get template(){return _polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_2__.a`
      <style>
        .container {
          position: relative;
          display: inline-block;
        }

        paper-button {
          transition: all 1s;
        }

        .success paper-button {
          color: white;
          background-color: var(--google-green-500);
          transition: none;
        }

        .error paper-button {
          color: white;
          background-color: var(--google-red-500);
          transition: none;
        }

        paper-button[disabled] {
          color: #c8c8c8;
        }

        .progress {
          @apply --layout;
          @apply --layout-center-center;
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
        }
      </style>
      <div class="container" id="container">
        <paper-button
          id="button"
          disabled="[[computeDisabled(disabled, progress)]]"
          on-click="buttonTapped"
        >
          <slot></slot>
        </paper-button>
        <template is="dom-if" if="[[progress]]">
          <div class="progress"><paper-spinner active=""></paper-spinner></div>
        </template>
      </div>
    `}static get properties(){return{hass:{type:Object},progress:{type:Boolean,value:!1},disabled:{type:Boolean,value:!1}}}tempClass(className){var classList=this.$.container.classList;classList.add(className);setTimeout(()=>{classList.remove(className)},1e3)}ready(){super.ready();this.addEventListener("click",ev=>this.buttonTapped(ev))}buttonTapped(ev){if(this.progress)ev.stopPropagation()}actionSuccess(){this.tempClass("success")}actionError(){this.tempClass("error")}computeDisabled(disabled,progress){return disabled||progress}}customElements.define("ha-progress-button",HaProgressButton)},290:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(57),_ha_progress_button__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(206),_common_dom_fire_event__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(65);class HaCallApiButton extends _polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__.a{render(){return _polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__.c`
      <ha-progress-button
        .progress="${this.progress}"
        @click="${this._buttonTapped}"
        ?disabled="${this.disabled}"
        ><slot></slot
      ></ha-progress-button>
    `}constructor(){super();this.method="POST";this.data={};this.disabled=!1;this.progress=!1}static get properties(){return{hass:{},progress:Boolean,path:String,method:String,data:{},disabled:Boolean}}get progressButton(){return this.renderRoot.querySelector("ha-progress-button")}async _buttonTapped(){this.progress=!0;const eventData={method:this.method,path:this.path,data:this.data};try{const resp=await this.hass.callApi(this.method,this.path,this.data);this.progress=!1;this.progressButton.actionSuccess();eventData.success=!0;eventData.response=resp}catch(err){this.progress=!1;this.progressButton.actionError();eventData.success=!1;eventData.response=err}Object(_common_dom_fire_event__WEBPACK_IMPORTED_MODULE_2__.a)(this,"hass-api-called",eventData)}}customElements.define("ha-call-api-button",HaCallApiButton)},365:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(1),_polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(10),_ha_icon__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(157),_common_entity_state_icon__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(172);class HaStateIcon extends _polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_1__.a{static get template(){return _polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_0__.a`
      <ha-icon icon="[[computeIcon(stateObj)]]"></ha-icon>
    `}static get properties(){return{stateObj:{type:Object}}}computeIcon(stateObj){return Object(_common_entity_state_icon__WEBPACK_IMPORTED_MODULE_3__.a)(stateObj)}}customElements.define("ha-state-icon",HaStateIcon)},697:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.r(__webpack_exports__);var app_route=__webpack_require__(97),utils_async=__webpack_require__(8),debounce=__webpack_require__(14),html_tag=__webpack_require__(1),polymer_element=__webpack_require__(10),ha_config_section=__webpack_require__(181),paper_button=__webpack_require__(72),paper_card=__webpack_require__(152),paper_item_body=__webpack_require__(163),paper_toggle_button=__webpack_require__(185),ha_call_api_button=__webpack_require__(290),hass_subpage=__webpack_require__(205),ha_style=__webpack_require__(99),lit_element=__webpack_require__(57),paper_item=__webpack_require__(125),paper_spinner=__webpack_require__(109),ha_card=__webpack_require__(168),fire_event=__webpack_require__(65);const fetchWebhooks=hass=>hass.callWS({type:"webhook/list"}),createCloudhook=(hass,webhookId)=>hass.callWS({type:"cloud/cloudhook/create",webhook_id:webhookId}),deleteCloudhook=(hass,webhookId)=>hass.callWS({type:"cloud/cloudhook/delete",webhook_id:webhookId});function _objectWithoutPropertiesLoose(source,excluded){if(null==source)return{};var target={},sourceKeys=Object.keys(source),key,i;for(i=0;i<sourceKeys.length;i++){key=sourceKeys[i];if(0<=excluded.indexOf(key))continue;target[key]=source[key]}return target}function _toPropertyKey(arg){var key=_toPrimitive(arg,"string");return"symbol"===typeof key?key:key+""}function _toPrimitive(input,hint){if("object"!==typeof input||null===input)return input;var prim=input[Symbol.toPrimitive];if(prim!==void 0){var res=prim.call(input,hint||"default");if("object"!==typeof res)return res;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===hint?String:Number)(input)}class cloud_webhooks_CloudWebhooks extends lit_element.a{static get properties(){return{hass:{},cloudStatus:{},_cloudHooks:{},_localHooks:{},_progress:{}}}constructor(){super();this._progress=[]}connectedCallback(){super.connectedCallback();this._fetchData()}render(){return lit_element.c`
      ${this.renderStyle()}
      <ha-card header="Webhooks">
        <div class="body">
          Anything that is configured to be triggered by a webhook can be given
          a publicly accessible URL to allow you to send data back to Home
          Assistant from anywhere, without exposing your instance to the
          internet.
        </div>

        ${this._renderBody()}

        <div class="footer">
          <a href="https://www.nabucasa.com/config/webhooks" target="_blank">
            Learn more about creating webhook-powered automations.
          </a>
        </div>
      </ha-card>
    `}updated(changedProps){if(changedProps.has("cloudStatus")&&this.cloudStatus){this._cloudHooks=this.cloudStatus.prefs.cloudhooks||{}}}_renderBody(){if(!this.cloudStatus||!this._localHooks||!this._cloudHooks){return lit_element.c`
        <div class="loading">Loading…</div>
      `}return this._localHooks.map(entry=>lit_element.c`
        <div class="webhook" .entry="${entry}">
          <paper-item-body two-line>
            <div>
              ${entry.name}
              ${entry.domain===entry.name.toLowerCase()?"":` (${entry.domain})`}
            </div>
            <div secondary>${entry.webhook_id}</div>
          </paper-item-body>
          ${this._progress.includes(entry.webhook_id)?lit_element.c`
                  <div class="progress">
                    <paper-spinner active></paper-spinner>
                  </div>
                `:this._cloudHooks[entry.webhook_id]?lit_element.c`
                  <paper-button @click="${this._handleManageButton}"
                    >Manage</paper-button
                  >
                `:lit_element.c`
                  <paper-toggle-button
                    @click="${this._enableWebhook}"
                  ></paper-toggle-button>
                `}
        </div>
      `)}_showDialog(webhookId){const webhook=this._localHooks.find(ent=>ent.webhook_id===webhookId),cloudhook=this._cloudHooks[webhookId];Object(fire_event.a)(this,"manage-cloud-webhook",{webhook:webhook,cloudhook,disableHook:()=>this._disableWebhook(webhookId)})}_handleManageButton(ev){const entry=ev.currentTarget.parentElement.entry;this._showDialog(entry.webhook_id)}async _enableWebhook(ev){const entry=ev.currentTarget.parentElement.entry;this._progress=[...this._progress,entry.webhook_id];let updatedWebhook;try{updatedWebhook=await createCloudhook(this.hass,entry.webhook_id)}catch(err){alert(err.message);return}finally{this._progress=this._progress.filter(wid=>wid!==entry.webhook_id)}this._cloudHooks=Object.assign({},this._cloudHooks,{[entry.webhook_id]:updatedWebhook});if(0===this._progress.length){this._showDialog(entry.webhook_id)}}async _disableWebhook(webhookId){this._progress=[...this._progress,webhookId];try{await deleteCloudhook(this.hass,webhookId)}catch(err){alert(`Failed to disable webhook: ${err.message}`);return}finally{this._progress=this._progress.filter(wid=>wid!==webhookId)}const _ref=this._cloudHooks,newHooks=_objectWithoutPropertiesLoose(_ref,[webhookId].map(_toPropertyKey));this._cloudHooks=newHooks}async _fetchData(){this._localHooks=await fetchWebhooks(this.hass)}renderStyle(){return lit_element.c`
      <style>
        .body {
          padding: 0 16px 8px;
        }
        .loading {
          padding: 0 16px;
        }
        .webhook {
          display: flex;
          padding: 4px 16px;
        }
        .progress {
          margin-right: 16px;
          display: flex;
          flex-direction: column;
          justify-content: center;
        }
        paper-button {
          font-weight: 500;
          color: var(--primary-color);
        }
        .footer {
          padding: 16px;
        }
        .footer a {
          color: var(--primary-color);
        }
      </style>
    `}}customElements.define("cloud-webhooks",cloud_webhooks_CloudWebhooks);var format_date_time=__webpack_require__(170),events_mixin=__webpack_require__(48),localize_mixin=__webpack_require__(71);const fetchSubscriptionInfo=hass=>hass.callWS({type:"cloud/subscription"}),updatePref=(hass,prefs)=>hass.callWS(Object.assign({type:"cloud/update_prefs"},prefs));var repeat=__webpack_require__(298),paper_tooltip=__webpack_require__(241),ha_state_icon=__webpack_require__(365),compute_state_name=__webpack_require__(104),compute_domain=__webpack_require__(155);const generateFilter=(includeDomains,includeEntities,excludeDomains,excludeEntities)=>{const includeDomainsSet=new Set(includeDomains),includeEntitiesSet=new Set(includeEntities),excludeDomainsSet=new Set(excludeDomains),excludeEntitiesSet=new Set(excludeEntities),haveInclude=0<includeDomainsSet.size||0<includeEntitiesSet.size,haveExclude=0<excludeDomainsSet.size||0<excludeEntitiesSet.size;if(!haveInclude&&!haveExclude){return()=>!0}if(haveInclude&&!haveExclude){return entityId=>includeEntitiesSet.has(entityId)||includeDomainsSet.has(Object(compute_domain.a)(entityId))}if(!haveInclude&&haveExclude){return entityId=>!excludeEntitiesSet.has(entityId)&&!excludeDomainsSet.has(Object(compute_domain.a)(entityId))}if(includeDomainsSet.size){return entityId=>includeDomainsSet.has(Object(compute_domain.a)(entityId))?!excludeEntitiesSet.has(entityId):includeEntitiesSet.has(entityId)}if(excludeDomainsSet.size){return entityId=>excludeDomainsSet.has(Object(compute_domain.a)(entityId))?includeEntitiesSet.has(entityId):!excludeEntitiesSet.has(entityId)}return entityId=>includeEntitiesSet.has(entityId)};class cloud_exposed_entities_CloudExposedEntities extends lit_element.a{static get properties(){return{hass:{},filter:{},supportedDomains:{},_filterFunc:{}}}render(){if(!this._filterFunc){return lit_element.c``}const states=[];Object.keys(this.hass.states).forEach(entityId=>{if(this._filterFunc(entityId)){const stateObj=this.hass.states[entityId];states.push([Object(compute_state_name.a)(stateObj),stateObj])}});states.sort();return lit_element.c`
      ${this.renderStyle()}
      ${Object(repeat.a)(states,stateInfo=>stateInfo[1].entity_id,stateInfo=>lit_element.c`
            <span>
              <ha-state-icon
                .stateObj="${stateInfo[1]}"
                @click="${this._handleMoreInfo}"
              ></ha-state-icon>
              <paper-tooltip position="bottom">${stateInfo[0]}</paper-tooltip>
            </span>
          `)}
    `}updated(changedProperties){if(changedProperties.has("filter")&&changedProperties.get("filter")!==this.filter){const filter=this.filter,filterFunc=generateFilter(filter.include_domains,filter.include_entities,filter.exclude_domains,filter.exclude_entities),domains=new Set(this.supportedDomains);this._filterFunc=entityId=>{const domain=entityId.split(".")[0];return domains.has(domain)&&filterFunc(entityId)}}}_handleMoreInfo(ev){Object(fire_event.a)(this,"hass-more-info",{entityId:ev.currentTarget.stateObj.entity_id})}renderStyle(){return lit_element.c`
      <style>
        ha-state-icon {
          color: var(--primary-text-color);
          cursor: pointer;
        }
      </style>
    `}}customElements.define("cloud-exposed-entities",cloud_exposed_entities_CloudExposedEntities);class cloud_alexa_pref_CloudAlexaPref extends lit_element.a{static get properties(){return{hass:{},cloudStatus:{}}}render(){if(!this.cloudStatus){return lit_element.c``}const enabled=this.cloudStatus.prefs.alexa_enabled;return lit_element.c`
      ${this.renderStyle()}
      <paper-card heading="Alexa">
        <paper-toggle-button
          .checked="${enabled}"
          @change="${this._toggleChanged}"
        ></paper-toggle-button>
        <div class="card-content">
          With the Alexa integration for Home Assistant Cloud you'll be able to
          control all your Home Assistant devices via any Alexa-enabled device.
          <ul>
            <li>
              To activate, search in the Alexa app for the Home Assistant Smart
              Home skill.
            </li>
            <li>
              <a
                href="https://www.home-assistant.io/cloud/alexa/"
                target="_blank"
              >
                Config documentation
              </a>
            </li>
          </ul>
          <em
            >This integration requires an Alexa-enabled device like the Amazon
            Echo.</em
          >
          ${enabled?lit_element.c`
                  <p>Exposed entities:</p>
                  <cloud-exposed-entities
                    .hass="${this.hass}"
                    .filter="${this.cloudStatus.alexa_entities}"
                    .supportedDomains="${this.cloudStatus.alexa_domains}"
                  ></cloud-exposed-entities>
                `:""}
        </div>
      </paper-card>
    `}async _toggleChanged(ev){const toggle=ev.target;try{await updatePref(this.hass,{alexa_enabled:toggle.checked});Object(fire_event.a)(this,"ha-refresh-cloud-status")}catch(err){toggle.checked=!toggle.checked}}renderStyle(){return lit_element.c`
      <style>
        a {
          color: var(--primary-color);
        }
        paper-card > paper-toggle-button {
          position: absolute;
          right: 8px;
          top: 16px;
        }
      </style>
    `}}customElements.define("cloud-alexa-pref",cloud_alexa_pref_CloudAlexaPref);class cloud_google_pref_CloudGooglePref extends lit_element.a{static get properties(){return{hass:{},cloudStatus:{}}}render(){if(!this.cloudStatus){return lit_element.c``}const{google_enabled,google_allow_unlock}=this.cloudStatus.prefs;return lit_element.c`
      ${this.renderStyle()}
      <paper-card heading="Google Assistant">
        <paper-toggle-button
          id="google_enabled"
          .checked="${google_enabled}"
          @change="${this._toggleChanged}"
        ></paper-toggle-button>
        <div class="card-content">
          With the Google Assistant integration for Home Assistant Cloud you'll
          be able to control all your Home Assistant devices via any Google
          Assistant-enabled device.
          <ul>
            <li>
              <a
                href="https://assistant.google.com/services/a/uid/00000091fd5fb875"
                target="_blank"
              >
                Activate the Home Assistant skill for Google Assistant
              </a>
            </li>
            <li>
              <a
                href="https://www.home-assistant.io/cloud/google_assistant/"
                target="_blank"
              >
                Config documentation
              </a>
            </li>
          </ul>
          <em
            >This integration requires a Google Assistant-enabled device like
            the Google Home or Android phone.</em
          >
          ${google_enabled?lit_element.c`
                  <div class="unlock">
                    <div>Allow unlocking locks</div>
                    <paper-toggle-button
                      id="google_allow_unlock"
                      .checked="${google_allow_unlock}"
                      @change="${this._toggleChanged}"
                    ></paper-toggle-button>
                  </div>
                  <p>Exposed entities:</p>
                  <cloud-exposed-entities
                    .hass="${this.hass}"
                    .filter="${this.cloudStatus.google_entities}"
                    .supportedDomains="${this.cloudStatus.google_domains}"
                  ></cloud-exposed-entities>
                `:""}
        </div>
        <div class="card-actions">
          <ha-call-api-button
            .hass="${this.hass}"
            .disabled="${!google_enabled}"
            path="cloud/google_actions/sync"
            >Sync devices</ha-call-api-button
          >
        </div>
      </paper-card>
    `}async _toggleChanged(ev){const toggle=ev.target;try{await updatePref(this.hass,{[toggle.id]:toggle.checked});Object(fire_event.a)(this,"ha-refresh-cloud-status")}catch(err){toggle.checked=!toggle.checked}}renderStyle(){return lit_element.c`
      <style>
        a {
          color: var(--primary-color);
        }
        paper-card > paper-toggle-button {
          position: absolute;
          right: 8px;
          top: 16px;
        }
        ha-call-api-button {
          color: var(--primary-color);
          font-weight: 500;
        }
        .unlock {
          display: flex;
          flex-direction: row;
          padding-top: 16px;
        }
        .unlock > div {
          flex: 1;
        }
      </style>
    `}}customElements.define("cloud-google-pref",cloud_google_pref_CloudGooglePref);let registeredWebhookDialog=!1;class ha_config_cloud_account_HaConfigCloudAccount extends Object(events_mixin.a)(Object(localize_mixin.a)(polymer_element.a)){static get template(){return html_tag.a`
      <style include="iron-flex ha-style">
        [slot="introduction"] {
          margin: -1em 0;
        }
        [slot="introduction"] a {
          color: var(--primary-color);
        }
        .content {
          padding-bottom: 24px;
        }
        paper-card {
          display: block;
        }
        .account-row {
          display: flex;
          padding: 0 16px;
        }
        paper-button {
          align-self: center;
        }
        .soon {
          font-style: italic;
          margin-top: 24px;
          text-align: center;
        }
        .nowrap {
          white-space: nowrap;
        }
        .wrap {
          white-space: normal;
        }
        .status {
          text-transform: capitalize;
          padding: 16px;
        }
        paper-button {
          color: var(--primary-color);
          font-weight: 500;
        }
      </style>
      <hass-subpage header="Home Assistant Cloud">
        <div class="content">
          <ha-config-section is-wide="[[isWide]]">
            <span slot="header">Home Assistant Cloud</span>
            <div slot="introduction">
              <p>
                Thank you for being part of Home Assistant Cloud. It's because
                of people like you that we are able to make a great home
                automation experience for everyone. Thank you!
              </p>
            </div>

            <paper-card heading="Nabu Casa Account">
              <div class="account-row">
                <paper-item-body two-line="">
                  [[cloudStatus.email]]
                  <div secondary="" class="wrap">
                    [[_formatSubscription(_subscription)]]
                  </div>
                </paper-item-body>
              </div>

              <div class="account-row">
                <paper-item-body> Cloud connection status </paper-item-body>
                <div class="status">[[cloudStatus.cloud]]</div>
              </div>

              <div class="card-actions">
                <a href="https://account.nabucasa.com" target="_blank"
                  ><paper-button>Manage Account</paper-button></a
                >
                <paper-button style="float: right" on-click="handleLogout"
                  >Sign out</paper-button
                >
              </div>
            </paper-card>
          </ha-config-section>

          <ha-config-section is-wide="[[isWide]]">
            <span slot="header">Integrations</span>
            <div slot="introduction">
              <p>
                Integrations for Home Assistant Cloud allow you to connect with
                services in the cloud without having to expose your Home
                Assistant instance publicly on the internet.
              </p>
              <p>
                Check the website for
                <a href="https://www.nabucasa.com" target="_blank"
                  >all available features</a
                >.
              </p>
            </div>

            <cloud-alexa-pref
              hass="[[hass]]"
              cloud-status="[[cloudStatus]]"
            ></cloud-alexa-pref>

            <cloud-google-pref
              hass="[[hass]]"
              cloud-status="[[cloudStatus]]"
            ></cloud-google-pref>

            <cloud-webhooks
              hass="[[hass]]"
              cloud-status="[[cloudStatus]]"
            ></cloud-webhooks>
          </ha-config-section>
        </div>
      </hass-subpage>
    `}static get properties(){return{hass:Object,isWide:Boolean,cloudStatus:Object,_subscription:{type:Object,value:null}}}ready(){super.ready();this._fetchSubscriptionInfo()}connectedCallback(){super.connectedCallback();if(!registeredWebhookDialog){registeredWebhookDialog=!0;Object(fire_event.a)(this,"register-dialog",{dialogShowEvent:"manage-cloud-webhook",dialogTag:"cloud-webhook-manage-dialog",dialogImport:()=>Promise.all([__webpack_require__.e(2),__webpack_require__.e(65)]).then(__webpack_require__.bind(null,731))})}}async _fetchSubscriptionInfo(){this._subscription=await fetchSubscriptionInfo(this.hass);if(this._subscription.provider&&this.cloudStatus&&"connected"!==this.cloudStatus.cloud){this.fire("ha-refresh-cloud-status")}}handleLogout(){this.hass.callApi("post","cloud/logout").then(()=>this.fire("ha-refresh-cloud-status"))}_formatSubscription(subInfo){if(null===subInfo){return"Fetching subscription\u2026"}let description=subInfo.human_description;if(subInfo.plan_renewal_date){description=description.replace("{periodEnd}",Object(format_date_time.a)(new Date(1e3*subInfo.plan_renewal_date),this.hass.language))}return description}}customElements.define("ha-config-cloud-account",ha_config_cloud_account_HaConfigCloudAccount);var paper_input=__webpack_require__(78),ha_progress_button=__webpack_require__(206);class ha_config_cloud_forgot_password_HaConfigCloudForgotPassword extends Object(events_mixin.a)(polymer_element.a){static get template(){return html_tag.a`
      <style include="iron-flex ha-style">
        .content {
          padding-bottom: 24px;
        }

        paper-card {
          display: block;
          max-width: 600px;
          margin: 0 auto;
          margin-top: 24px;
        }
        h1 {
          @apply --paper-font-headline;
          margin: 0;
        }
        .error {
          color: var(--google-red-500);
        }
        .card-actions {
          display: flex;
          justify-content: space-between;
          align-items: center;
        }
        .card-actions a {
          color: var(--primary-text-color);
        }
        [hidden] {
          display: none;
        }
      </style>
      <hass-subpage header="Forgot Password">
        <div class="content">
          <paper-card>
            <div class="card-content">
              <h1>Forgot your password?</h1>
              <p>
                Enter your email address and we will send you a link to reset
                your password.
              </p>
              <div class="error" hidden$="[[!_error]]">[[_error]]</div>
              <paper-input
                autofocus=""
                id="email"
                label="E-mail"
                value="{{email}}"
                type="email"
                on-keydown="_keyDown"
                error-message="Invalid email"
              ></paper-input>
            </div>
            <div class="card-actions">
              <ha-progress-button
                on-click="_handleEmailPasswordReset"
                progress="[[_requestInProgress]]"
                >Send reset email</ha-progress-button
              >
            </div>
          </paper-card>
        </div>
      </hass-subpage>
    `}static get properties(){return{hass:Object,email:{type:String,notify:!0,observer:"_emailChanged"},_requestInProgress:{type:Boolean,value:!1},_error:{type:String,value:""}}}_emailChanged(){this._error="";this.$.email.invalid=!1}_keyDown(ev){if(13===ev.keyCode){this._handleEmailPasswordReset();ev.preventDefault()}}_handleEmailPasswordReset(){if(!this.email||!this.email.includes("@")){this.$.email.invalid=!0}if(this.$.email.invalid)return;this._requestInProgress=!0;this.hass.callApi("post","cloud/forgot_password",{email:this.email}).then(()=>{this._requestInProgress=!1;this.fire("cloud-done",{flashMessage:"Check your email for instructions on how to reset your password."})},err=>this.setProperties({_requestInProgress:!1,_error:err&&err.body&&err.body.message?err.body.message:"Unknown error"}))}}customElements.define("ha-config-cloud-forgot-password",ha_config_cloud_forgot_password_HaConfigCloudForgotPassword);var paper_icon_button=__webpack_require__(98),paper_ripple=__webpack_require__(75),navigate_mixin=__webpack_require__(95);class ha_config_cloud_login_HaConfigCloudLogin extends Object(navigate_mixin.a)(Object(events_mixin.a)(polymer_element.a)){static get template(){return html_tag.a`
      <style include="iron-flex ha-style">
        .content {
          padding-bottom: 24px;
        }
        [slot="introduction"] {
          margin: -1em 0;
        }
        [slot="introduction"] a {
          color: var(--primary-color);
        }
        paper-card {
          display: block;
        }
        paper-item {
          cursor: pointer;
        }
        paper-card:last-child {
          margin-top: 24px;
        }
        h1 {
          @apply --paper-font-headline;
          margin: 0;
        }
        .error {
          color: var(--google-red-500);
        }
        .card-actions {
          display: flex;
          justify-content: space-between;
          align-items: center;
        }
        [hidden] {
          display: none;
        }
        .flash-msg {
          padding-right: 44px;
        }
        .flash-msg paper-icon-button {
          position: absolute;
          top: 8px;
          right: 8px;
          color: var(--secondary-text-color);
        }
      </style>
      <hass-subpage header="Cloud Login">
        <div class="content">
          <ha-config-section is-wide="[[isWide]]">
            <span slot="header">Home Assistant Cloud</span>
            <div slot="introduction">
              <p>
                Home Assistant Cloud connects your local instance securely to
                cloud-only services Amazon Alexa and Google Assistant.
              </p>
              <p>
                This service is run by our partner
                <a href="https://www.nabucasa.com" target="_blank"
                  >Nabu&nbsp;Casa,&nbsp;Inc</a
                >, a company founded by the founders of Home Assistant and
                Hass.io.
              </p>
              <p>
                Home Assistant Cloud is a subscription service with a free one
                month trial. No payment information necessary.
              </p>
              <p>
                <a href="https://www.nabucasa.com" target="_blank"
                  >Learn more about Home Assistant Cloud</a
                >
              </p>
            </div>

            <paper-card hidden$="[[!flashMessage]]">
              <div class="card-content flash-msg">
                [[flashMessage]]
                <paper-icon-button icon="hass:close" on-click="_dismissFlash"
                  >Dismiss</paper-icon-button
                >
                <paper-ripple id="flashRipple" noink=""></paper-ripple>
              </div>
            </paper-card>

            <paper-card>
              <div class="card-content">
                <h1>Sign In</h1>
                <div class="error" hidden$="[[!_error]]">[[_error]]</div>
                <paper-input
                  label="Email"
                  id="email"
                  type="email"
                  value="{{email}}"
                  on-keydown="_keyDown"
                  error-message="Invalid email"
                ></paper-input>
                <paper-input
                  id="password"
                  label="Password"
                  value="{{_password}}"
                  type="password"
                  on-keydown="_keyDown"
                  error-message="Passwords are at least 8 characters"
                ></paper-input>
              </div>
              <div class="card-actions">
                <ha-progress-button
                  on-click="_handleLogin"
                  progress="[[_requestInProgress]]"
                  >Sign in</ha-progress-button
                >
                <button
                  class="link"
                  hidden="[[_requestInProgress]]"
                  on-click="_handleForgotPassword"
                >
                  forgot password?
                </button>
              </div>
            </paper-card>

            <paper-card>
              <paper-item on-click="_handleRegister">
                <paper-item-body two-line="">
                  Start your free 1 month trial
                  <div secondary="">No payment information necessary</div>
                </paper-item-body>
                <iron-icon icon="hass:chevron-right"></iron-icon>
              </paper-item>
            </paper-card>
          </ha-config-section>
        </div>
      </hass-subpage>
    `}static get properties(){return{hass:Object,isWide:Boolean,email:{type:String,notify:!0},_password:{type:String,value:""},_requestInProgress:{type:Boolean,value:!1},flashMessage:{type:String,notify:!0},_error:String}}static get observers(){return["_inputChanged(email, _password)"]}connectedCallback(){super.connectedCallback();if(this.flashMessage){requestAnimationFrame(()=>requestAnimationFrame(()=>this.$.flashRipple.simulatedRipple()))}}_inputChanged(){this.$.email.invalid=!1;this.$.password.invalid=!1;this._error=!1}_keyDown(ev){if(13===ev.keyCode){this._handleLogin();ev.preventDefault()}}_handleLogin(){let invalid=!1;if(!this.email||!this.email.includes("@")){this.$.email.invalid=!0;this.$.email.focus();invalid=!0}if(8>this._password.length){this.$.password.invalid=!0;if(!invalid){invalid=!0;this.$.password.focus()}}if(invalid)return;this._requestInProgress=!0;this.hass.callApi("post","cloud/login",{email:this.email,password:this._password}).then(()=>{this.fire("ha-refresh-cloud-status");this.setProperties({email:"",_password:""})},err=>{this._password="";const errCode=err&&err.body&&err.body.code;if("PasswordChangeRequired"===errCode){alert("You need to change your password before logging in.");this.navigate("/config/cloud/forgot-password");return}const props={_requestInProgress:!1,_error:err&&err.body&&err.body.message?err.body.message:"Unknown error"};if("UserNotConfirmed"===errCode){props._error="You need to confirm your email before logging in."}this.setProperties(props);this.$.email.focus()})}_handleRegister(){this.flashMessage="";this.navigate("/config/cloud/register")}_handleForgotPassword(){this.flashMessage="";this.navigate("/config/cloud/forgot-password")}_dismissFlash(){setTimeout(()=>{this.flashMessage=""},200)}}customElements.define("ha-config-cloud-login",ha_config_cloud_login_HaConfigCloudLogin);class ha_config_cloud_register_HaConfigCloudRegister extends Object(events_mixin.a)(polymer_element.a){static get template(){return html_tag.a`
    <style include="iron-flex ha-style">
      [slot=introduction] {
        margin: -1em 0;
      }
      [slot=introduction] a {
        color: var(--primary-color);
      }
      a {
        color: var(--primary-color);
      }
      paper-card {
        display: block;
      }
      paper-item {
        cursor: pointer;
      }
      paper-card:last-child {
        margin-top: 24px;
      }
      h1 {
        @apply --paper-font-headline;
        margin: 0;
      }
      .error {
        color: var(--google-red-500);
      }
      .card-actions {
        display: flex;
        justify-content: space-between;
        align-items: center;
      }
      [hidden] {
        display: none;
      }
    </style>
    <hass-subpage header="Register Account">
      <div class="content">
        <ha-config-section is-wide="[[isWide]]">
          <span slot="header">Start your free trial</span>
          <div slot="introduction">
            <p>
              Create an account to start your free one month trial with Home Assistant Cloud. No payment information necessary.
            </p>
            <p>
              The trial will give you access to all the benefits of Home Assistant Cloud, including:
            </p>
            <ul>
              <li>Integration with Google Assistant</li>
              <li>Integration with Amazon Alexa</li>
            </ul>
            <p>
              This service is run by our partner <a href='https://www.nabucasa.com' target='_blank'>Nabu&nbsp;Casa,&nbsp;Inc</a>, a company founded by the founders of Home Assistant and Hass.io.
            </p>

            <p>
              By registering an account you agree to the following terms and conditions.
              </p><ul>
                <li><a href="https://home-assistant.io/tos/" target="_blank">Terms and Conditions</a></li>
                <li><a href="https://home-assistant.io/privacy/" target="_blank">Privacy Policy</a></li>
              </ul>
            </p>
          </div>

          <paper-card>
            <div class="card-content">
              <div class="header">
                <h1>Create Account</h1>
                <div class="error" hidden$="[[!_error]]">[[_error]]</div>
              </div>
              <paper-input autofocus="" id="email" label="Email address" type="email" value="{{email}}" on-keydown="_keyDown" error-message="Invalid email"></paper-input>
              <paper-input id="password" label="Password" value="{{_password}}" type="password" on-keydown="_keyDown" error-message="Your password needs to be at least 8 characters"></paper-input>
            </div>
            <div class="card-actions">
              <ha-progress-button on-click="_handleRegister" progress="[[_requestInProgress]]">Start trial</ha-progress-button>
              <button class="link" hidden="[[_requestInProgress]]" on-click="_handleResendVerifyEmail">Resend confirmation email</button>
            </div>
          </paper-card>
        </ha-config-section>
      </div>
    </hass-subpage>
`}static get properties(){return{hass:Object,isWide:Boolean,email:{type:String,notify:!0},_requestInProgress:{type:Boolean,value:!1},_password:{type:String,value:""},_error:{type:String,value:""}}}static get observers(){return["_inputChanged(email, _password)"]}_inputChanged(){this._error="";this.$.email.invalid=!1;this.$.password.invalid=!1}_keyDown(ev){if(13===ev.keyCode){this._handleRegister();ev.preventDefault()}}_handleRegister(){let invalid=!1;if(!this.email||!this.email.includes("@")){this.$.email.invalid=!0;this.$.email.focus();invalid=!0}if(8>this._password.length){this.$.password.invalid=!0;if(!invalid){invalid=!0;this.$.password.focus()}}if(invalid)return;this._requestInProgress=!0;this.hass.callApi("post","cloud/register",{email:this.email,password:this._password}).then(()=>this._verificationEmailSent(),err=>{this._password="";this.setProperties({_requestInProgress:!1,_error:err&&err.body&&err.body.message?err.body.message:"Unknown error"})})}_handleResendVerifyEmail(){if(!this.email){this.$.email.invalid=!0;return}this.hass.callApi("post","cloud/resend_confirm",{email:this.email}).then(()=>this._verificationEmailSent(),err=>this.setProperties({_error:err&&err.body&&err.body.message?err.body.message:"Unknown error"}))}_verificationEmailSent(){this.setProperties({_requestInProgress:!1,_password:""});this.fire("cloud-done",{flashMessage:"Account created! Check your email for instructions on how to activate your account."})}}customElements.define("ha-config-cloud-register",ha_config_cloud_register_HaConfigCloudRegister);const LOGGED_IN_URLS=["/cloud/account"],NOT_LOGGED_IN_URLS=["/cloud/login","/cloud/register","/cloud/forgot-password"];class ha_config_cloud_HaConfigCloud extends Object(navigate_mixin.a)(polymer_element.a){static get template(){return html_tag.a`
      <app-route
        route="[[route]]"
        pattern="/cloud/:page"
        data="{{_routeData}}"
        tail="{{_routeTail}}"
      ></app-route>

      <template
        is="dom-if"
        if="[[_equals(_routeData.page, &quot;account&quot;)]]"
        restamp=""
      >
        <ha-config-cloud-account
          hass="[[hass]]"
          cloud-status="[[cloudStatus]]"
          is-wide="[[isWide]]"
        ></ha-config-cloud-account>
      </template>

      <template
        is="dom-if"
        if="[[_equals(_routeData.page, &quot;login&quot;)]]"
        restamp=""
      >
        <ha-config-cloud-login
          page-name="login"
          hass="[[hass]]"
          is-wide="[[isWide]]"
          email="{{_loginEmail}}"
          flash-message="{{_flashMessage}}"
        ></ha-config-cloud-login>
      </template>

      <template
        is="dom-if"
        if="[[_equals(_routeData.page, &quot;register&quot;)]]"
        restamp=""
      >
        <ha-config-cloud-register
          page-name="register"
          hass="[[hass]]"
          is-wide="[[isWide]]"
          email="{{_loginEmail}}"
        ></ha-config-cloud-register>
      </template>

      <template
        is="dom-if"
        if="[[_equals(_routeData.page, &quot;forgot-password&quot;)]]"
        restamp=""
      >
        <ha-config-cloud-forgot-password
          page-name="forgot-password"
          hass="[[hass]]"
          email="{{_loginEmail}}"
        ></ha-config-cloud-forgot-password>
      </template>
    `}static get properties(){return{hass:Object,isWide:Boolean,loadingAccount:{type:Boolean,value:!1},cloudStatus:{type:Object},_flashMessage:{type:String,value:""},route:Object,_routeData:Object,_routeTail:Object,_loginEmail:String}}static get observers(){return["_checkRoute(route, cloudStatus)"]}ready(){super.ready();this.addEventListener("cloud-done",ev=>{this._flashMessage=ev.detail.flashMessage;this.navigate("/config/cloud/login")})}_checkRoute(route){if(!route||"/cloud"!==route.path.substr(0,6))return;this._debouncer=debounce.a.debounce(this._debouncer,utils_async.d.after(0),()=>{if(!this.cloudStatus||!this.cloudStatus.logged_in&&!NOT_LOGGED_IN_URLS.includes(route.path)){this.navigate("/config/cloud/login",!0)}else if(this.cloudStatus.logged_in&&!LOGGED_IN_URLS.includes(route.path)){this.navigate("/config/cloud/account",!0)}})}_equals(a,b){return a===b}}customElements.define("ha-config-cloud",ha_config_cloud_HaConfigCloud)}}]);
//# sourceMappingURL=4af8e2548c40e2b6f4e4.chunk.js.map
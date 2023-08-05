(window.webpackJsonp=window.webpackJsonp||[]).push([[50],{151:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.d(__webpack_exports__,"a",function(){return computeStateDomain});var _compute_domain__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(155);function computeStateDomain(stateObj){return Object(_compute_domain__WEBPACK_IMPORTED_MODULE_0__.a)(stateObj.entity_id)}},153:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.d(__webpack_exports__,"a",function(){return DEFAULT_DOMAIN_ICON});__webpack_require__.d(__webpack_exports__,"f",function(){return DOMAINS_WITH_CARD});__webpack_require__.d(__webpack_exports__,"g",function(){return DOMAINS_WITH_MORE_INFO});__webpack_require__.d(__webpack_exports__,"c",function(){return DOMAINS_HIDE_MORE_INFO});__webpack_require__.d(__webpack_exports__,"d",function(){return DOMAINS_MORE_INFO_NO_HISTORY});__webpack_require__.d(__webpack_exports__,"h",function(){return STATES_OFF});__webpack_require__.d(__webpack_exports__,"e",function(){return DOMAINS_TOGGLE});__webpack_require__.d(__webpack_exports__,"i",function(){return UNIT_C});__webpack_require__.d(__webpack_exports__,"j",function(){return UNIT_F});__webpack_require__.d(__webpack_exports__,"b",function(){return DEFAULT_VIEW_ENTITY_ID});const DEFAULT_DOMAIN_ICON="hass:bookmark",DOMAINS_WITH_CARD=["climate","cover","configurator","input_select","input_number","input_text","lock","media_player","scene","script","timer","vacuum","water_heater","weblink"],DOMAINS_WITH_MORE_INFO=["alarm_control_panel","automation","camera","climate","configurator","cover","fan","group","history_graph","input_datetime","light","lock","media_player","script","sun","updater","vacuum","water_heater","weather"],DOMAINS_HIDE_MORE_INFO=["input_number","input_select","input_text","scene","weblink"],DOMAINS_MORE_INFO_NO_HISTORY=["camera","configurator","history_graph","scene"],STATES_OFF=["closed","locked","off"],DOMAINS_TOGGLE=new Set(["fan","input_boolean","light","switch"]),UNIT_C="\xB0C",UNIT_F="\xB0F",DEFAULT_VIEW_ENTITY_ID="group.default_view"},154:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.d(__webpack_exports__,"a",function(){return domainIcon});var _const__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(153);const fixedIcons={alert:"hass:alert",automation:"hass:playlist-play",calendar:"hass:calendar",camera:"hass:video",climate:"hass:thermostat",configurator:"hass:settings",conversation:"hass:text-to-speech",device_tracker:"hass:account",fan:"hass:fan",group:"hass:google-circles-communities",history_graph:"hass:chart-line",homeassistant:"hass:home-assistant",homekit:"hass:home-automation",image_processing:"hass:image-filter-frames",input_boolean:"hass:drawing",input_datetime:"hass:calendar-clock",input_number:"hass:ray-vertex",input_select:"hass:format-list-bulleted",input_text:"hass:textbox",light:"hass:lightbulb",mailbox:"hass:mailbox",notify:"hass:comment-alert",plant:"hass:flower",proximity:"hass:apple-safari",remote:"hass:remote",scene:"hass:google-pages",script:"hass:file-document",sensor:"hass:eye",simple_alarm:"hass:bell",sun:"hass:white-balance-sunny",switch:"hass:flash",timer:"hass:timer",updater:"hass:cloud-upload",vacuum:"hass:robot-vacuum",water_heater:"hass:thermometer",weblink:"hass:open-in-new"};function domainIcon(domain,state){if(domain in fixedIcons){return fixedIcons[domain]}switch(domain){case"alarm_control_panel":switch(state){case"armed_home":return"hass:bell-plus";case"armed_night":return"hass:bell-sleep";case"disarmed":return"hass:bell-outline";case"triggered":return"hass:bell-ring";default:return"hass:bell";}case"binary_sensor":return state&&"off"===state?"hass:radiobox-blank":"hass:checkbox-marked-circle";case"cover":return"closed"===state?"hass:window-closed":"hass:window-open";case"lock":return state&&"unlocked"===state?"hass:lock-open":"hass:lock";case"media_player":return state&&"off"!==state&&"idle"!==state?"hass:cast-connected":"hass:cast";case"zwave":switch(state){case"dead":return"hass:emoticon-dead";case"sleeping":return"hass:sleep";case"initializing":return"hass:timer-sand";default:return"hass:z-wave";}default:console.warn("Unable to find icon for domain "+domain+" ("+state+")");return _const__WEBPACK_IMPORTED_MODULE_0__.a;}}},155:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.d(__webpack_exports__,"a",function(){return computeDomain});function computeDomain(entityId){return entityId.substr(0,entityId.indexOf("."))}},157:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__(94);const IronIconClass=customElements.get("iron-icon");let loaded=!1;customElements.define("ha-icon",class extends IronIconClass{listen(...args){super.listen(...args);if(!loaded&&"mdi"===this._iconsetName){loaded=!0;__webpack_require__.e(47).then(__webpack_require__.bind(null,210))}}})},165:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(1),_polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(10),_ha_icon__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(157),_common_entity_compute_state_domain__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(151),_common_entity_state_icon__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(172);class StateBadge extends _polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_1__.a{static get template(){return _polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_0__.a`
      <style>
        :host {
          position: relative;
          display: inline-block;
          width: 40px;
          color: var(--paper-item-icon-color, #44739e);
          border-radius: 50%;
          height: 40px;
          text-align: center;
          background-size: cover;
          line-height: 40px;
        }

        ha-icon {
          transition: color 0.3s ease-in-out, filter 0.3s ease-in-out;
        }

        /* Color the icon if light or sun is on */
        ha-icon[data-domain="light"][data-state="on"],
        ha-icon[data-domain="switch"][data-state="on"],
        ha-icon[data-domain="binary_sensor"][data-state="on"],
        ha-icon[data-domain="fan"][data-state="on"],
        ha-icon[data-domain="sun"][data-state="above_horizon"] {
          color: var(--paper-item-icon-active-color, #fdd835);
        }

        /* Color the icon if unavailable */
        ha-icon[data-state="unavailable"] {
          color: var(--state-icon-unavailable-color);
        }
      </style>

      <ha-icon
        id="icon"
        data-domain$="[[_computeDomain(stateObj)]]"
        data-state$="[[stateObj.state]]"
        icon="[[_computeIcon(stateObj, overrideIcon)]]"
      ></ha-icon>
    `}static get properties(){return{stateObj:{type:Object,observer:"_updateIconAppearance"},overrideIcon:String}}_computeDomain(stateObj){return Object(_common_entity_compute_state_domain__WEBPACK_IMPORTED_MODULE_3__.a)(stateObj)}_computeIcon(stateObj,overrideIcon){return overrideIcon||Object(_common_entity_state_icon__WEBPACK_IMPORTED_MODULE_4__.a)(stateObj)}_updateIconAppearance(newVal){var errorMessage=null;const iconStyle={color:"",filter:""},hostStyle={backgroundImage:""};if(newVal.attributes.entity_picture){hostStyle.backgroundImage="url("+newVal.attributes.entity_picture+")";iconStyle.display="none"}else{if(newVal.attributes.hs_color){const hue=newVal.attributes.hs_color[0],sat=newVal.attributes.hs_color[1];if(10<sat)iconStyle.color=`hsl(${hue}, 100%, ${100-sat/2}%)`}if(newVal.attributes.brightness){const brightness=newVal.attributes.brightness;if("number"!==typeof brightness){errorMessage=`Type error: state-badge expected number, but type of ${newVal.entity_id}.attributes.brightness is ${typeof brightness} (${brightness})`;console.warn(errorMessage)}iconStyle.filter=`brightness(${(brightness+245)/5}%)`}}Object.assign(this.$.icon.style,iconStyle);Object.assign(this.style,hostStyle);if(errorMessage){throw new Error(`Frontend error: ${errorMessage}`)}}}customElements.define("state-badge",StateBadge)},172:function(module,__webpack_exports__,__webpack_require__){"use strict";var common_const=__webpack_require__(153),compute_domain=__webpack_require__(155),domain_icon=__webpack_require__(154);const fixedDeviceClassIcons={humidity:"hass:water-percent",illuminance:"hass:brightness-5",temperature:"hass:thermometer",pressure:"hass:gauge"};function sensorIcon(state){const dclass=state.attributes.device_class;if(dclass&&dclass in fixedDeviceClassIcons){return fixedDeviceClassIcons[dclass]}if("battery"===dclass){const battery=+state.state;if(isNaN(battery)){return"hass:battery-unknown"}const batteryRound=10*Math.round(battery/10);if(100<=batteryRound){return"hass:battery"}if(0>=batteryRound){return"hass:battery-alert"}return`${"hass"}:battery-${batteryRound}`}const unit=state.attributes.unit_of_measurement;if(unit===common_const.i||unit===common_const.j){return"hass:thermometer"}return Object(domain_icon.a)("sensor")}__webpack_require__.d(__webpack_exports__,"a",function(){return stateIcon});const domainIcons={binary_sensor:function(state){const activated=state.state&&"off"===state.state;switch(state.attributes.device_class){case"battery":return activated?"hass:battery":"hass:battery-outline";case"cold":return activated?"hass:thermometer":"hass:snowflake";case"connectivity":return activated?"hass:server-network-off":"hass:server-network";case"door":return activated?"hass:door-closed":"hass:door-open";case"garage_door":return activated?"hass:garage":"hass:garage-open";case"gas":case"power":case"problem":case"safety":case"smoke":return activated?"hass:verified":"hass:alert";case"heat":return activated?"hass:thermometer":"hass:fire";case"light":return activated?"hass:brightness-5":"hass:brightness-7";case"lock":return activated?"hass:lock":"hass:lock-open";case"moisture":return activated?"hass:water-off":"hass:water";case"motion":return activated?"hass:walk":"hass:run";case"occupancy":return activated?"hass:home-outline":"hass:home";case"opening":return activated?"hass:square":"hass:square-outline";case"plug":return activated?"hass:power-plug-off":"hass:power-plug";case"presence":return activated?"hass:home-outline":"hass:home";case"sound":return activated?"hass:music-note-off":"hass:music-note";case"vibration":return activated?"hass:crop-portrait":"hass:vibrate";case"window":return activated?"hass:window-closed":"hass:window-open";default:return activated?"hass:radiobox-blank":"hass:checkbox-marked-circle";}},cover:function(state){const open="closed"!==state.state;switch(state.attributes.device_class){case"garage":return open?"hass:garage-open":"hass:garage";default:return Object(domain_icon.a)("cover",state.state);}},sensor:sensorIcon,input_datetime:function(state){if(!state.attributes.has_date){return"hass:clock"}if(!state.attributes.has_time){return"hass:calendar"}return Object(domain_icon.a)("input_datetime")}};function stateIcon(state){if(!state){return common_const.a}if(state.attributes.icon){return state.attributes.icon}const domain=Object(compute_domain.a)(state.entity_id);if(domain in domainIcons){return domainIcons[domain](state)}return Object(domain_icon.a)(domain,state.state)}},181:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(1),_polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(10),_resources_ha_style__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(99);class HaConfigSection extends _polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_1__.a{static get template(){return _polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_0__.a`
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
    `}static get properties(){return{hass:{type:Object},narrow:{type:Boolean},showMenu:{type:Boolean,value:!1},isWide:{type:Boolean,value:!1}}}computeContentClasses(isWide){var classes="content ";return isWide?classes:classes+"narrow"}computeClasses(isWide){return"together layout "+(isWide?"horizontal":"vertical narrow")}}customElements.define("ha-config-section",HaConfigSection)},194:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_polymer_polymer_legacy_js__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(3),_polymer_iron_flex_layout_iron_flex_layout_js__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(33),_polymer_paper_styles_typography_js__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(50),_paper_item_shared_styles_js__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(127),_polymer_polymer_lib_legacy_polymer_fn_js__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(4),_polymer_polymer_lib_utils_html_tag_js__WEBPACK_IMPORTED_MODULE_5__=__webpack_require__(1),_paper_item_behavior_js__WEBPACK_IMPORTED_MODULE_6__=__webpack_require__(105);/**
@license
Copyright (c) 2015 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at
http://polymer.github.io/LICENSE.txt The complete set of authors may be found at
http://polymer.github.io/AUTHORS.txt The complete set of contributors may be
found at http://polymer.github.io/CONTRIBUTORS.txt Code distributed by Google as
part of the polymer project is also subject to an additional IP rights grant
found at http://polymer.github.io/PATENTS.txt
*/Object(_polymer_polymer_lib_legacy_polymer_fn_js__WEBPACK_IMPORTED_MODULE_4__.a)({_template:_polymer_polymer_lib_utils_html_tag_js__WEBPACK_IMPORTED_MODULE_5__.a`
    <style include="paper-item-shared-styles"></style>
    <style>
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
        @apply --paper-icon-item;
      }

      .content-icon {
        @apply --layout-horizontal;
        @apply --layout-center;

        width: var(--paper-item-icon-width, 56px);
        @apply --paper-item-icon;
      }
    </style>

    <div id="contentIcon" class="content-icon">
      <slot name="item-icon"></slot>
    </div>
    <slot></slot>
`,is:"paper-icon-item",behaviors:[_paper_item_behavior_js__WEBPACK_IMPORTED_MODULE_6__.a]})},205:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_app_layout_app_header_layout_app_header_layout__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(179),_polymer_app_layout_app_header_app_header__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(174),_polymer_app_layout_app_toolbar_app_toolbar__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(107),_polymer_paper_icon_button_paper_icon_button__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(98),_polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(1),_polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_5__=__webpack_require__(10);class HassSubpage extends _polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_5__.a{static get template(){return _polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_4__.a`
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
    `}static get properties(){return{header:String}}_backTapped(){history.back()}}customElements.define("hass-subpage",HassSubpage)},365:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(1),_polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(10),_ha_icon__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(157),_common_entity_state_icon__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(172);class HaStateIcon extends _polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_1__.a{static get template(){return _polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_0__.a`
      <ha-icon icon="[[computeIcon(stateObj)]]"></ha-icon>
    `}static get properties(){return{stateObj:{type:Object}}}computeIcon(stateObj){return Object(_common_entity_state_icon__WEBPACK_IMPORTED_MODULE_3__.a)(stateObj)}}customElements.define("ha-state-icon",HaStateIcon)},700:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.r(__webpack_exports__);var app_route=__webpack_require__(97),html_tag=__webpack_require__(1),polymer_element=__webpack_require__(10),debounce=__webpack_require__(14),utils_async=__webpack_require__(8),iron_flex_layout_classes=__webpack_require__(79),paper_tooltip=__webpack_require__(241),paper_button=__webpack_require__(72),paper_card=__webpack_require__(152),iron_icon=__webpack_require__(94),paper_item=__webpack_require__(125),paper_item_body=__webpack_require__(163),ha_state_icon=__webpack_require__(365),hass_subpage=__webpack_require__(205),ha_style=__webpack_require__(99),ha_config_section=__webpack_require__(181),events_mixin=__webpack_require__(48),localize_mixin=__webpack_require__(71),compute_state_name=__webpack_require__(104);let registeredDialog=!1;class ha_config_entries_dashboard_HaConfigManagerDashboard extends Object(localize_mixin.a)(Object(events_mixin.a)(polymer_element.a)){static get template(){return html_tag.a`
      <style include="iron-flex ha-style">
        paper-button {
          color: var(--primary-color);
          font-weight: 500;
          top: 3px;
          margin-right: -0.57em;
        }
        paper-card:last-child {
          margin-top: 12px;
        }
        .config-entry-row {
          display: flex;
          padding: 0 16px;
        }
        ha-state-icon {
          cursor: pointer;
        }
        .configured a {
          color: var(--primary-text-color);
          text-decoration: none;
        }
      </style>

      <hass-subpage
        header="[[localize('ui.panel.config.integrations.caption')]]"
      >
        <template is="dom-if" if="[[progress.length]]">
          <ha-config-section>
            <span slot="header"
              >[[localize('ui.panel.config.integrations.discovered')]]</span
            >
            <paper-card>
              <template is="dom-repeat" items="[[progress]]">
                <div class="config-entry-row">
                  <paper-item-body>
                    [[_computeIntegrationTitle(localize, item.handler)]]
                  </paper-item-body>
                  <paper-button on-click="_continueFlow"
                    >[[localize('ui.panel.config.integrations.configure')]]</paper-button
                  >
                </div>
              </template>
            </paper-card>
          </ha-config-section>
        </template>

        <ha-config-section class="configured">
          <span slot="header"
            >[[localize('ui.panel.config.integrations.configured')]]</span
          >
          <paper-card>
            <template is="dom-if" if="[[!entries.length]]">
              <div class="config-entry-row">
                <paper-item-body two-line>
                  <div>[[localize('ui.panel.config.integrations.none')]]</div>
                </paper-item-body>
              </div>
            </template>
            <template is="dom-repeat" items="[[entries]]">
              <a href="/config/integrations/[[item.entry_id]]">
                <paper-item>
                  <paper-item-body two-line>
                    <div>
                      [[_computeIntegrationTitle(localize, item.domain)]]:
                      [[item.title]]
                    </div>
                    <div secondary>
                      <template
                        is="dom-repeat"
                        items="[[_computeConfigEntryEntities(hass, item, entities)]]"
                      >
                        <span>
                          <ha-state-icon
                            state-obj="[[item]]"
                            on-click="_handleMoreInfo"
                          ></ha-state-icon>
                          <paper-tooltip position="bottom"
                            >[[_computeStateName(item)]]</paper-tooltip
                          >
                        </span>
                      </template>
                    </div>
                  </paper-item-body>
                  <iron-icon icon="hass:chevron-right"></iron-icon>
                </paper-item>
              </a>
            </template>
          </paper-card>
        </ha-config-section>

        <ha-config-section>
          <span slot="header"
            >[[localize('ui.panel.config.integrations.new')]]</span
          >
          <paper-card>
            <template is="dom-repeat" items="[[handlers]]">
              <div class="config-entry-row">
                <paper-item-body>
                  [[_computeIntegrationTitle(localize, item)]]
                </paper-item-body>
                <paper-button on-click="_createFlow"
                  >[[localize('ui.panel.config.integrations.configure')]]</paper-button
                >
              </div>
            </template>
          </paper-card>
        </ha-config-section>
      </hass-subpage>
    `}static get properties(){return{hass:Object,isWide:Boolean,entries:Array,entities:Array,progress:Array,handlers:Array}}connectedCallback(){super.connectedCallback();if(!registeredDialog){registeredDialog=!0;this.fire("register-dialog",{dialogShowEvent:"show-config-flow",dialogTag:"ha-config-flow",dialogImport:()=>Promise.all([__webpack_require__.e(1),__webpack_require__.e(2),__webpack_require__.e(3),__webpack_require__.e(7),__webpack_require__.e(66)]).then(__webpack_require__.bind(null,732))})}}_createFlow(ev){this.fire("show-config-flow",{hass:this.hass,newFlowForHandler:ev.model.item,dialogClosedCallback:()=>this.fire("hass-reload-entries")})}_continueFlow(ev){this.fire("show-config-flow",{hass:this.hass,continueFlowId:ev.model.item.flow_id,dialogClosedCallback:()=>this.fire("hass-reload-entries")})}_computeIntegrationTitle(localize,integration){return localize(`component.${integration}.config.title`)}_computeConfigEntryEntities(hass,configEntry,entities){if(!entities){return[]}const states=[];entities.forEach(entity=>{if(entity.config_entry_id===configEntry.entry_id&&entity.entity_id in hass.states){states.push(hass.states[entity.entity_id])}});return states}_computeStateName(stateObj){return Object(compute_state_name.a)(stateObj)}_handleMoreInfo(ev){this.fire("hass-more-info",{entityId:ev.model.item.entity_id})}}customElements.define("ha-config-entries-dashboard",ha_config_entries_dashboard_HaConfigManagerDashboard);var state_badge=__webpack_require__(165),compare=(a,b)=>{if(a<b){return-1}if(a>b){return 1}return 0},paper_icon_item=__webpack_require__(194);function computeEntityName(hass,entity){if(entity.name)return entity.name;const state=hass.states[entity.entity_id];return state?Object(compute_state_name.a)(state):null}class ha_device_card_HaDeviceCard extends Object(events_mixin.a)(Object(localize_mixin.a)(polymer_element.a)){static get template(){return html_tag.a`
      <style>
        :host(:not([narrow])) .device-entities {
          max-height: 225px;
          overflow: auto;
        }
        paper-card {
          flex: 1 0 100%;
          padding-bottom: 10px;
          min-width: 0;
        }
        .device {
          width: 30%;
        }
        .device .name {
          font-weight: bold;
        }
        .device .model,
        .device .manuf {
          color: var(--secondary-text-color);
        }
        .extra-info {
          margin-top: 8px;
        }
        paper-icon-item {
          cursor: pointer;
          padding-top: 4px;
          padding-bottom: 4px;
        }
        .manuf,
        .entity-id {
          color: var(--secondary-text-color);
        }
      </style>
      <paper-card heading="[[device.name]]">
        <div class="card-content">
          <!--
            <h1>[[configEntry.title]] ([[_computeIntegrationTitle(localize, configEntry.domain)]])</h1>
          -->
          <div class="info">
            <div class="model">[[device.model]]</div>
            <div class="manuf">
              [[localize('ui.panel.config.integrations.config_entry.manuf',
              'manufacturer', device.manufacturer)]]
            </div>
          </div>
          <template is="dom-if" if="[[device.hub_device_id]]">
            <div class="extra-info">
              [[localize('ui.panel.config.integrations.config_entry.hub')]]
              <span class="hub"
                >[[_computeDeviceName(devices, device.hub_device_id)]]</span
              >
            </div>
          </template>
          <template is="dom-if" if="[[device.sw_version]]">
            <div class="extra-info">
              [[localize('ui.panel.config.integrations.config_entry.firmware',
              'version', device.sw_version)]]
            </div>
          </template>
        </div>

        <div class="device-entities">
          <template
            is="dom-repeat"
            items="[[_computeDeviceEntities(hass, device, entities)]]"
            as="entity"
          >
            <paper-icon-item on-click="_openMoreInfo">
              <state-badge
                state-obj="[[_computeStateObj(entity, hass)]]"
                slot="item-icon"
              ></state-badge>
              <paper-item-body>
                <div class="name">[[_computeEntityName(entity, hass)]]</div>
                <div class="secondary entity-id">[[entity.entity_id]]</div>
              </paper-item-body>
            </paper-icon-item>
          </template>
        </div>
      </paper-card>
    `}static get properties(){return{device:Object,devices:Array,entities:Array,hass:Object,narrow:{type:Boolean,reflectToAttribute:!0},_childDevices:{type:Array,computed:"_computeChildDevices(device, devices)"}}}_computeChildDevices(device,devices){return devices.filter(dev=>dev.hub_device_id===device.id).sort((dev1,dev2)=>compare(dev1.name,dev2.name))}_computeDeviceEntities(hass,device,entities){return entities.filter(entity=>entity.device_id===device.id).sort((ent1,ent2)=>compare(computeEntityName(hass,ent1)||`zzz${ent1.entity_id}`,computeEntityName(hass,ent2)||`zzz${ent2.entity_id}`))}_computeStateObj(entity,hass){return hass.states[entity.entity_id]}_computeEntityName(entity,hass){return computeEntityName(hass,entity)||`(${this.localize("ui.panel.config.integrations.config_entry.entity_unavailable")})`}_computeDeviceName(devices,deviceId){const device=devices.find(dev=>dev.id===deviceId);return device?device.name:`(${this.localize("ui.panel.config.integrations.config_entry.device_unavailable")})`}_openMoreInfo(ev){this.fire("hass-more-info",{entityId:ev.model.entity.entity_id})}}customElements.define("ha-device-card",ha_device_card_HaDeviceCard);function ha_ce_entities_card_computeEntityName(hass,entity){if(entity.name)return entity.name;const state=hass.states[entity.entity_id];return state?Object(compute_state_name.a)(state):null}class ha_ce_entities_card_HaCeEntitiesCard extends Object(localize_mixin.a)(Object(events_mixin.a)(polymer_element.a)){static get template(){return html_tag.a`
      <style>
        paper-card {
          flex: 1 0 100%;
          padding-bottom: 8px;
        }
        paper-icon-item {
          cursor: pointer;
          padding-top: 4px;
          padding-bottom: 4px;
        }
      </style>
      <paper-card heading="[[heading]]">
        <template is="dom-repeat" items="[[entities]]" as="entity">
          <paper-icon-item on-click="_openMoreInfo">
            <state-badge
              state-obj="[[_computeStateObj(entity, hass)]]"
              slot="item-icon"
            ></state-badge>
            <paper-item-body>
              <div class="name">[[_computeEntityName(entity, hass)]]</div>
              <div class="secondary entity-id">[[entity.entity_id]]</div>
            </paper-item-body>
          </paper-icon-item>
        </template>
      </paper-card>
    `}static get properties(){return{heading:String,entities:Array,hass:Object}}_computeStateObj(entity,hass){return hass.states[entity.entity_id]}_computeEntityName(entity,hass){return ha_ce_entities_card_computeEntityName(hass,entity)||`(${this.localize("ui.panel.config.integrations.config_entry.entity_unavailable")})`}_openMoreInfo(ev){this.fire("hass-more-info",{entityId:ev.model.entity.entity_id})}}customElements.define("ha-ce-entities-card",ha_ce_entities_card_HaCeEntitiesCard);var navigate_mixin=__webpack_require__(95);class ha_config_entry_page_HaConfigEntryPage extends Object(navigate_mixin.a)(Object(events_mixin.a)(Object(localize_mixin.a)(polymer_element.a))){static get template(){return html_tag.a`
      <style>
        .content {
          display: flex;
          flex-wrap: wrap;
          padding: 4px;
          justify-content: center;
        }
        .card {
          box-sizing: border-box;
          display: flex;
          flex: 1 0 300px;
          min-width: 0;
          max-width: 500px;
          padding: 8px;
        }
      </style>
      <hass-subpage header="[[configEntry.title]]">
        <paper-icon-button
          slot="toolbar-icon"
          icon="hass:delete"
          on-click="_removeEntry"
        ></paper-icon-button>
        <div class="content">
          <template
            is="dom-if"
            if="[[_computeIsEmpty(_configEntryDevices, _noDeviceEntities)]]"
          >
            <p>
              [[localize('ui.panel.config.integrations.config_entry.no_devices')]]
            </p>
          </template>
          <template is="dom-repeat" items="[[_configEntryDevices]]" as="device">
            <ha-device-card
              class="card"
              hass="[[hass]]"
              devices="[[devices]]"
              device="[[device]]"
              entities="[[entities]]"
              narrow="[[narrow]]"
            ></ha-device-card>
          </template>
          <template is="dom-if" if="[[_noDeviceEntities.length]]">
            <ha-ce-entities-card
              class="card"
              heading="[[localize('ui.panel.config.integrations.config_entry.no_device')]]"
              entities="[[_noDeviceEntities]]"
              hass="[[hass]]"
              narrow="[[narrow]]"
            ></ha-ce-entities-card>
          </template>
        </div>
      </hass-subpage>
    `}static get properties(){return{hass:Object,isWide:Boolean,narrow:Boolean,configEntry:{type:Object,value:null},_configEntryDevices:{type:Array,computed:"_computeConfigEntryDevices(configEntry, devices)"},_noDeviceEntities:{type:Array,computed:"_computeNoDeviceEntities(configEntry, entities)"},devices:Array,entries:Array,entities:Array}}_computeConfigEntryDevices(configEntry,devices){if(!devices)return[];return devices.filter(device=>device.config_entries.includes(configEntry.entry_id)).sort((dev1,dev2)=>!!dev1.hub_device_id-!!dev2.hub_device_id||compare(dev1.name,dev2.name))}_computeNoDeviceEntities(configEntry,entities){if(!entities)return[];return entities.filter(ent=>!ent.device_id&&ent.config_entry_id===configEntry.entry_id)}_computeIsEmpty(configEntryDevices,noDeviceEntities){return 0===configEntryDevices.length&&0===noDeviceEntities.length}_removeEntry(){if(!confirm(this.localize("ui.panel.config.integrations.config_entry.delete_confirm")))return;const entryId=this.configEntry.entry_id;this.hass.callApi("delete",`config/config_entries/entry/${entryId}`).then(result=>{this.fire("hass-reload-entries");if(result.require_restart){alert(this.localize("ui.panel.config.integrations.config_entry.restart_confirm"))}this.navigate("/config/integrations/dashboard",!0)})}}customElements.define("ha-config-entry-page",ha_config_entry_page_HaConfigEntryPage);class ha_config_entries_HaConfigEntries extends Object(navigate_mixin.a)(polymer_element.a){static get template(){return html_tag.a`
      <app-route
        route="[[route]]"
        pattern="/integrations/:page"
        data="{{_routeData}}"
        tail="{{_routeTail}}"
      ></app-route>

      <template is="dom-if" if="[[_configEntry]]">
        <ha-config-entry-page
          hass="[[hass]]"
          config-entry="[[_configEntry]]"
          entries="[[_entries]]"
          entities="[[_entities]]"
          devices="[[_devices]]"
          narrow="[[narrow]]"
        ></ha-config-entry-page>
      </template>
      <template is="dom-if" if="[[!_configEntry]]">
        <ha-config-entries-dashboard
          hass="[[hass]]"
          entries="[[_entries]]"
          entities="[[_entities]]"
          handlers="[[_handlers]]"
          progress="[[_progress]]"
        ></ha-config-entries-dashboard>
      </template>
    `}static get properties(){return{hass:Object,isWide:Boolean,narrow:Boolean,route:Object,_configEntry:{type:Object,computed:"_computeConfigEntry(_routeData, _entries)"},_entries:Array,_entities:Array,_devices:Array,_progress:Array,_handlers:Array,_routeData:Object,_routeTail:Object}}ready(){super.ready();this._loadData();this.addEventListener("hass-reload-entries",()=>this._loadData())}connectedCallback(){super.connectedCallback();this.hass.connection.subscribeEvents(()=>{this._debouncer=debounce.a.debounce(this._debouncer,utils_async.d.after(500),()=>this._loadData())},"config_entry_discovered").then(unsub=>{this._unsubEvents=unsub})}disconnectedCallback(){super.disconnectedCallback();if(this._unsubEvents)this._unsubEvents()}_loadData(){this.hass.callApi("get","config/config_entries/entry").then(entries=>{this._entries=entries.sort((conf1,conf2)=>compare(conf1.title,conf2.title))});this.hass.callApi("get","config/config_entries/flow").then(progress=>{this._progress=progress});this.hass.callApi("get","config/config_entries/flow_handlers").then(handlers=>{this._handlers=handlers});this.hass.callWS({type:"config/entity_registry/list"}).then(entities=>{this._entities=entities});this.hass.callWS({type:"config/device_registry/list"}).then(devices=>{this._devices=devices})}_computeConfigEntry(routeData,entries){return!!entries&&!!routeData&&entries.find(ent=>ent.entry_id===routeData.page)}}customElements.define("ha-config-entries",ha_config_entries_HaConfigEntries)}}]);
//# sourceMappingURL=c8729513fa57fd781fc8.chunk.js.map
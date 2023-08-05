(window.webpackJsonp=window.webpackJsonp||[]).push([[32],{170:function(module,__webpack_exports__,__webpack_require__){"use strict";var fecha__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(167);__webpack_exports__.a=function(){try{new Date().toLocaleString("i")}catch(e){return"RangeError"===e.name}return!1}()?(dateObj,locales)=>dateObj.toLocaleString(locales,{year:"numeric",month:"long",day:"numeric",hour:"numeric",minute:"2-digit"}):dateObj=>fecha__WEBPACK_IMPORTED_MODULE_0__.a.format(dateObj,"haDateTime")},719:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.r(__webpack_exports__);var _polymer_app_layout_app_header_layout_app_header_layout__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(179),_polymer_app_layout_app_header_app_header__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(174),_polymer_app_layout_app_toolbar_app_toolbar__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(107),_polymer_paper_button_paper_button__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(72),_polymer_paper_card_paper_card__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(152),_polymer_paper_input_paper_textarea__WEBPACK_IMPORTED_MODULE_5__=__webpack_require__(191),_polymer_paper_item_paper_item_body__WEBPACK_IMPORTED_MODULE_6__=__webpack_require__(163),_polymer_paper_item_paper_item__WEBPACK_IMPORTED_MODULE_7__=__webpack_require__(125),_polymer_paper_tabs_paper_tab__WEBPACK_IMPORTED_MODULE_8__=__webpack_require__(212),_polymer_paper_tabs_paper_tabs__WEBPACK_IMPORTED_MODULE_9__=__webpack_require__(239),_polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_10__=__webpack_require__(1),_polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_11__=__webpack_require__(10),_components_ha_menu_button__WEBPACK_IMPORTED_MODULE_12__=__webpack_require__(132),_resources_ha_style__WEBPACK_IMPORTED_MODULE_13__=__webpack_require__(99),_common_datetime_format_date_time__WEBPACK_IMPORTED_MODULE_14__=__webpack_require__(170),_mixins_localize_mixin__WEBPACK_IMPORTED_MODULE_15__=__webpack_require__(71),_mixins_events_mixin__WEBPACK_IMPORTED_MODULE_16__=__webpack_require__(48);let registeredDialog=!1;class HaPanelMailbox extends Object(_mixins_events_mixin__WEBPACK_IMPORTED_MODULE_16__.a)(Object(_mixins_localize_mixin__WEBPACK_IMPORTED_MODULE_15__.a)(_polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_11__.a)){static get template(){return _polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_10__.a`
      <style include="ha-style">
        :host {
          -ms-user-select: initial;
          -webkit-user-select: initial;
          -moz-user-select: initial;
        }

        .content {
          padding: 16px;
          max-width: 600px;
          margin: 0 auto;
        }

        paper-card {
          display: block;
        }

        paper-item {
          cursor: pointer;
        }

        .empty {
          text-align: center;
          color: var(--secondary-text-color);
        }

        .header {
          @apply --paper-font-title;
        }

        .row {
          display: flex;
          justify-content: space-between;
        }

        @media all and (max-width: 450px) {
          .content {
            width: auto;
            padding: 0;
          }
        }

        .tip {
          color: var(--secondary-text-color);
          font-size: 14px;
        }
        .date {
          color: var(--primary-text-color);
        }
      </style>

      <app-header-layout has-scrolling-region>
        <app-header slot="header" fixed>
          <app-toolbar>
            <ha-menu-button
              narrow="[[narrow]]"
              show-menu="[[showMenu]]"
            ></ha-menu-button>
            <div main-title>[[localize('panel.mailbox')]]</div>
          </app-toolbar>
          <div sticky hidden$="[[areTabsHidden(platforms)]]">
            <paper-tabs
              scrollable
              selected="[[_currentPlatform]]"
              on-iron-activate="handlePlatformSelected"
            >
              <template is="dom-repeat" items="[[platforms]]">
                <paper-tab data-entity="[[item]]">
                  [[getPlatformName(item)]]
                </paper-tab>
              </template>
            </paper-tabs>
          </div>
        </app-header>
        <div class="content">
          <paper-card>
            <template is="dom-if" if="[[!_messages.length]]">
              <div class="card-content empty">
                [[localize('ui.panel.mailbox.empty')]]
              </div>
            </template>
            <template is="dom-repeat" items="[[_messages]]">
              <paper-item on-click="openMP3Dialog">
                <paper-item-body style="width:100%" two-line>
                  <div class="row">
                    <div>[[item.caller]]</div>
                    <div class="tip">
                      [[localize('ui.duration.second', 'count', item.duration)]]
                    </div>
                  </div>
                  <div secondary>
                    <span class="date">[[item.timestamp]]</span> -
                    [[item.message]]
                  </div>
                </paper-item-body>
              </paper-item>
            </template>
          </paper-card>
        </div>
      </app-header-layout>
    `}static get properties(){return{hass:{type:Object},narrow:{type:Boolean,value:!1},showMenu:{type:Boolean,value:!1},platforms:{type:Array},_messages:{type:Array},_currentPlatform:{type:Number,value:0}}}connectedCallback(){super.connectedCallback();if(!registeredDialog){registeredDialog=!0;this.fire("register-dialog",{dialogShowEvent:"show-audio-message-dialog",dialogTag:"ha-dialog-show-audio-message",dialogImport:()=>Promise.all([__webpack_require__.e(2),__webpack_require__.e(63)]).then(__webpack_require__.bind(null,695))})}this.hassChanged=this.hassChanged.bind(this);this.hass.connection.subscribeEvents(this.hassChanged,"mailbox_updated").then(function(unsub){this._unsubEvents=unsub}.bind(this));this.computePlatforms().then(function(platforms){this.platforms=platforms;this.hassChanged()}.bind(this))}disconnectedCallback(){super.disconnectedCallback();if(this._unsubEvents)this._unsubEvents()}hassChanged(){if(!this._messages){this._messages=[]}this.getMessages().then(function(items){this._messages=items}.bind(this))}openMP3Dialog(event){this.fire("show-audio-message-dialog",{hass:this.hass,message:event.model.item})}getMessages(){const platform=this.platforms[this._currentPlatform];return this.hass.callApi("GET",`mailbox/messages/${platform.name}`).then(values=>{const platformItems=[],arrayLength=values.length;for(let i=0;i<arrayLength;i++){const datetime=Object(_common_datetime_format_date_time__WEBPACK_IMPORTED_MODULE_14__.a)(new Date(1e3*values[i].info.origtime),this.hass.language);platformItems.push({timestamp:datetime,caller:values[i].info.callerid,message:values[i].text,sha:values[i].sha,duration:values[i].info.duration,platform:platform})}return platformItems.sort(function(a,b){return new Date(b.timestamp)-new Date(a.timestamp)})})}computePlatforms(){return this.hass.callApi("GET","mailbox/platforms")}handlePlatformSelected(ev){const newPlatform=ev.detail.selected;if(newPlatform!==this._currentPlatform){this._currentPlatform=newPlatform;this.hassChanged()}}areTabsHidden(platforms){return!platforms||2>platforms.length}getPlatformName(item){const entity=`mailbox.${item.name}`,stateObj=this.hass.states[entity.toLowerCase()];return stateObj.attributes.friendly_name}}customElements.define("ha-panel-mailbox",HaPanelMailbox)}}]);
//# sourceMappingURL=ccc5441bcd9be4ac7dcc.chunk.js.map
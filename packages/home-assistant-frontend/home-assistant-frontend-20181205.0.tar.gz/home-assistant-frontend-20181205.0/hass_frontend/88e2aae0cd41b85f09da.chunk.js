(window.webpackJsonp=window.webpackJsonp||[]).push([[55],{205:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_app_layout_app_header_layout_app_header_layout__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(179),_polymer_app_layout_app_header_app_header__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(174),_polymer_app_layout_app_toolbar_app_toolbar__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(107),_polymer_paper_icon_button_paper_icon_button__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(98),_polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(1),_polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_5__=__webpack_require__(10);class HassSubpage extends _polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_5__.a{static get template(){return _polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_4__.a`
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
    `}static get properties(){return{header:String}}_backTapped(){history.back()}}customElements.define("hass-subpage",HassSubpage)},703:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.r(__webpack_exports__);var app_route=__webpack_require__(97),utils_async=__webpack_require__(8),debounce=__webpack_require__(14),html_tag=__webpack_require__(1),polymer_element=__webpack_require__(10),navigate_mixin=__webpack_require__(95),paper_fab=__webpack_require__(228),paper_item=__webpack_require__(125),paper_card=__webpack_require__(152),paper_item_body=__webpack_require__(163),hass_subpage=__webpack_require__(205),localize_mixin=__webpack_require__(71),events_mixin=__webpack_require__(48);let registeredDialog=!1;class ha_user_picker_HaUserPicker extends Object(events_mixin.a)(Object(navigate_mixin.a)(Object(localize_mixin.a)(polymer_element.a))){static get template(){return html_tag.a`
      <style>
        paper-fab {
          position: fixed;
          bottom: 16px;
          right: 16px;
          z-index: 1;
        }
        paper-fab[is-wide] {
          bottom: 24px;
          right: 24px;
        }
        paper-card {
          display: block;
          max-width: 600px;
          margin: 16px auto;
        }
        a {
          text-decoration: none;
          color: var(--primary-text-color);
        }
      </style>

      <hass-subpage header="[[localize('ui.panel.config.users.picker.title')]]">
        <paper-card>
          <template is="dom-repeat" items="[[users]]" as="user">
            <a href="[[_computeUrl(user)]]">
              <paper-item>
                <paper-item-body two-line>
                  <div>[[_withDefault(user.name, 'Unnamed User')]]</div>
                  <div secondary="">
                    [[user.id]]
                    <template is="dom-if" if="[[user.system_generated]]">
                      - System Generated
                    </template>
                  </div>
                </paper-item-body>
                <iron-icon icon="hass:chevron-right"></iron-icon>
              </paper-item>
            </a>
          </template>
        </paper-card>

        <paper-fab
          is-wide$="[[isWide]]"
          icon="hass:plus"
          title="[[localize('ui.panel.config.users.picker.add_user')]]"
          on-click="_addUser"
        ></paper-fab>
      </hass-subpage>
    `}static get properties(){return{hass:Object,users:Array}}connectedCallback(){super.connectedCallback();if(!registeredDialog){registeredDialog=!0;this.fire("register-dialog",{dialogShowEvent:"show-add-user",dialogTag:"ha-dialog-add-user",dialogImport:()=>Promise.all([__webpack_require__.e(2),__webpack_require__.e(67)]).then(__webpack_require__.bind(null,733))})}}_withDefault(value,defaultValue){return value||defaultValue}_computeUrl(user){return`/config/users/${user.id}`}_addUser(){this.fire("show-add-user",{hass:this.hass,dialogClosedCallback:async({userId})=>{this.fire("reload-users");if(userId)this.navigate(`/config/users/${userId}`)}})}}customElements.define("ha-user-picker",ha_user_picker_HaUserPicker);__webpack_require__(72);class ha_user_editor_HaUserEditor extends Object(events_mixin.a)(Object(navigate_mixin.a)(Object(localize_mixin.a)(polymer_element.a))){static get template(){return html_tag.a`
      <style>
        paper-card {
          display: block;
          max-width: 600px;
          margin: 0 auto 16px;
        }
        paper-card:first-child {
          margin-top: 16px;
        }
        paper-card:last-child {
          margin-bottom: 16px;
        }
      </style>

      <hass-subpage header="View user">
        <paper-card heading="[[_computeName(user)]]">
          <table class="card-content">
            <tr>
              <td>ID</td>
              <td>[[user.id]]</td>
            </tr>
            <tr>
              <td>Owner</td>
              <td>[[user.is_owner]]</td>
            </tr>
            <tr>
              <td>Active</td>
              <td>[[user.is_active]]</td>
            </tr>
            <tr>
              <td>System generated</td>
              <td>[[user.system_generated]]</td>
            </tr>
          </table>
        </paper-card>
        <paper-card>
          <div class="card-actions">
            <paper-button
              on-click="_deleteUser"
              disabled="[[user.system_generated]]"
            >
              [[localize('ui.panel.config.users.editor.delete_user')]]
            </paper-button>
            <template is="dom-if" if="[[user.system_generated]]">
              Unable to remove system generated users.
            </template>
          </div>
        </paper-card>
      </hass-subpage>
    `}static get properties(){return{hass:Object,user:Object}}_computeName(user){return user&&(user.name||"Unnamed user")}async _deleteUser(ev){if(!confirm(`Are you sure you want to delete ${this._computeName(this.user)}`)){ev.target.blur();return}try{await this.hass.callWS({type:"config/auth/delete",user_id:this.user.id})}catch(err){alert(err.code);return}this.fire("reload-users");this.navigate("/config/users")}}customElements.define("ha-user-editor",ha_user_editor_HaUserEditor);var fire_event=__webpack_require__(65);class ha_config_users_HaConfigUsers extends Object(navigate_mixin.a)(polymer_element.a){static get template(){return html_tag.a`
      <app-route
        route="[[route]]"
        pattern="/users/:user"
        data="{{_routeData}}"
      ></app-route>

      <template
        is="dom-if"
        if="[[_equals(_routeData.user, &quot;picker&quot;)]]"
      >
        <ha-user-picker hass="[[hass]]" users="[[_users]]"></ha-user-picker>
      </template>
      <template
        is="dom-if"
        if="[[!_equals(_routeData.user, &quot;picker&quot;)]]"
        restamp
      >
        <ha-user-editor
          hass="[[hass]]"
          user="[[_computeUser(_users, _routeData.user)]]"
        ></ha-user-editor>
      </template>
    `}static get properties(){return{hass:Object,route:{type:Object,observer:"_checkRoute"},_routeData:Object,_user:{type:Object,value:null},_users:{type:Array,value:null}}}ready(){super.ready();this._loadData();this.addEventListener("reload-users",()=>this._loadData())}_handlePickUser(ev){this._user=ev.detail.user}_checkRoute(route){if(!route||"/users"!==route.path.substr(0,6))return;Object(fire_event.a)(this,"iron-resize");this._debouncer=debounce.a.debounce(this._debouncer,utils_async.d.after(0),()=>{if("/users"===route.path){this.navigate("/config/users/picker",!0)}})}_computeUser(users,userId){return users&&users.filter(u=>u.id===userId)[0]}_equals(a,b){return a===b}async _loadData(){this._users=await this.hass.callWS({type:"config/auth/list"})}}customElements.define("ha-config-users",ha_config_users_HaConfigUsers)}}]);
//# sourceMappingURL=88e2aae0cd41b85f09da.chunk.js.map
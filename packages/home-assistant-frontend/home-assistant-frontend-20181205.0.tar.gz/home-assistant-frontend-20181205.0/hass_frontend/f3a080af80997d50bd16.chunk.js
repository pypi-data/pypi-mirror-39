(window.webpackJsonp=window.webpackJsonp||[]).push([[16],{105:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.d(__webpack_exports__,"a",function(){return PaperItemBehavior});var _polymer_polymer_polymer_legacy_js__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(3),_polymer_iron_behaviors_iron_button_state_js__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(23),_polymer_iron_behaviors_iron_control_state_js__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(18);/**
@license
Copyright (c) 2015 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at
http://polymer.github.io/LICENSE.txt The complete set of authors may be found at
http://polymer.github.io/AUTHORS.txt The complete set of contributors may be
found at http://polymer.github.io/CONTRIBUTORS.txt Code distributed by Google as
part of the polymer project is also subject to an additional IP rights grant
found at http://polymer.github.io/PATENTS.txt
*/const PaperItemBehavior=[_polymer_iron_behaviors_iron_button_state_js__WEBPACK_IMPORTED_MODULE_1__.a,_polymer_iron_behaviors_iron_control_state_js__WEBPACK_IMPORTED_MODULE_2__.a,{hostAttributes:{role:"option",tabindex:"0"}}]},125:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_polymer_polymer_legacy_js__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(3),_polymer_iron_flex_layout_iron_flex_layout_js__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(33),_paper_item_shared_styles_js__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(127),_polymer_polymer_lib_legacy_polymer_fn_js__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(4),_polymer_polymer_lib_utils_html_tag_js__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(1),_paper_item_behavior_js__WEBPACK_IMPORTED_MODULE_5__=__webpack_require__(105);/**
@license
Copyright (c) 2015 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at
http://polymer.github.io/LICENSE.txt The complete set of authors may be found at
http://polymer.github.io/AUTHORS.txt The complete set of contributors may be
found at http://polymer.github.io/CONTRIBUTORS.txt Code distributed by Google as
part of the polymer project is also subject to an additional IP rights grant
found at http://polymer.github.io/PATENTS.txt
*/Object(_polymer_polymer_lib_legacy_polymer_fn_js__WEBPACK_IMPORTED_MODULE_3__.a)({_template:_polymer_polymer_lib_utils_html_tag_js__WEBPACK_IMPORTED_MODULE_4__.a`
    <style include="paper-item-shared-styles">
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
      }
    </style>
    <slot></slot>
`,is:"paper-item",behaviors:[_paper_item_behavior_js__WEBPACK_IMPORTED_MODULE_5__.a]})},126:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_polymer_polymer_legacy_js__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(3),_polymer_paper_styles_default_theme_js__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(39),_polymer_iron_menu_behavior_iron_menu_behavior_js__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(110),_polymer_polymer_lib_legacy_polymer_fn_js__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(4),_polymer_polymer_lib_utils_html_tag_js__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(1);/**
@license
Copyright (c) 2015 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at
http://polymer.github.io/LICENSE.txt The complete set of authors may be found at
http://polymer.github.io/AUTHORS.txt The complete set of contributors may be
found at http://polymer.github.io/CONTRIBUTORS.txt Code distributed by Google as
part of the polymer project is also subject to an additional IP rights grant
found at http://polymer.github.io/PATENTS.txt
*/Object(_polymer_polymer_lib_legacy_polymer_fn_js__WEBPACK_IMPORTED_MODULE_3__.a)({_template:_polymer_polymer_lib_utils_html_tag_js__WEBPACK_IMPORTED_MODULE_4__.a`
    <style>
      :host {
        display: block;
        padding: 8px 0;

        background: var(--paper-listbox-background-color, var(--primary-background-color));
        color: var(--paper-listbox-color, var(--primary-text-color));

        @apply --paper-listbox;
      }
    </style>

    <slot></slot>
`,is:"paper-listbox",behaviors:[_polymer_iron_menu_behavior_iron_menu_behavior_js__WEBPACK_IMPORTED_MODULE_2__.a],hostAttributes:{role:"listbox"}})},127:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_iron_flex_layout_iron_flex_layout_js__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(33),_polymer_paper_styles_color_js__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(58),_polymer_paper_styles_color_js__WEBPACK_IMPORTED_MODULE_1___default=__webpack_require__.n(_polymer_paper_styles_color_js__WEBPACK_IMPORTED_MODULE_1__),_polymer_paper_styles_default_theme_js__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(39),_polymer_paper_styles_typography_js__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(50);/**
@license
Copyright (c) 2015 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at
http://polymer.github.io/LICENSE.txt The complete set of authors may be found at
http://polymer.github.io/AUTHORS.txt The complete set of contributors may be
found at http://polymer.github.io/CONTRIBUTORS.txt Code distributed by Google as
part of the polymer project is also subject to an additional IP rights grant
found at http://polymer.github.io/PATENTS.txt
*/const $_documentContainer=document.createElement("template");$_documentContainer.setAttribute("style","display: none;");$_documentContainer.innerHTML=`<dom-module id="paper-item-shared-styles">
  <template>
    <style>
      :host, .paper-item {
        display: block;
        position: relative;
        min-height: var(--paper-item-min-height, 48px);
        padding: 0px 16px;
      }

      .paper-item {
        @apply --paper-font-subhead;
        border:none;
        outline: none;
        background: white;
        width: 100%;
        text-align: left;
      }

      :host([hidden]), .paper-item[hidden] {
        display: none !important;
      }

      :host(.iron-selected), .paper-item.iron-selected {
        font-weight: var(--paper-item-selected-weight, bold);

        @apply --paper-item-selected;
      }

      :host([disabled]), .paper-item[disabled] {
        color: var(--paper-item-disabled-color, var(--disabled-text-color));

        @apply --paper-item-disabled;
      }

      :host(:focus), .paper-item:focus {
        position: relative;
        outline: 0;

        @apply --paper-item-focused;
      }

      :host(:focus):before, .paper-item:focus:before {
        @apply --layout-fit;

        background: currentColor;
        content: '';
        opacity: var(--dark-divider-opacity);
        pointer-events: none;

        @apply --paper-item-focused-before;
      }
    </style>
  </template>
</dom-module>`;document.head.appendChild($_documentContainer.content)},157:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__(94);const IronIconClass=customElements.get("iron-icon");let loaded=!1;customElements.define("ha-icon",class extends IronIconClass{listen(...args){super.listen(...args);if(!loaded&&"mdi"===this._iconsetName){loaded=!0;__webpack_require__.e(47).then(__webpack_require__.bind(null,210))}}})},182:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.d(__webpack_exports__,"a",function(){return isComponentLoaded});function isComponentLoaded(hass,component){return hass&&-1!==hass.config.components.indexOf(component)}},194:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_polymer_polymer_legacy_js__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(3),_polymer_iron_flex_layout_iron_flex_layout_js__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(33),_polymer_paper_styles_typography_js__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(50),_paper_item_shared_styles_js__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(127),_polymer_polymer_lib_legacy_polymer_fn_js__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(4),_polymer_polymer_lib_utils_html_tag_js__WEBPACK_IMPORTED_MODULE_5__=__webpack_require__(1),_paper_item_behavior_js__WEBPACK_IMPORTED_MODULE_6__=__webpack_require__(105);/**
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
`,is:"paper-icon-item",behaviors:[_paper_item_behavior_js__WEBPACK_IMPORTED_MODULE_6__.a]})},707:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.r(__webpack_exports__);var _polymer_app_layout_app_toolbar_app_toolbar__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(107),_polymer_iron_flex_layout_iron_flex_layout_classes__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(79),_polymer_paper_icon_button_paper_icon_button__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(98),_polymer_paper_item_paper_icon_item__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(194),_polymer_paper_item_paper_item__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(125),_polymer_paper_listbox_paper_listbox__WEBPACK_IMPORTED_MODULE_5__=__webpack_require__(126),_polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_6__=__webpack_require__(1),_polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_7__=__webpack_require__(10),_ha_icon__WEBPACK_IMPORTED_MODULE_8__=__webpack_require__(157),_util_hass_translation__WEBPACK_IMPORTED_MODULE_9__=__webpack_require__(41),_mixins_localize_mixin__WEBPACK_IMPORTED_MODULE_10__=__webpack_require__(71),_common_config_is_component_loaded__WEBPACK_IMPORTED_MODULE_11__=__webpack_require__(182);class HaSidebar extends Object(_mixins_localize_mixin__WEBPACK_IMPORTED_MODULE_10__.a)(_polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_7__.a){static get template(){return _polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_6__.a`
    <style include="iron-flex iron-flex-alignment iron-positioning">
      :host {
        --sidebar-text: {
          color: var(--sidebar-text-color);
          font-weight: 500;
          font-size: 14px;
        };
        height: 100%;
        display: block;
        overflow: auto;
        -ms-user-select: none;
        -webkit-user-select: none;
        -moz-user-select: none;
        border-right: 1px solid var(--divider-color);
        background-color: var(--sidebar-background-color, var(--primary-background-color));
      }

      app-toolbar {
        font-weight: 400;
        color: var(--primary-text-color);
        border-bottom: 1px solid var(--divider-color);
        background-color: var(--primary-background-color);
      }

      app-toolbar a {
        color: var(--primary-text-color);
      }

      paper-listbox {
        padding: 0;
      }

      paper-listbox > a {
        @apply --sidebar-text;
        text-decoration: none;

        --paper-item-icon: {
          color: var(--sidebar-icon-color);
        };
      }

      paper-icon-item {
        margin: 8px;
        padding-left: 9px;
        border-radius: 4px;
        --paper-item-min-height: 40px;
      }

      .iron-selected paper-icon-item:before {
        border-radius: 4px;
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
        pointer-events: none;
        content: "";
        background-color: var(--sidebar-selected-icon-color);
        opacity: 0.12;
        transition: opacity 15ms linear;
        will-change: opacity;
      }

      .iron-selected paper-icon-item[pressed]:before {
        opacity: 0.37;
      }

      paper-icon-item span {
        @apply --sidebar-text;
      }

      a.iron-selected {
        --paper-item-icon: {
          color: var(--sidebar-selected-icon-color);
        };
      }

      a.iron-selected .item-text {
        color: var(--sidebar-selected-text-color);
      }

      paper-icon-item.logout {
        margin-top: 16px;
      }

      .divider {
        height: 1px;
        background-color: var(--divider-color);
        margin: 4px 0;
      }

      .subheader {
        @apply --sidebar-text;
        padding: 16px;
      }

      .dev-tools {
        padding: 0 8px;
      }

      .dev-tools a {
        color: var(--sidebar-icon-color);
      }

      .profile-badge {
        /* for ripple */
        position: relative;
        box-sizing: border-box;
        width: 40px;
        line-height: 40px;
        border-radius: 50%;
        text-align: center;
        background-color: var(--light-primary-color);
        text-decoration: none;
        color: var(--primary-text-color);
      }

      .profile-badge.long {
        font-size: 80%;
      }
    </style>

    <app-toolbar>
      <div main-title=>Home Assistant</div>
      <template is='dom-if' if='[[hass.user]]'>
        <a href='/profile' class$='[[_computeBadgeClass(_initials)]]'>
          <paper-ripple></paper-ripple>
          [[_initials]]
        </a>
      </template>
    </app-toolbar>

    <paper-listbox attr-for-selected="data-panel" selected="[[hass.panelUrl]]">
      <a href='[[_computeUrl(defaultPage)]]' data-panel$="[[defaultPage]]" tabindex="-1">
        <paper-icon-item>
          <ha-icon slot="item-icon" icon="hass:apps"></ha-icon>
          <span class="item-text">[[localize('panel.states')]]</span>
        </paper-icon-item>
      </a>

      <template is="dom-repeat" items="[[panels]]">
        <a href='[[_computeUrl(item.url_path)]]' data-panel$='[[item.url_path]]' tabindex="-1">
          <paper-icon-item>
            <ha-icon slot="item-icon" icon="[[item.icon]]"></ha-icon>
            <span class="item-text">[[_computePanelName(localize, item)]]</span>
          </paper-icon-item>
        </a>
      </template>

      <template is='dom-if' if='[[!hass.user]]'>
        <paper-icon-item on-click='_handleLogOut' class="logout">
          <ha-icon slot="item-icon" icon="hass:exit-to-app"></ha-icon>
          <span class="item-text">[[localize('ui.sidebar.log_out')]]</span>
        </paper-icon-item>
      </template>
    </paper-listbox>

    <div>
      <div class="divider"></div>

      <div class="subheader">[[localize('ui.sidebar.developer_tools')]]</div>

      <div class="dev-tools layout horizontal justified">
        <a href="/dev-service" tabindex="-1">
          <paper-icon-button
            icon="hass:remote"
            alt="[[localize('panel.dev-services')]]"
            title="[[localize('panel.dev-services')]]"
          ></paper-icon-button>
        </a>
        <a href="/dev-state" tabindex="-1">
          <paper-icon-button
            icon="hass:code-tags"
            alt="[[localize('panel.dev-states')]]"
            title="[[localize('panel.dev-states')]]"

          ></paper-icon-button>
        </a>
        <a href="/dev-event" tabindex="-1">
          <paper-icon-button
            icon="hass:radio-tower"
            alt="[[localize('panel.dev-events')]]"
            title="[[localize('panel.dev-events')]]"

          ></paper-icon-button>
        </a>
        <a href="/dev-template" tabindex="-1">
          <paper-icon-button
            icon="hass:file-xml"
            alt="[[localize('panel.dev-templates')]]"
            title="[[localize('panel.dev-templates')]]"

          ></paper-icon-button>
          </a>
        <template is="dom-if" if="[[_mqttLoaded(hass)]]">
          <a href="/dev-mqtt" tabindex="-1">
            <paper-icon-button
              icon="hass:altimeter"
              alt="[[localize('panel.dev-mqtt')]]"
              title="[[localize('panel.dev-mqtt')]]"

            ></paper-icon-button>
          </a>
        </template>
        <a href="/dev-info" tabindex="-1">
          <paper-icon-button
            icon="hass:information-outline"
            alt="[[localize('panel.dev-info')]]"
            title="[[localize('panel.dev-info')]]"
          ></paper-icon-button>
        </a>
      </div>
    </div>
`}static get properties(){return{hass:{type:Object},menuShown:{type:Boolean},menuSelected:{type:String},narrow:Boolean,panels:{type:Array,computed:"computePanels(hass)"},defaultPage:String,_initials:{type:String,computed:"_computeUserInitials(hass.user.name)"}}}_computeUserInitials(name){if(!name)return"user";return name.trim().split(" ").slice(0,3).map(s=>s.substr(0,1)).join("")}_computeBadgeClass(initials){return`profile-badge ${2<initials.length?"long":""}`}_mqttLoaded(hass){return Object(_common_config_is_component_loaded__WEBPACK_IMPORTED_MODULE_11__.a)(hass,"mqtt")}_computeUserName(user){return user&&(user.name||"Unnamed User")}_computePanelName(localize,panel){return localize(`panel.${panel.title}`)||panel.title}computePanels(hass){var panels=hass.panels,sortValue={map:1,logbook:2,history:3},result=[];Object.keys(panels).forEach(function(key){if(panels[key].title){result.push(panels[key])}});result.sort(function(a,b){var aBuiltIn=a.component_name in sortValue,bBuiltIn=b.component_name in sortValue;if(aBuiltIn&&bBuiltIn){return sortValue[a.component_name]-sortValue[b.component_name]}if(aBuiltIn){return-1}if(bBuiltIn){return 1}if(a.title<b.title){return-1}if(a.title>b.title){return 1}return 0});return result}_computeUrl(urlPath){return`/${urlPath}`}_handleLogOut(){this.fire("hass-logout")}}customElements.define("ha-sidebar",HaSidebar)}}]);
//# sourceMappingURL=f3a080af80997d50bd16.chunk.js.map
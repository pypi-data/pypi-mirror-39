(window.webpackJsonp=window.webpackJsonp||[]).push([[62],{230:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_polymer_polymer_legacy_js__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(3),_polymer_iron_flex_layout_iron_flex_layout_js__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(33),_polymer_iron_icon_iron_icon_js__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(95),_polymer_paper_styles_element_styles_paper_material_styles_js__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(82),_polymer_paper_styles_color_js__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(58),_polymer_paper_styles_color_js__WEBPACK_IMPORTED_MODULE_4___default=__webpack_require__.n(_polymer_paper_styles_color_js__WEBPACK_IMPORTED_MODULE_4__),_polymer_paper_styles_default_theme_js__WEBPACK_IMPORTED_MODULE_5__=__webpack_require__(39),_polymer_paper_behaviors_paper_button_behavior_js__WEBPACK_IMPORTED_MODULE_6__=__webpack_require__(56),_polymer_polymer_lib_legacy_polymer_fn_js__WEBPACK_IMPORTED_MODULE_7__=__webpack_require__(4),_polymer_polymer_lib_utils_html_tag_js__WEBPACK_IMPORTED_MODULE_8__=__webpack_require__(1);/**
@license
Copyright (c) 2015 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at
http://polymer.github.io/LICENSE.txt The complete set of authors may be found at
http://polymer.github.io/AUTHORS.txt The complete set of contributors may be
found at http://polymer.github.io/CONTRIBUTORS.txt Code distributed by Google as
part of the polymer project is also subject to an additional IP rights grant
found at http://polymer.github.io/PATENTS.txt
*/const template=_polymer_polymer_lib_utils_html_tag_js__WEBPACK_IMPORTED_MODULE_8__.a`
  <style include="paper-material-styles">
    :host {
      @apply --layout-vertical;
      @apply --layout-center-center;

      background: var(--paper-fab-background, var(--accent-color));
      border-radius: 50%;
      box-sizing: border-box;
      color: var(--text-primary-color);
      cursor: pointer;
      height: 56px;
      min-width: 0;
      outline: none;
      padding: 16px;
      position: relative;
      -moz-user-select: none;
      -ms-user-select: none;
      -webkit-user-select: none;
      user-select: none;
      width: 56px;
      z-index: 0;

      /* NOTE: Both values are needed, since some phones require the value \`transparent\`. */
      -webkit-tap-highlight-color: rgba(0,0,0,0);
      -webkit-tap-highlight-color: transparent;

      @apply --paper-fab;
    }

    [hidden] {
      display: none !important;
    }

    :host([mini]) {
      width: 40px;
      height: 40px;
      padding: 8px;

      @apply --paper-fab-mini;
    }

    :host([disabled]) {
      color: var(--paper-fab-disabled-text, var(--paper-grey-500));
      background: var(--paper-fab-disabled-background, var(--paper-grey-300));

      @apply --paper-fab-disabled;
    }

    iron-icon {
      @apply --paper-fab-iron-icon;
    }

    span {
      width: 100%;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      text-align: center;

      @apply --paper-fab-label;
    }

    :host(.keyboard-focus) {
      background: var(--paper-fab-keyboard-focus-background, var(--paper-pink-900));
    }

    :host([elevation="1"]) {
      @apply --paper-material-elevation-1;
    }

    :host([elevation="2"]) {
      @apply --paper-material-elevation-2;
    }

    :host([elevation="3"]) {
      @apply --paper-material-elevation-3;
    }

    :host([elevation="4"]) {
      @apply --paper-material-elevation-4;
    }

    :host([elevation="5"]) {
      @apply --paper-material-elevation-5;
    }
  </style>

  <iron-icon id="icon" hidden\$="{{!_computeIsIconFab(icon, src)}}" src="[[src]]" icon="[[icon]]"></iron-icon>
  <span hidden\$="{{_computeIsIconFab(icon, src)}}">{{label}}</span>
`;template.setAttribute("strip-whitespace","");Object(_polymer_polymer_lib_legacy_polymer_fn_js__WEBPACK_IMPORTED_MODULE_7__.a)({_template:template,is:"paper-fab",behaviors:[_polymer_paper_behaviors_paper_button_behavior_js__WEBPACK_IMPORTED_MODULE_6__.a],properties:{src:{type:String,value:""},icon:{type:String,value:""},mini:{type:Boolean,value:!1,reflectToAttribute:!0},label:{type:String,observer:"_labelChanged"}},_labelChanged:function(){this.setAttribute("aria-label",this.label)},_computeIsIconFab:function(icon,src){return 0<icon.length||0<src.length}})},253:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.d(__webpack_exports__,"a",function(){return addCard});__webpack_require__.d(__webpack_exports__,"f",function(){return replaceCard});__webpack_require__.d(__webpack_exports__,"c",function(){return deleteCard});__webpack_require__.d(__webpack_exports__,"h",function(){return swapCard});__webpack_require__.d(__webpack_exports__,"e",function(){return moveCard});__webpack_require__.d(__webpack_exports__,"b",function(){return addView});__webpack_require__.d(__webpack_exports__,"g",function(){return replaceView});__webpack_require__.d(__webpack_exports__,"d",function(){return deleteView});const addCard=(config,path,cardConfig)=>{const[viewIndex]=path,views=[];config.views.forEach((viewConf,index)=>{if(index!==viewIndex){views.push(config.views[index]);return}const cards=viewConf.cards?[...viewConf.cards,cardConfig]:[cardConfig];views.push(Object.assign({},viewConf,{cards}))});return Object.assign({},config,{views})},replaceCard=(config,path,cardConfig)=>{const[viewIndex,cardIndex]=path,views=[];config.views.forEach((viewConf,index)=>{if(index!==viewIndex){views.push(config.views[index]);return}views.push(Object.assign({},viewConf,{cards:(viewConf.cards||[]).map((origConf,ind)=>ind===cardIndex?cardConfig:origConf)}))});return Object.assign({},config,{views})},deleteCard=(config,path)=>{const[viewIndex,cardIndex]=path,views=[];config.views.forEach((viewConf,index)=>{if(index!==viewIndex){views.push(config.views[index]);return}views.push(Object.assign({},viewConf,{cards:(viewConf.cards||[]).filter((_origConf,ind)=>ind!==cardIndex)}))});return Object.assign({},config,{views})},swapCard=(config,path1,path2)=>{const card1=config.views[path1[0]].cards[path1[1]],card2=config.views[path2[0]].cards[path2[1]],origView1=config.views[path1[0]],newView1=Object.assign({},origView1,{cards:origView1.cards.map((origCard,index)=>index===path1[1]?card2:origCard)}),origView2=path1[0]===path2[0]?newView1:config.views[path2[0]],newView2=Object.assign({},origView2,{cards:origView2.cards.map((origCard,index)=>index===path2[1]?card1:origCard)});return Object.assign({},config,{views:config.views.map((origView,index)=>index===path2[0]?newView2:index===path1[0]?newView1:origView)})},moveCard=(config,fromPath,toPath)=>{if(fromPath[0]===toPath[0]){throw new Error("You can not move a card to the view it is in.")}const fromView=config.views[fromPath[0]],card=fromView.cards[fromPath[1]],newView1=Object.assign({},fromView,{cards:(fromView.cards||[]).filter((_origConf,ind)=>ind!==fromPath[1])}),toView=config.views[toPath[0]],cards=toView.cards?[...toView.cards,card]:[card],newView2=Object.assign({},toView,{cards});return Object.assign({},config,{views:config.views.map((origView,index)=>index===toPath[0]?newView2:index===fromPath[0]?newView1:origView)})},addView=(config,viewConfig)=>Object.assign({},config,{views:config.views.concat(viewConfig)}),replaceView=(config,viewIndex,viewConfig)=>Object.assign({},config,{views:config.views.map((origView,index)=>index===viewIndex?viewConfig:origView)}),deleteView=(config,viewIndex)=>Object.assign({},config,{views:config.views.filter((_origView,index)=>index!==viewIndex)})},751:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.r(__webpack_exports__);var paper_fab=__webpack_require__(230),lit_element=__webpack_require__(57),paper_button=__webpack_require__(72),paper_menu_button=__webpack_require__(130),paper_icon_button=__webpack_require__(99),paper_listbox=__webpack_require__(128),show_edit_card_dialog=__webpack_require__(375),lit_localize_mixin=__webpack_require__(154),config_util=__webpack_require__(253);async function confDeleteCard(lovelace,path){if(!confirm("Are you sure you want to delete this card?")){return}try{await lovelace.saveConfig(Object(config_util.c)(lovelace.config,path))}catch(err){alert(`Deleting failed: ${err.message}`)}}var fire_event=__webpack_require__(65);let registeredDialog=!1;const registerEditCardDialog=element=>Object(fire_event.a)(element,"register-dialog",{dialogShowEvent:"show-move-card-view",dialogTag:"hui-dialog-move-card-view",dialogImport:()=>__webpack_require__.e(89).then(__webpack_require__.bind(null,747))}),showMoveCardViewDialog=(element,moveCardViewDialogParams)=>{if(!registeredDialog){registeredDialog=!0;registerEditCardDialog(element)}Object(fire_event.a)(element,"show-move-card-view",moveCardViewDialogParams)};class hui_card_options_HuiCardOptions extends Object(lit_localize_mixin.a)(lit_element.a){static get properties(){return{hass:{},lovelace:{},path:{}}}render(){return lit_element.c`
      <style>
        div.options {
          border-top: 1px solid #e8e8e8;
          padding: 5px 8px;
          background: var(--paper-card-background-color, white);
          box-shadow: rgba(0, 0, 0, 0.14) 0px 2px 2px 0px,
            rgba(0, 0, 0, 0.12) 0px 1px 5px -4px,
            rgba(0, 0, 0, 0.2) 0px 3px 1px -2px;
          display: flex;
        }
        div.options .primary-actions {
          flex: 1;
          margin: auto;
        }
        div.options .secondary-actions {
          flex: 4;
          text-align: right;
        }
        paper-button {
          color: var(--primary-color);
          font-weight: 500;
          letter-spacing: 0.05em;
          font-size: 16px;
          padding: 0;
          margin: 0;
        }
        paper-icon-button {
          color: var(--primary-text-color);
        }
        paper-icon-button.move-arrow[disabled] {
          color: var(--disabled-text-color);
        }
        paper-menu-button {
          color: var(--secondary-text-color);
          padding: 0;
        }
        paper-item.header {
          color: var(--primary-text-color);
          text-transform: uppercase;
          font-weight: 500;
          font-size: 14px;
        }
        paper-item {
          cursor: pointer;
        }
      </style>
      <slot></slot>
      <div class="options">
        <div class="primary-actions">
          <paper-button @click="${this._editCard}"
            >${this.localize("ui.panel.lovelace.editor.edit_card.edit")}</paper-button
          >
        </div>
        <div class="secondary-actions">
          <paper-icon-button
            title="Move card down"
            class="move-arrow"
            icon="hass:arrow-down"
            @click="${this._cardDown}"
            ?disabled="${this.lovelace.config.views[this.path[0]].cards.length===this.path[1]+1}"
          ></paper-icon-button>
          <paper-icon-button
            title="Move card up"
            class="move-arrow"
            icon="hass:arrow-up"
            @click="${this._cardUp}"
            ?disabled="${0===this.path[1]}"
          ></paper-icon-button>
          <paper-menu-button>
            <paper-icon-button
              icon="hass:dots-vertical"
              slot="dropdown-trigger"
            ></paper-icon-button>
            <paper-listbox slot="dropdown-content">
              <paper-item @click="${this._moveCard}">Move Card</paper-item>
              <paper-item @click="${this._deleteCard}"
                >${this.localize("ui.panel.lovelace.editor.edit_card.delete")}</paper-item
              >
            </paper-listbox>
          </paper-menu-button>
        </div>
      </div>
    `}_editCard(){Object(show_edit_card_dialog.a)(this,{lovelace:this.lovelace,path:this.path})}_cardUp(){const lovelace=this.lovelace,path=this.path;lovelace.saveConfig(Object(config_util.h)(lovelace.config,path,[path[0],path[1]-1]))}_cardDown(){const lovelace=this.lovelace,path=this.path;lovelace.saveConfig(Object(config_util.h)(lovelace.config,path,[path[0],path[1]+1]))}_moveCard(){showMoveCardViewDialog(this,{path:this.path,lovelace:this.lovelace})}_deleteCard(){confDeleteCard(this.lovelace,this.path)}}customElements.define("hui-card-options",hui_card_options_HuiCardOptions)}}]);
//# sourceMappingURL=6fad67b3ff719efc28a5.chunk.js.map
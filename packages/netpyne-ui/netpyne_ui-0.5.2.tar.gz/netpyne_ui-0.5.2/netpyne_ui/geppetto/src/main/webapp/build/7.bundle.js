webpackJsonp([7],{

/***/ 1645:
/***/ (function(module, exports, __webpack_require__) {

var __WEBPACK_AMD_DEFINE_RESULT__;!(__WEBPACK_AMD_DEFINE_RESULT__ = function (require) {

    __webpack_require__(3267);

    var React = __webpack_require__(0);

    var SpotlightButton = __webpack_require__(3269);
    var ControlPanelButton = __webpack_require__(3270);
    var QueryBuilderButton = __webpack_require__(3271);
    var TutorialButton = __webpack_require__(3272);

    var GEPPETTO = __webpack_require__(99);

    var ForegroundControls = React.createClass({
        displayName: 'ForegroundControls',


        getInitialState: function getInitialState() {
            return {
                disableSpotlight: false,
                showDropDown: false
            };
        },

        componentDidMount: function componentDidMount() {},

        componentWillMount: function componentWillMount() {
            GEPPETTO.ForegroundControls = this;
        },

        refresh: function refresh() {
            this.forceUpdate();
        },

        render: function render() {
            var spotlightBtn = GEPPETTO.Spotlight != undefined ? React.createFactory(SpotlightButton)({ disabled: this.state.disableSpotlight }) : '';
            var controlPanelBtn = GEPPETTO.ControlPanel != undefined ? React.createFactory(ControlPanelButton)({}) : '';

            var queryBuilderBtn = GEPPETTO.QueryBuilder != undefined ? React.createFactory(QueryBuilderButton)({}) : '';

            var tutorialBtn = GEPPETTO.Tutorial != undefined ? React.createFactory(TutorialButton)({}) : '';

            return React.createElement(
                'div',
                { className: 'foreground-controls' },
                controlPanelBtn,
                React.createElement('br', null),
                spotlightBtn,
                queryBuilderBtn == "" ? '' : React.createElement('br', null),
                queryBuilderBtn,
                React.createElement('br', null),
                tutorialBtn
            );
        }
    });

    return ForegroundControls;
}.call(exports, __webpack_require__, exports, module),
				__WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));

/***/ }),

/***/ 1712:
/***/ (function(module, exports, __webpack_require__) {

var __WEBPACK_AMD_DEFINE_RESULT__;!(__WEBPACK_AMD_DEFINE_RESULT__ = function (require) {
    /**
     * Button used as part of GEPPETTO Components
     *
     * @mixin Button
     */
    var React = __webpack_require__(0);

    return {
        displayName: 'Button',

        render: function render() {
            return React.DOM.button({
                type: 'button',
                id: this.props.id,
                className: 'btn ' + this.props.className + (this.props.hidden === true ? ' hiddenElement' : ''),
                'data-toggle': this.props['data-toggle'],
                onClick: this.props.onClick,
                disabled: this.props.disabled,
                icon: this.props.icon
            }, React.DOM.i({ className: this.props.icon }), " " + this.props.label);
        }
    };
}.call(exports, __webpack_require__, exports, module),
				__WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));

/***/ }),

/***/ 3267:
/***/ (function(module, exports, __webpack_require__) {

// style-loader: Adds some css to the DOM by adding a <style> tag

// load the styles
var content = __webpack_require__(3268);
if(typeof content === 'string') content = [[module.i, content, '']];
// add the styles to the DOM
var update = __webpack_require__(27)(content, {});
if(content.locals) module.exports = content.locals;
// Hot Module Replacement
if(false) {
	// When the styles change, update the <style> tags
	if(!content.locals) {
		module.hot.accept("!!../../../../node_modules/css-loader/index.js!../../../../node_modules/less-loader/dist/cjs.js?{\"modifyVars\":{\"url\":\"'../../../extensions/geppetto-netpyne/css/colors'\"}}!./ForegroundControls.less", function() {
			var newContent = require("!!../../../../node_modules/css-loader/index.js!../../../../node_modules/less-loader/dist/cjs.js?{\"modifyVars\":{\"url\":\"'../../../extensions/geppetto-netpyne/css/colors'\"}}!./ForegroundControls.less");
			if(typeof newContent === 'string') newContent = [[module.id, newContent, '']];
			update(newContent);
		});
	}
	// When the module is disposed, remove the <style> tags
	module.hot.dispose(function() { update(); });
}

/***/ }),

/***/ 3268:
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__(26)(undefined);
// imports


// module
exports.push([module.i, "#foreground-toolbar {\n  position: fixed;\n  left: 52px;\n  top: 320px;\n}\n.foreground-controls button {\n  border: none;\n  width: 24px;\n  height: 24px;\n  padding: 1px;\n  margin-bottom: 4px;\n}\n", ""]);

// exports


/***/ }),

/***/ 3269:
/***/ (function(module, exports, __webpack_require__) {

var __WEBPACK_AMD_DEFINE_RESULT__;!(__WEBPACK_AMD_DEFINE_RESULT__ = function (require) {

    var React = __webpack_require__(0),
        GEPPETTO = __webpack_require__(99);

    return React.createClass({
        mixins: [__webpack_require__(1712)],

        componentDidMount: function componentDidMount() {},

        getDefaultProps: function getDefaultProps() {
            return {
                label: '',
                id: 'spotlightBtn',
                className: 'squareB',
                icon: 'fa fa-search',
                onClick: function onClick() {
                    if (GEPPETTO.Spotlight != undefined) {
                        GEPPETTO.trigger('spin_logo');
                        GEPPETTO.Spotlight.open(GEPPETTO.Resources.SEARCH_FLOW);
                        GEPPETTO.trigger('stop_spin_logo');
                    }
                }
            };
        }

    });
}.call(exports, __webpack_require__, exports, module),
				__WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));

/***/ }),

/***/ 3270:
/***/ (function(module, exports, __webpack_require__) {

var __WEBPACK_AMD_DEFINE_RESULT__;!(__WEBPACK_AMD_DEFINE_RESULT__ = function (require) {

    var React = __webpack_require__(0),
        GEPPETTO = __webpack_require__(99);

    return React.createClass({
        mixins: [__webpack_require__(1712)],

        componentDidMount: function componentDidMount() {},

        getDefaultProps: function getDefaultProps() {
            return {
                label: '',
                id: 'controlPanelBtn',
                className: 'squareB',
                icon: 'fa fa-list',
                onClick: function onClick() {
                    GEPPETTO.ControlPanel.open();
                }
            };
        }

    });
}.call(exports, __webpack_require__, exports, module),
				__WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));

/***/ }),

/***/ 3271:
/***/ (function(module, exports, __webpack_require__) {

var __WEBPACK_AMD_DEFINE_RESULT__;!(__WEBPACK_AMD_DEFINE_RESULT__ = function (require) {

    var React = __webpack_require__(0),
        GEPPETTO = __webpack_require__(99);

    return React.createClass({
        mixins: [__webpack_require__(1712)],

        componentDidMount: function componentDidMount() {},

        getDefaultProps: function getDefaultProps() {
            return {
                label: '',
                id: 'queryBuilderBtn',
                className: 'squareB',
                icon: 'fa fa-cogs',
                onClick: function onClick() {
                    GEPPETTO.QueryBuilder.open();
                }
            };
        }

    });
}.call(exports, __webpack_require__, exports, module),
				__WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));

/***/ }),

/***/ 3272:
/***/ (function(module, exports, __webpack_require__) {

var __WEBPACK_AMD_DEFINE_RESULT__;!(__WEBPACK_AMD_DEFINE_RESULT__ = function (require) {

    var React = __webpack_require__(0),
        GEPPETTO = __webpack_require__(99);

    return React.createClass({
        mixins: [__webpack_require__(1712)],

        componentDidMount: function componentDidMount() {},

        getDefaultProps: function getDefaultProps() {
            return {
                label: '',
                id: 'tutorialBtn',
                className: 'squareB',
                icon: 'fa fa-leanpub',
                onClick: function onClick() {
                    GEPPETTO.CommandController.execute("G.toggleTutorial()", true);
                }
            };
        }
    });
}.call(exports, __webpack_require__, exports, module),
				__WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));

/***/ })

});
//# sourceMappingURL=7.bundle.js.map
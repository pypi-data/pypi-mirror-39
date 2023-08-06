webpackJsonp([46],{

/***/ 1630:
/***/ (function(module, exports, __webpack_require__) {

var __WEBPACK_AMD_DEFINE_RESULT__;var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

!(__WEBPACK_AMD_DEFINE_RESULT__ = function (require) {

	var React = __webpack_require__(0);
	__webpack_require__(3251);
	var defaultChildStyle = { 'alignSelf': 'auto', 'flexGrow': 0, 'order': 0 };

	var AbstractComponent = __webpack_require__(271);

	return function (_AbstractComponent) {
		_inherits(Panel, _AbstractComponent);

		function Panel(props) {
			_classCallCheck(this, Panel);

			var _this = _possibleConstructorReturn(this, (Panel.__proto__ || Object.getPrototypeOf(Panel)).call(this, props));

			var defaultParentStyle = { 'flexDirection': 'column', 'justifyContent': 'flex-start', 'alignItems': 'flex-start', 'flexWrap': 'nowrap', 'alignContent': 'flex-start', 'display': 'flex' };
			_this.state = {
				parentStyle: $.extend(defaultParentStyle, _this.props.parentStyle),
				items: _this.props.items
			};
			return _this;
		}

		_createClass(Panel, [{
			key: 'addChildren',
			value: function addChildren(items) {
				this.setState({ items: this.state.items.concat(items) });
			}
		}, {
			key: 'setChildren',
			value: function setChildren(items) {
				this.setState({ items: items });
			}
		}, {
			key: 'componentWillReceiveProps',
			value: function componentWillReceiveProps(nextProps) {
				this.setState({
					items: nextProps.items
				});
			}
		}, {
			key: 'setDirection',
			value: function setDirection(direction) {
				var currentStyle = this.state.parentStyle;
				currentStyle['flexDirection'] = direction;
				this.setState({ parentStyle: currentStyle });
			}
		}, {
			key: 'componentDidMount',
			value: function componentDidMount() {
				var comp = $('#' + this.props.id);
				if (comp.parent().hasClass('dialog')) {
					comp.parent().height(comp.height() + 10);
					comp.parent().parent().width(comp.width() + 70);
				}
			}
		}, {
			key: 'render',
			value: function render() {
				var itemComponents = this.state.items.map(function (item) {
					return React.createElement(
						'div',
						{ key: item.props.id, style: defaultChildStyle },
						item
					);
				});

				return React.createElement(
					'div',
					{ className: 'panelContainer material', id: this.props.id, style: this.state.parentStyle },
					itemComponents
				);
			}
		}]);

		return Panel;
	}(AbstractComponent);
}.call(exports, __webpack_require__, exports, module),
				__WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));

/***/ }),

/***/ 3251:
/***/ (function(module, exports, __webpack_require__) {

// style-loader: Adds some css to the DOM by adding a <style> tag

// load the styles
var content = __webpack_require__(3252);
if(typeof content === 'string') content = [[module.i, content, '']];
// add the styles to the DOM
var update = __webpack_require__(28)(content, {});
if(content.locals) module.exports = content.locals;
// Hot Module Replacement
if(false) {
	// When the styles change, update the <style> tags
	if(!content.locals) {
		module.hot.accept("!!../../../../node_modules/css-loader/index.js!../../../../node_modules/less-loader/dist/cjs.js?{\"modifyVars\":{\"url\":\"'../../../extensions/geppetto-netpyne/css/colors'\"}}!./Panel.less", function() {
			var newContent = require("!!../../../../node_modules/css-loader/index.js!../../../../node_modules/less-loader/dist/cjs.js?{\"modifyVars\":{\"url\":\"'../../../extensions/geppetto-netpyne/css/colors'\"}}!./Panel.less");
			if(typeof newContent === 'string') newContent = [[module.id, newContent, '']];
			update(newContent);
		});
	}
	// When the module is disposed, remove the <style> tags
	module.hot.dispose(function() { update(); });
}

/***/ }),

/***/ 3252:
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__(27)(undefined);
// imports


// module
exports.push([module.i, ".box {\n  box-sizing: border-box;\n  background: #fff;\n  border: 1px solid #999;\n  border-radius: 3px;\n  width: 180px;\n  height: 180px;\n  margin: 10px;\n  padding: 10px;\n  float: left;\n}\n.react-draggable {\n  cursor: move;\n}\n.react-draggable strong {\n  background: #ddd;\n  border: 1px solid #999;\n  border-radius: 3px;\n  display: block;\n  margin-bottom: 10px;\n  padding: 3px 5px;\n  text-align: center;\n}\n.cursor {\n  cursor: move;\n}\n.no-cursor {\n  cursor: auto;\n}\n.cursor-y {\n  cursor: ns-resize;\n}\n.cursor-x {\n  cursor: ew-resize;\n}\n", ""]);

// exports


/***/ })

});
//# sourceMappingURL=46.bundle.js.map
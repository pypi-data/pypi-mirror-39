webpackJsonp([34],{

/***/ 1310:
/***/ (function(module, exports, __webpack_require__) {

// style-loader: Adds some css to the DOM by adding a <style> tag

// load the styles
var content = __webpack_require__(1311);
if(typeof content === 'string') content = [[module.i, content, '']];
// add the styles to the DOM
var update = __webpack_require__(26)(content, {});
if(content.locals) module.exports = content.locals;
// Hot Module Replacement
if(false) {
	// When the styles change, update the <style> tags
	if(!content.locals) {
		module.hot.accept("!!../../../../node_modules/css-loader/index.js!../../../../node_modules/less-loader/dist/cjs.js?{\"modifyVars\":{\"url\":\"'../../../extensions/geppetto-netpyne/css/colors'\"}}!./PythonConsole.less", function() {
			var newContent = require("!!../../../../node_modules/css-loader/index.js!../../../../node_modules/less-loader/dist/cjs.js?{\"modifyVars\":{\"url\":\"'../../../extensions/geppetto-netpyne/css/colors'\"}}!./PythonConsole.less");
			if(typeof newContent === 'string') newContent = [[module.id, newContent, '']];
			update(newContent);
		});
	}
	// When the module is disposed, remove the <style> tags
	module.hot.dispose(function() { update(); });
}

/***/ }),

/***/ 1311:
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__(25)(undefined);
// imports


// module
exports.push([module.i, ".dark-orange {\n  color: #cc215a;\n}\n.orange {\n  color: #f23d7a;\n}\n.orange-color {\n  color: #f23d7a;\n}\n.orange-color-bg {\n  background-color: #f23d7a;\n}\n#pythonConsoleButton {\n  margin: 0 auto;\n  margin-bottom: 26px;\n  position: relative;\n  border-width: 1px;\n  border-bottom: 0;\n  border-left: 0;\n  border-style: solid;\n  box-shadow: none;\n  cursor: pointer;\n  text-shadow: none;\n  width: 140px;\n  height: 35px;\n  z-index: 3;\n}\n#pythonConsoleButton > a::-moz-focus-inner {\n  border: 0;\n}\n#pythonConsoleButton .glyphicon {\n  font-size: 50px;\n}\n#pythonConsole {\n  background: #ffffff !important;\n  color: #ccc;\n  height: 250px;\n  width: 100%;\n  max-height: 100%;\n  padding: 0px;\n  border: 0;\n  top: 0px;\n  z-index: 1;\n  margin-bottom: 0px;\n  cursor: pointer;\n  border-radius: 0;\n}\n#pythonConsoleOutput {\n  width: 100%;\n  height: 100%;\n}\n", ""]);

// exports


/***/ }),

/***/ 352:
/***/ (function(module, exports, __webpack_require__) {

var __WEBPACK_AMD_DEFINE_RESULT__;/**
 * React component for displaying a Python console.
 *
 * @author Adrian Quintana (adrian@metacell.us)
 * @author Dario Del Piano
 */
!(__WEBPACK_AMD_DEFINE_RESULT__ = function (require) {

    var React = __webpack_require__(0);
    __webpack_require__(1310);
    $.widget.bridge('uitooltip', $.ui.tooltip);

    return React.createClass({
        render: function render() {

            return React.createElement(
                'div',
                { className: 'col-lg-6 panel-body', id: 'pythonConsoleOutput' },
                React.createElement('iframe', { id: 'pythonConsoleFrame', src: this.props["pythonNotebookPath"], marginWidth: '0',
                    marginHeight: '0', frameBorder: 'no', scrolling: 'yes',
                    allowTransparency: 'true',
                    style: { width: '100%',
                        height: this.props.iframeHeight + 'px' } })
            );
        }
    });
}.call(exports, __webpack_require__, exports, module),
				__WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));

/***/ })

});
//# sourceMappingURL=34.bundle.js.map
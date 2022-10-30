/* *
 *
 *  (c) 2009-2021 Øystein Moseng
 *
 *  Main keyboard navigation handling.
 *
 *  License: www.highcharts.com/license
 *
 *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
 *
 * */
'use strict';
import H from '../Core/Globals.js';
var doc = H.doc, win = H.win;
import MenuComponent from './Components/MenuComponent.js';
import U from '../Core/Utilities.js';
var addEvent = U.addEvent, fireEvent = U.fireEvent;
import EventProvider from './Utils/EventProvider.js';
import HTMLUtilities from './Utils/HTMLUtilities.js';
var getElement = HTMLUtilities.getElement;
/* *
 *
 *  Class
 *
 * */
/**
 * The KeyboardNavigation class, containing the overall keyboard navigation
 * logic for the chart.
 *
 * @requires module:modules/accessibility
 *
 * @private
 * @class
 * @param {Highcharts.Chart} chart
 *        Chart object
 * @param {object} components
 *        Map of component names to AccessibilityComponent objects.
 * @name Highcharts.KeyboardNavigation
 */
var KeyboardNavigation = /** @class */ (function () {
    /* *
     *
     *  Constructor
     *
     * */
    function KeyboardNavigation(chart, components) {
        /* *
         *
         *  Properties
         *
         * */
        this.chart = void 0;
        this.components = void 0;
        this.currentModuleIx = NaN;
        this.eventProvider = void 0;
        this.exitAnchor = void 0;
        this.modules = [];
        this.tabindexContainer = void 0;
        this.init(chart, components);
    }
    /* *
     *
     *  Functions
     *
     * */
    /* eslint-disable valid-jsdoc */
    /**
     * Initialize the class
     * @private
     * @param {Highcharts.Chart} chart
     *        Chart object
     * @param {object} components
     *        Map of component names to AccessibilityComponent objects.
     */
    KeyboardNavigation.prototype.init = function (chart, components) {
        var _this = this;
        var ep = this.eventProvider = new EventProvider();
        this.chart = chart;
        this.components = components;
        this.modules = [];
        this.currentModuleIx = 0;
        this.update();
        ep.addEvent(this.tabindexContainer, 'keydown', function (e) { return _this.onKeydown(e); });
        ep.addEvent(this.tabindexContainer, 'focus', function (e) { return _this.onFocus(e); });
        ['mouseup', 'touchend'].forEach(function (eventName) {
            return ep.addEvent(doc, eventName, function () { return _this.onMouseUp(); });
        });
        ['mousedown', 'touchstart'].forEach(function (eventName) {
            return ep.addEvent(chart.renderTo, eventName, function () {
                _this.isClickingChart = true;
            });
        });
        ep.addEvent(chart.renderTo, 'mouseover', function () {
            _this.pointerIsOverChart = true;
        });
        ep.addEvent(chart.renderTo, 'mouseout', function () {
            _this.pointerIsOverChart = false;
        });
    };
    /**
     * Update the modules for the keyboard navigation.
     * @param {Array<string>} [order]
     *        Array specifying the tab order of the components.
     */
    KeyboardNavigation.prototype.update = function (order) {
        var a11yOptions = this.chart.options.accessibility, keyboardOptions = a11yOptions && a11yOptions.keyboardNavigation, components = this.components;
        this.updateContainerTabindex();
        if (keyboardOptions &&
            keyboardOptions.enabled &&
            order &&
            order.length) {
            // We (still) have keyboard navigation. Update module list
            this.modules = order.reduce(function (modules, componentName) {
                var navModules = components[componentName].getKeyboardNavigation();
                return modules.concat(navModules);
            }, []);
            this.updateExitAnchor();
        }
        else {
            this.modules = [];
            this.currentModuleIx = 0;
            this.removeExitAnchor();
        }
    };
    /**
     * Function to run on container focus
     * @private
     * @param {global.FocusEvent} e Browser focus event.
     */
    KeyboardNavigation.prototype.onFocus = function (e) {
        var chart = this.chart;
        var focusComesFromChart = (e.relatedTarget &&
            chart.container.contains(e.relatedTarget));
        // Init keyboard nav if tabbing into chart
        if (!this.exiting &&
            !this.tabbingInBackwards &&
            !this.isClickingChart &&
            !focusComesFromChart &&
            this.modules[0]) {
            this.modules[0].init(1);
        }
        this.exiting = false;
    };
    /**
     * Reset chart navigation state if we click outside the chart and it's
     * not already reset.
     * @private
     */
    KeyboardNavigation.prototype.onMouseUp = function () {
        delete this.isClickingChart;
        if (!this.keyboardReset && !this.pointerIsOverChart) {
            var chart = this.chart, curMod = this.modules &&
                this.modules[this.currentModuleIx || 0];
            if (curMod && curMod.terminate) {
                curMod.terminate();
            }
            if (chart.focusElement) {
                chart.focusElement.removeFocusBorder();
            }
            this.currentModuleIx = 0;
            this.keyboardReset = true;
        }
    };
    /**
     * Function to run on keydown
     * @private
     * @param {global.KeyboardEvent} ev Browser keydown event.
     */
    KeyboardNavigation.prototype.onKeydown = function (ev) {
        var e = ev || win.event, curNavModule = (this.modules &&
            this.modules.length &&
            this.modules[this.currentModuleIx]);
        var preventDefault;
        // Used for resetting nav state when clicking outside chart
        this.keyboardReset = false;
        // Used for sending focus out of the chart by the modules.
        this.exiting = false;
        // If there is a nav module for the current index, run it.
        // Otherwise, we are outside of the chart in some direction.
        if (curNavModule) {
            var response = curNavModule.run(e);
            if (response === curNavModule.response.success) {
                preventDefault = true;
            }
            else if (response === curNavModule.response.prev) {
                preventDefault = this.prev();
            }
            else if (response === curNavModule.response.next) {
                preventDefault = this.next();
            }
            if (preventDefault) {
                e.preventDefault();
                e.stopPropagation();
            }
        }
    };
    /**
     * Go to previous module.
     * @private
     */
    KeyboardNavigation.prototype.prev = function () {
        return this.move(-1);
    };
    /**
     * Go to next module.
     * @private
     */
    KeyboardNavigation.prototype.next = function () {
        return this.move(1);
    };
    /**
     * Move to prev/next module.
     * @private
     * @param {number} direction
     * Direction to move. +1 for next, -1 for prev.
     * @return {boolean}
     * True if there was a valid module in direction.
     */
    KeyboardNavigation.prototype.move = function (direction) {
        var curModule = this.modules && this.modules[this.currentModuleIx];
        if (curModule && curModule.terminate) {
            curModule.terminate(direction);
        }
        // Remove existing focus border if any
        if (this.chart.focusElement) {
            this.chart.focusElement.removeFocusBorder();
        }
        this.currentModuleIx += direction;
        var newModule = this.modules && this.modules[this.currentModuleIx];
        if (newModule) {
            if (newModule.validate && !newModule.validate()) {
                return this.move(direction); // Invalid module, recurse
            }
            if (newModule.init) {
                newModule.init(direction); // Valid module, init it
                return true;
            }
        }
        // No module
        this.currentModuleIx = 0; // Reset counter
        // Set focus to chart or exit anchor depending on direction
        this.exiting = true;
        if (direction > 0) {
            this.exitAnchor.focus();
        }
        else {
            this.tabindexContainer.focus();
        }
        return false;
    };
    /**
     * We use an exit anchor to move focus out of chart whenever we want, by
     * setting focus to this div and not preventing the default tab action. We
     * also use this when users come back into the chart by tabbing back, in
     * order to navigate from the end of the chart.
     * @private
     */
    KeyboardNavigation.prototype.updateExitAnchor = function () {
        var endMarkerId = 'highcharts-end-of-chart-marker-' + this.chart.index, endMarker = getElement(endMarkerId);
        this.removeExitAnchor();
        if (endMarker) {
            this.makeElementAnExitAnchor(endMarker);
            this.exitAnchor = endMarker;
        }
        else {
            this.createExitAnchor();
        }
    };
    /**
     * Chart container should have tabindex if navigation is enabled.
     * @private
     */
    KeyboardNavigation.prototype.updateContainerTabindex = function () {
        var a11yOptions = this.chart.options.accessibility, keyboardOptions = a11yOptions && a11yOptions.keyboardNavigation, shouldHaveTabindex = !(keyboardOptions && keyboardOptions.enabled === false), chart = this.chart, container = chart.container;
        var tabindexContainer;
        if (chart.renderTo.hasAttribute('tabindex')) {
            container.removeAttribute('tabindex');
            tabindexContainer = chart.renderTo;
        }
        else {
            tabindexContainer = container;
        }
        this.tabindexContainer = tabindexContainer;
        var curTabindex = tabindexContainer.getAttribute('tabindex');
        if (shouldHaveTabindex && !curTabindex) {
            tabindexContainer.setAttribute('tabindex', '0');
        }
        else if (!shouldHaveTabindex) {
            chart.container.removeAttribute('tabindex');
        }
    };
    /**
     * @private
     */
    KeyboardNavigation.prototype.makeElementAnExitAnchor = function (el) {
        var chartTabindex = this.tabindexContainer.getAttribute('tabindex') || 0;
        el.setAttribute('class', 'highcharts-exit-anchor');
        el.setAttribute('tabindex', chartTabindex);
        el.setAttribute('aria-hidden', false);
        // Handle focus
        this.addExitAnchorEventsToEl(el);
    };
    /**
     * Add new exit anchor to the chart.
     *
     * @private
     */
    KeyboardNavigation.prototype.createExitAnchor = function () {
        var chart = this.chart, exitAnchor = this.exitAnchor = doc.createElement('div');
        chart.renderTo.appendChild(exitAnchor);
        this.makeElementAnExitAnchor(exitAnchor);
    };
    /**
     * @private
     */
    KeyboardNavigation.prototype.removeExitAnchor = function () {
        if (this.exitAnchor && this.exitAnchor.parentNode) {
            this.exitAnchor.parentNode
                .removeChild(this.exitAnchor);
            delete this.exitAnchor;
        }
    };
    /**
     * @private
     */
    KeyboardNavigation.prototype.addExitAnchorEventsToEl = function (element) {
        var chart = this.chart, keyboardNavigation = this;
        this.eventProvider.addEvent(element, 'focus', function (ev) {
            var e = ev || win.event, focusComesFromChart = (e.relatedTarget &&
                chart.container.contains(e.relatedTarget)), comingInBackwards = !(focusComesFromChart || keyboardNavigation.exiting);
            if (comingInBackwards) {
                // Focus the container instead
                keyboardNavigation.tabbingInBackwards = true;
                keyboardNavigation.tabindexContainer.focus();
                delete keyboardNavigation.tabbingInBackwards;
                e.preventDefault();
                // Move to last valid keyboard nav module
                // Note the we don't run it, just set the index
                if (keyboardNavigation.modules &&
                    keyboardNavigation.modules.length) {
                    keyboardNavigation.currentModuleIx =
                        keyboardNavigation.modules.length - 1;
                    var curModule = keyboardNavigation.modules[keyboardNavigation.currentModuleIx];
                    // Validate the module
                    if (curModule &&
                        curModule.validate && !curModule.validate()) {
                        // Invalid. Try moving backwards to find next valid.
                        keyboardNavigation.prev();
                    }
                    else if (curModule) {
                        // We have a valid module, init it
                        curModule.init(-1);
                    }
                }
            }
            else {
                // Don't skip the next focus, we only skip once.
                keyboardNavigation.exiting = false;
            }
        });
    };
    /**
     * Remove all traces of keyboard navigation.
     * @private
     */
    KeyboardNavigation.prototype.destroy = function () {
        this.removeExitAnchor();
        this.eventProvider.removeAddedEvents();
        this.chart.container.removeAttribute('tabindex');
    };
    return KeyboardNavigation;
}());
/* *
 *
 *  Class Namespace
 *
 * */
(function (KeyboardNavigation) {
    /* *
     *
     *  Declarations
     *
     * */
    /* *
     *
     *  Construction
     *
     * */
    var composedItems = [];
    /* *
     *
     *  Functions
     *
     * */
    /* eslint-disable valid-jsdoc */
    /**
     * @private
     */
    function compose(ChartClass) {
        MenuComponent.compose(ChartClass);
        if (composedItems.indexOf(ChartClass) === -1) {
            composedItems.push(ChartClass);
            var chartProto = ChartClass.prototype;
            chartProto.dismissPopupContent = chartDismissPopupContent;
        }
        if (composedItems.indexOf(doc) === -1) {
            composedItems.push(doc);
            addEvent(doc, 'keydown', documentOnKeydown);
        }
        return ChartClass;
    }
    KeyboardNavigation.compose = compose;
    /**
     * Dismiss popup content in chart, including export menu and tooltip.
     * @private
     */
    function chartDismissPopupContent() {
        var chart = this;
        fireEvent(this, 'dismissPopupContent', {}, function () {
            if (chart.tooltip) {
                chart.tooltip.hide(0);
            }
            chart.hideExportMenu();
        });
    }
    /**
     * Add event listener to document to detect ESC key press and dismiss
     * hover/popup content.
     * @private
     */
    function documentOnKeydown(e) {
        var keycode = e.which || e.keyCode;
        var esc = 27;
        if (keycode === esc && H.charts) {
            H.charts.forEach(function (chart) {
                if (chart && chart.dismissPopupContent) {
                    chart.dismissPopupContent();
                }
            });
        }
    }
})(KeyboardNavigation || (KeyboardNavigation = {}));
/* *
 *
 *  Default Export
 *
 * */
export default KeyboardNavigation;

/**
 * Created by pulphix on 13/12/16.
 */
try { return (function (element, css_property, using) {
    using = using || document;
    if (css_property.toLowerCase() == "offsetheight"){
        return element.offsetHeight + "px"
    }
    var elementStyle = window.getComputedStyle(element,null);
    return elementStyle.getPropertyValue(css_property)
}).apply(this, arguments); }
catch(e) { throw (e instanceof Error) ? e : new Error(e); }
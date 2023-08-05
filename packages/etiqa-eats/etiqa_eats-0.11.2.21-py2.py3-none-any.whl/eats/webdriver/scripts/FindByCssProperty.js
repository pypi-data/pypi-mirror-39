/**
 * Created by pulphix on 13/12/16.
 */
try { return (function (css_property, css_value, using) {
    using = using || document;

    var elements = using.querySelectorAll('*');
    var matches = [];
    for (var i = 0; i < elements.length; ++i) {
        var element = elements[i];
        var elementStyle = window.getComputedStyle(element,null);
        if (elementStyle.getPropertyValue(css_property) === css_value) {
            matches.push(element);
        }
    }
    return matches;
}).apply(this, arguments); }
catch(e) { throw (e instanceof Error) ? e : new Error(e); }
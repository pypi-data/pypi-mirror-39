try { return (function (element, using) {
    using = using || document;
    var left = parseInt(element.offsetLeft);
    var top = parseInt(element.offsetTop);
    var right = parseInt(left + parseInt(element.offsetWidth));
    var bottom = parseInt(top + parseInt(element.offsetHeight));
    var x = Math.max(left, 0);
    var y = Math.max(top, 0);
    var style = window.getComputedStyle(element)

    return JSON.stringify({
        x:x,
        y:y,
        width: right - x,
        height: bottom - y,
        shadow: style.getPropertyValue('box-shadow')
    });
}).apply(this, arguments); }
catch(e) { throw (e instanceof Error) ? e : new Error(e); }
try { return (function (element, using) {
    using = using || document;
    return JSON.stringify({
        width: using.documentElement.clientWidth,
        height: using.documentElement.clientHeight
    });
}).apply(this, arguments); }
catch(e) { throw (e instanceof Error) ? e : new Error(e); }
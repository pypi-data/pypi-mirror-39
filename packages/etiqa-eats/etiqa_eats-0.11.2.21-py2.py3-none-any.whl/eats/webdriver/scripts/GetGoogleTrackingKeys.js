try { return (function () {
    var values = []
    var trackers = ga.getAll();
    function trackerObj(tracker) {
        var keys = tracker.b.data.keys;
        var tracker_obj = {};

        keys.forEach(function (key) {
            var value = tracker.get(key);

            if (typeof(value) === "function") return;

            tracker_obj[key] = tracker.get(key);
        });

        return tracker_obj;
    }

    trackers.forEach(function (tracker) {
        values.push(trackerObj(tracker));
    });
    return JSON.stringify(values)
}).apply(this, arguments); }
catch(e) { throw (e instanceof Error) ? e : new Error(e); }
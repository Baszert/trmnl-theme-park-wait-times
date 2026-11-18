// Queue Coaster: queue-times.com for one park. Out: ride list by wait, crowd level, a thought, and the hours of the day.
function transform(input) {
  try {
    var d = input.IDX_0 || input, r1 = function (n) { return Math.round(n * 10) / 10; };
    var now = Math.round((input.__now || Date.now()) / 1000);
    var lands = Array.isArray(d.lands) ? d.lands : null, loose = Array.isArray(d.rides) ? d.rides : [];
    if (!lands && !loose.length) return { qc: { status: 'offline', top: [], now: Math.round(Date.now() / 1000) } };
    var skip = /single[\s-]?rider|rider (swap|switch)|child swap|virtual queue|lightning lane|premier access|fast ?pass/i;
    var all = [], upd = 0;
    var take = function (r, land) {
      if (skip.test(r.name)) return;
      var t = Math.round(Date.parse(r.last_updated) / 1000) || 0; if (t > upd) upd = t;
      all.push({ n: r.name.normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[®™]/g, '').replace(/,\s*presented by.*$/i, '').replace(/\s+/g, ' ').trim(), w: r.is_open ? (r.wait_time | 0) : 0, o: !!r.is_open, i: all.length, land: land });
    };
    (lands || []).forEach(function (l) { (l.rides || []).forEach(function (r) { take(r, l.name); }); });
    loose.forEach(function (r) { take(r, ''); });

    var open = all.filter(function (r) { return r.o; });
    // Opening hours come from themeparks.wiki (IDX_1). Without them (a park that source does not know), a park with almost nothing running counts as closed.
    var sched = (input.IDX_1 || {}).schedule, hours = null, nowMs = now * 1000;
    if (Array.isArray(sched)) {
      var wins = sched.filter(function (e) { return e.type === 'OPERATING' && /T\d\d:\d\d/.test(e.openingTime) && /T\d\d:\d\d/.test(e.closingTime); }).map(function (e) {
        var om = /([+-])(\d\d):(\d\d)$/.exec(e.openingTime);
        return { o: Date.parse(e.openingTime), c: Date.parse(e.closingTime), ot: /T(\d\d:\d\d)/.exec(e.openingTime)[1], ct: /T(\d\d:\d\d)/.exec(e.closingTime)[1], date: e.date, off: om ? (om[1] === '-' ? -1 : 1) * (+om[2] * 60 + +om[3]) : 0 };
      }).sort(function (a, b) { return a.o - b.o; });
      if (wins.length) {
        var cur = wins.filter(function (w) { return w.o <= nowMs && nowMs < w.c; })[0], nxt = wins.filter(function (w) { return w.o > nowMs; })[0];
        if (cur) { var lm = Math.max(0, Math.round((cur.c - nowMs) / 60000)); hours = { open: true, closes: cur.ct, day: { from: cur.ot, to: cur.ct, pct: Math.max(0, Math.min(100, Math.round((nowMs - cur.o) / (cur.c - cur.o) * 100))), left: lm >= 60 ? Math.floor(lm / 60) + 'h ' + ('0' + lm % 60).slice(-2) + 'm left' : lm + ' min left' } }; }
        else {
          hours = { open: false, opens: '' };
          if (nxt) {
            var ld = new Date(nowMs + nxt.off * 60000).toISOString().slice(0, 10), tm = new Date(Date.parse(ld + 'T00:00:00Z') + 86400000).toISOString().slice(0, 10);
            var day = nxt.date === ld ? 'today' : nxt.date === tm ? 'tomorrow' : ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'][new Date(nxt.date + 'T00:00:00Z').getUTCDay()];
            hours.opens = day + ' at ' + nxt.ot;
          }
        }
      }
    }
    var reason = hours ? (hours.open ? (open.length ? 'open' : 'down') : 'hours') : 'guess';
    var status = !all.length ? 'offline' : hours ? (hours.open && open.length ? 'open' : 'closed') : (open.length < 3 || open.length / all.length < 0.15) ? 'closed' : 'open';
    var sum = open.reduce(function (s, r) { return s + r.w; }, 0), avg = open.length ? sum / open.length : 0;
    var byWait = open.slice().sort(function (a, b) { return b.w - a.w || a.i - b.i; });
    var max = byWait.length ? byWait[0].w : 0;
    byWait.forEach(function (r, k) { r.rank = k + 1; });
    var short = function (n, k) { return n.length > k ? n.slice(0, k - 1).replace(/[\s:,;-]+$/, '') + '…' : n; };

    // The words under the crowd gauge.
    var level = avg < 6 ? 'QUIET' : avg < 15 ? 'LIVELY' : avg < 30 ? 'BUSY' : avg < 45 ? 'PACKED' : 'INSANE';
    var seg = open.length ? Math.max(1, Math.min(10, Math.round(avg / 4))) : 0;
    var nm = max ? byWait[0].n : '';
    var thought = !open.length ? '' : max >= 60 ? nm + ' is ' + max + ' min?! I have queued for ages...'
      : max >= 40 ? nm + ' is ' + max + ' min. Snacks first!'
      : max >= 20 ? 'Not bad! ' + nm + ' is only ' + max + ' min.'
      : max >= 10 ? 'Short lines today. Go ride ' + nm + '!'
      : 'Walk-on everywhere! Ride it all!';

    var top = byWait.slice(0, 20).map(function (r) {
      return { n: r.n, w: r.w, rank: r.rank, q: r.w ? Math.min(5, Math.ceil(r.w / 12)) : 0, pct: max ? Math.max(2, Math.round(r.w / max * 100)) : 0,
        heat: r.w >= 45 ? 'hot' : r.w >= 20 ? 'warm' : 'cool' };
    });

    // The tip: the open ride with the shortest line right now (a walk-on wins).
    var low = byWait.length ? byWait[byWait.length - 1] : null;
    var tip = low ? { n: low.n, w: low.w } : null;
    // The day bar: opening to closing with a mark for now.
    var day = null;
    if (hours && hours.open && hours.day) day = hours.day;
    return { qc: { status: status, reason: reason, closes: hours && hours.open ? hours.closes : '', opens: hours && !hours.open ? hours.opens : '', now: Math.round((input.__now || Date.now()) / 1000), updated: upd, open: open.length, total: all.length, down: all.length - open.length,
      avg: Math.round(avg), max: max, level: level, seg: seg, thought: thought, top: top, tip: tip, day: day, walkons: open.filter(function (r) { return !r.w; }).length } };
  } catch (err) {
    return { qc: { status: 'offline', error: String(err), top: [], now: Math.round(Date.now() / 1000) } };
  }
}
if (typeof module !== 'undefined') module.exports = transform;

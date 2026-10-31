// Real data from queue-times.com (26 Oct 2026, evening), plus a busy-day sample made by stretching Disneyland Paris' queues.
import fs from 'node:fs';
const raw = (f) => JSON.parse(fs.readFileSync(new URL('./raw/' + f, import.meta.url)));
const busy = () => { const d = raw('p4.json'); const k = 2.4, f = (r) => ({ ...r, wait_time: r.is_open ? Math.round(r.wait_time * k / 5) * 5 : 0 }); return { lands: d.lands.map((l) => ({ ...l, rides: l.rides.map(f) })), rides: d.rides.map(f) }; };
const at = (f, park, sched, now = '2026-10-26T20:20Z') => ({ lang: 'en', off: 3600, park, input: () => { const d = typeof f === 'function' ? f() : raw(f); return { IDX_0: d, ...(sched ? { IDX_1: raw(sched) } : {}), __now: Date.parse(now) }; } });
export const S = {
  paris: { label: 'Disneyland Paris, normal evening', ...at('p4.json', '4~Disneyland Paris', 's4.json') },
  busy: { label: 'Busy day sample (Disneyland Paris waits x2.4)', ...at(busy, '4~Disneyland Paris', 's4.json') },
  calm: { label: 'Phantasialand, calm', ...at('p56.json', '56~Phantasialand') },
  liseberg: { label: 'Liseberg', ...at('p11.json', '11~Liseberg') },
  efteling: { label: 'Efteling after closing time: opens tomorrow 10:00', ...at('p160.json', '160~Efteling', 's160.json') },
  closed: { label: 'Plopsaland, every ride closed', ...at('p54.json', '54~Plopsaland Belgium') },
  offline: { label: 'No connection', lang: 'en', off: 3600, park: '160~Efteling', input: () => ({ IDX_0: { error: 'timeout' }, __now: Date.parse('2026-10-26T20:20Z') }) },
};

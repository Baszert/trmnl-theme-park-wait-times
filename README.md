# Theme Park Wait Times for TRMNL (Queue Coaster)

Live wait times for 140 theme parks. Which rides have the longest queues, how busy the park is, how long it stays open, and what a guest in the line thinks about it. The waits are drawn as the hills of a pixel roller coaster. A closed park shows when the gates open instead.

## Screens and settings

All four sizes (full, half horizontal, half vertical, quadrant), landscape and portrait.

- **Park:** pick your park from the list (the default is the Efteling). No account, no keys.

## How it works

- The polling URLs are the queue times of one park from [Queue-Times.com](https://queue-times.com) and its schedule from [ThemeParks.wiki](https://themeparks.wiki).
- `src/transform.js` (serverless) puts the rides in order by wait, leaves out the extras that are not queues (single rider, virtual queue, Lightning Lane and the like), works out the crowd level and the line of the coaster track, and takes the hours from the schedule.
- The park list is in `dev/parks.json`; `dev/gen.py`, `dev/sprites.py` and `dev/cars.py` draw the sprites.

## Development

```bash
cd dev && npm install && cd ..
node dev/build.mjs            # renders every scenario into dev/out with the framework CSS (needs a connection)
python3 dev/render.py         # device-faithful mockups (see the script for the details)
```

`dev/raw` holds real queue times (26 Oct 2026); one scenario stretches the queues of a park to show a busy day.

## Data and credits

- Wait times: **[Powered by Queue-Times.com](https://queue-times.com)**. Opening hours: [ThemeParks.wiki](https://themeparks.wiki).
- The pixel font (`dev/rct2.otf`) is by Qimplef, [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/): the font stays under that licence, the rest of the code under MIT.
- Not affiliated with any of the parks.

## Links and license

- This is a TRMNL plugin (private plugin id 520725); the code here is what runs on TRMNL.
- Code: [MIT](LICENSE). The pixel font is CC BY-SA 3.0 (see above).

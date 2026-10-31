# Writes src/settings.yml: the park select (queue-times id, name, themeparks.wiki id for opening hours) and the two polling URLs. Keeps the plugin id.
import json, re
q = json.load(open('dev/parks.json')); tp = json.load(open('dev/tpmap.json'))
parks = sorted({(k['name'], k['country'], k['id']) for g in q for k in g['parks']})
j = lambda x: json.dumps(x, ensure_ascii=False)
opts = ''.join(f"  - {j(f'{n} ({c})')}: {j('%d~%s~%s' % (i, n.replace(chr(126), ' '), tp.get(str(i), 'none')))}\n" for n, c, i in parks)
old = open('src/settings.yml').read(); pid = re.search(r'^id: (\d+)', old, re.M)
default = '160~Efteling~' + tp['160']
about = ("Live wait times for 140 theme parks. See which rides have the longest queues, how busy the park is, how long it stays open, and what a guest in the line thinks about it. A closed park shows when the gates open instead.<br><br>"
         "Pick your park in the settings. No account, no keys.<br><br>"
         "Data: <a href=\"https://queue-times.com\">Powered by Queue-Times.com</a> (waits) and <a href=\"https://themeparks.wiki\">ThemeParks.wiki</a> (opening hours). Pixel font by Qimplef (CC BY-SA 3.0).")
urls = ("https://queue-times.com/parks/{{ park | default: \"%s\" | split: \"~\" | first }}/queue_times.json\n"
        "https://api.themeparks.wiki/v1/entity/{{ park | default: \"%s\" | split: \"~\" | last }}/schedule" % (default, default))
y = f"""---
strategy: polling
no_screen_padding: 'no'
dark_mode: 'no'
static_data: ''
polling_verb: get
framework_version:
serverless_language: node
refresh_interval_floor:
polling_url: |-
  {urls.replace(chr(10), chr(10) + '  ')}
polling_headers: ''
polling_body:
{('id: ' + pid.group(1) + chr(10)) if pid else ''}oauth_enabled: 'false'
oauth_pkce_enabled: 'no'
custom_fields:
- keyname: about
  field_type: author_bio
  name: About This Plugin
  category: games,travel
  description: {j(about)}
  email_address: trmnl@achtnegen.nl
- keyname: park
  field_type: select
  name: Park
  description: Which theme park to show. Waits update every few minutes while the park is open.
  options:
{opts}  default: {default}
name: Theme Park Wait Times
description:
refresh_interval: 15
"""
open('src/settings.yml', 'w').write(y); print('settings.yml', len(parks), 'parks')

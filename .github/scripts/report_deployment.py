from datetime import datetime
import json
import sys

from jinja2 import Template

import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib.pyplot import figure

args = sys.argv
project = args[1]
report = args[2]

with open("reports/{}/deployments.json".format(project), "r+") as f:
    out = json.load(f)
    deps = out.get("results", {}).get("deployments", [])
    current = json.loads(report)
    deps.insert(0, current)
    out["results"]["deployments"] = deps
    f.seek(0)
    f.write(json.dumps(out, indent=4))
    f.truncate()

def get_datetimes(timestring):
    # Remove milliseconds
    timestring = timestring.split('.')[0]
    return datetime.strptime(timestring, "%Mm%S")

dates = [datetime.strptime(d.get("date"), "%a %b %d %H:%M:%S %Y") for d in deps]
times = [get_datetimes(d.get("time")) for d in deps]

l = len(dates) if len(dates) <= 30 else 30

dates = dates[:l]
times = times[:l]

figure(figsize=(12, 8), dpi=80)
ax = plt.gca()
myFmt = DateFormatter("%Mmin %Ss")
ax.yaxis.set_major_formatter(myFmt)
ax.plot(dates, times, linestyle='-', marker='.', color='b')
plt.title("GalaxyKubeMan startup time")
plt.xlabel("Date of Test")
plt.ylabel("Startup Time")
plt.gcf().autofmt_xdate()
plt.savefig("reports/{}/deployments.svg".format(project))


with open(".github/templates/deployments.html.j2", "r") as f:
    template = Template(f.read())

with open("reports/{}/deployments.html".format(project), "w") as f:
    htmlout = "<thead><tr><th>Date</th><th>Status</th><th>GKM time</th></tr></thead><tbody>"
    for each in deps:
        htmlout += "<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format(each.get("date"), each.get("status"), each.get("time"))
    htmlout += "</tbody>"
    f.write(template.render(table=htmlout))


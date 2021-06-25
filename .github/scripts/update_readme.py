from datetime import datetime
import json
import sys

from jinja2 import Template

args = sys.argv
inchunk = args[1]
allchunks = args[2]
readme_path = args[3]

with open(inchunk, 'r') as f:
    new_chunk = json.load(f)
    chunk_id = list(new_chunk.keys())[0]
    new_chunk = new_chunk.get(chunk_id)

with open(allchunks, 'r+') as f:
    chunks = json.load(f)
    old_chunk = chunks.get(chunk_id, {})
    new_chunk['run2'] = old_chunk.get('run1', 'N/A')
    new_chunk['date2'] = old_chunk.get('date1', 'N/A')
    chunks[chunk_id] = new_chunk
    f.seek(0)
    f.write(json.dumps(chunks, indent=4))
    f.truncate()

with open(".github/templates/README.md.j2", "r") as f:
    template = Template(f.read())

with open(readme_path, "w") as f:
    htmlout = "<thead><tr><th>Chunk ID</th><th>Tool List</th><th>Latest report</th><th>Previous report</th></tr></thead><tbody>"
    ids = list(chunks.keys())
    ids = [int(x) for x in ids]
    ids.sort()
    ids = [str(x) for x in ids]
    for eachid in ids:
        eachchunk = chunks.get(eachid)
        htmlout += "<tr><td>{}</td><td><a href=\"{}\">Toolset</a></td><td><a href=\"{}\">{}</a></td><td><a href=\"{}\">{}</a></td></tr>".format(eachid, eachchunk.get("tools"), eachchunk.get("run1"), eachchunk.get("date1"), eachchunk.get("run2"), eachchunk.get("date2"))
    htmlout += "</tbody>"
    f.write(template.render(anviltools=htmlout))

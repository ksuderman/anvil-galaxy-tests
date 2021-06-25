import yaml
import re
import sys

args = sys.argv
outdir = args[1]


with open("production/anvil/tools.yaml", 'r') as f:
    out = yaml.safe_load(f.read())

tool_list = out.get('tools', [])
sections = {}
for tool in tool_list:
    section = tool.get("tool_panel_section_label") or "Other Tools"
    section_list = sections.get(section, [])
    section_list.append(tool)
    sections[section] = section_list

def standardize_name(section):
    return re.sub("[^0-9a-z]", "_", section.lower())

print(sections.keys())
for section in sections.keys():
    t_list = sections.get(section)
    out = {"install_repository_dependencies": "true",
           "install_resolver_dependencies": "false",
           "install_tool_dependencies": "false",
           "tool_panel_section_label": section}
    out_tools = []
    section_id = standardize_name(section)
    for t in t_list:
        t.pop("tool_shed_url")
        t["tool_panel_section_id"] = section_id
        out_tools.append(t)
    out["tools"] = out_tools
    with open("{}/{}.yml.lock".format(outdir, section_id), 'w') as f:
        f.write(yaml.safe_dump(out))
    out.pop("install_repository_dependencies")
    out.pop("install_resolver_dependencies")
    out.pop("install_tool_dependencies")
    new_tools = []
    for t in out_tools:
        n = t.get("name")
        owner = t.get("owner")
        new_tools.append({"name": n, "owner": owner})
    out["tools"] = new_tools
    with open("{}/{}.yml".format(outdir, section_id), 'w') as f:
        f.write(yaml.safe_dump(out))


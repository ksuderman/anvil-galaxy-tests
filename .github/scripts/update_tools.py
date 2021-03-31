import os
import sys
import yaml
from bioblend import toolshed

"""
A simple program to update the tool revisions in a tools.yml file.

The program will either replace the list of revisions with just the latest
revision available on the ToolShed, or append the latest revision (if a newer
revision is available) to the existing list of revisions.

NOTE: The program doesn't (can't) actually check if an available revision is
"newer" than the current revision, just if they have differnt SHA values.  If
the revisions are different it is assumed that the version on the ToolShed is
newer.

USAGE:

python .github/scripts/update_tools.py [append|replace] ./production/anvil/tools.yml /path/to/write.yml
"""

DEFAULT_TOOLSHED = 'https://toolshed.g2.bx.psu.edu'

# Common keys into the tools dict. Defined solely so our IDE can do completions
# and I don't consistently misspell revisisions or have to remember if it is
# toolshed_url or tool_shed_url
NAME = 'name'
OWNER = 'owner'
TOOLS = 'tools'
SHED = 'tool_shed_url'
REVISIONS = 'revisions'

# The toolsheds that we have already connected to.
tool_sheds = { DEFAULT_TOOLSHED: toolshed.ToolShedInstance(DEFAULT_TOOLSHED) }

def validate(tool):
    """Ensure the tool has the fields we need so we don't need to check later."""
    if SHED not in tool:
        tool[SHED] = DEFAULT_TOOLSHED
    if REVISIONS not in tool:
        tool[REVISIONS] = []

def append(tool, revision):
    if revision not in tool[REVISIONS]:
        tool[REVISIONS].append(revision)

def replace(tool, revision):
    tool[REVISIONS] = [ revision ]

def update_file(add_to_list, infile, outfile):
    with open(infile, "r") as f:
        data = yaml.safe_load(f)

    tool_list = data[TOOLS]
    for tool in tool_list:
        print(f"Getting latest revision for {tool[NAME]}")
        validate(tool)
        url = tool[SHED]
        if url in tool_sheds:
            ts = tool_sheds[url]
        else:
            ts = toolshed.ToolShedInstance(url)
            tool_sheds[url] = ts
        revs = ts.repositories.get_ordered_installable_revisions(tool[NAME], tool[OWNER])
        if revs and len(revs) > 0:
            add_to_list(tool, revs[-1])

    data = { "tools": tool_list }
    with open(outfile, "w") as f:
        yaml.dump(data, f, default_flow_style=False)

if __name__ == '__main__':
    # Very very simple command line parsing.
    if len(sys.argv) != 4:
        print(f"ERROR: Expected 3 parameters but found {len(sys.argv)-1}")
        print(f"USAGE: python {sys.argv[0]} [append|replace] <input file> <output file>")
        sys.exit(1)

    mode = None
    if sys.argv[1] == 'append':
        mode = append
    elif sys.argv[1] == 'replace':
        mode = replace
    else:
        print(f"Invalid mode: {sys.argv[1]}")
        print("Must be one of append or replace")
        sys.exit(1)

    infile = sys.argv[2]
    outfile = sys.argv[3]
    if not os.path.exists(infile):
        print(f"Could not find the input file {infile}")
        sys.exit(1)

    update_file(mode, infile, outfile)

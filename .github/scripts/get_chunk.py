import os
import sys
import yaml
import json
from datetime import datetime

RUNS_PER_DAY = 2
NCHUNKS = 7 * RUNS_PER_DAY

github_base = "https://github.com/anvilproject/galaxy-tests/blob/main"
preview_base = "https://htmlpreview.github.io/?{}".format(github_base)

def load_tools(tools_file: str) -> list[dict]:
    with open(tools_file) as f:
        tools = yaml.safe_load(f)
    return tools['tools']


def get_chunk(chunk:int, tools: list[dict]) -> dict:
    return {
        'chunk': chunk,
        'tools': [ tools[i] for i in range(0,len(tools)) if i % NCHUNKS == chunk]
    }


def write_tools(tools: dict, filepath:str) -> None:
    with open(filepath, 'w', encoding='UTF-8') as f:
        for tool in tools['tools']:
            for rev in tool['revisions']:
                # Save the parameters needed by galaxy-tool-test to simplify
                # things later.
                f.write(f"-t {tool['name']} --tool-version {rev}\n")


def run(args: list[str]):
    tools_file = None
    chunk = None
    outdir = None
    while len(args) > 0:
        arg = args.pop(0)
        if arg in ['-c', '--chunk']:
            chunk = int(args.pop(0))
        elif arg in ['-o', '--output']:
            outdir = args.pop(0)
        else:
            tools_file = arg

    if tools_file is None:
        print("ERROR: tool.yml file not provided.")
        return
    if outdir is None:
        print("ERROR: output directory not provided")
        return
    if chunk is None:
        today = datetime.today()
        day = today.weekday()
        ampm = 0 if today.strftime('%p') == 'AM' else 1
        chunk = day * RUNS_PER_DAY + ampm

    tools = load_tools(tools_file)
    tools = get_chunk(chunk, tools)
    with open(f"{outdir}/tools.yml", 'w', encoding='UTF-8') as f:
        yaml.safe_dump(tools, f)

    chunk_data = {
        str(chunk): {
            "run1": f"{preview_base}/{outdir}/results.html",
            "date1": today.strftime("%a %b %d %H:%M:%S %Y"),
            "tools": f"{github_base}/{outdir}/tools.yml"
        }
    }

    with open(f'{outdir}/chunk.json', 'w') as f:
        f.write(json.dumps(chunk_data, indent=4))

    write_tools(tools, f"{outdir}/chunk.txt")



if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Error: the path to the tools.yml file was not provided")
        sys.exit(1)
    run(sys.argv)

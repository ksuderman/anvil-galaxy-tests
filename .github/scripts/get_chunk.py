import os
import sys
import yaml
import json
from datetime import datetime

RUNS_PER_DAY = 2
NCHUNKS = 7 * RUNS_PER_DAY


def load_tools(tools_file: str) -> list[dict]:
    with open(tools_file) as f:
        tools = yaml.safe_load(f)
    return tools['tools']


def get_chunk(chunk:int, tools: list[dict]) -> dict:
    return {
        'chunk': chunk,
        'tools': [ tools[i] for i in range(0,len(tools)) if i % NCHUNKS == chunk]
    }


def print_tools(tools: dict) -> None:
    for tool in tools['tools']:
        for rev in tool['revisions']:
            # Save the parameters needed by galaxy-tool-test to simplify
            # things later.
            print(f"-t {tool['name']} --tool-version {rev}")


def run(args: list[str]):
    tools_file = None
    chunk = None
    while len(args) > 0:
        arg = args.pop(0)
        if arg in ['-c', '--chunk']:
            chunk = int(args.pop(0))
        else:
            tools_file = arg

    if tools_file is None:
        print(f"ERROR: tool.yml file not provided.")
        return
    if chunk is None:
        today = datetime.today()
        day = today.weekday()
        ampm = 0 if today.strftime('%p') == 'AM' else 1
        chunk = day * RUNS_PER_DAY + ampm

    tools = load_tools(tools_file)
    tools = get_chunk(chunk, tools)
    print_tools(tools)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Error: the path to the tools.yml file was not provided")
        sys.exit(1)
    run(sys.argv)

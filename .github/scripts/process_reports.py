import os
import pprint
import sys
import json


def run(dirname: str):
    with open(f'{dirname}/chunk.json') as f:
        chunk = list(json.load(f).keys())[0]

    json_file = f'{dirname}/results.json'
    with open(json_file) as f:
        # print(f"Reading {json_file}")
        results = json.load(f)

    # passed = []
    # failed = []
    # errored = []
    # skipped = []
    # lines = []
    test_name = json_file.split('/')[3]
    # print(test_name)
    test_segments = test_name.split('-')
    # pprint.pprint(test_segments)
    try:
        if len(test_segments) == 7:
            type = test_segments[0]
            year = int(test_segments[1])
            month = test_segments[2]
            day = test_segments[3]
            hour = test_segments[4]
            if year < 100:
                year += 2000
        else:
            year = 2023
            type = test_segments[0]
            month = test_segments[1]
            day = test_segments[2]
            hour = test_segments[3]
    except:
        print(test_name)
        return

    timestamp = f"{year}{month}{day}{hour}"
    for test in results['tests']:
        tool = test['id']
        if '/' in tool:
            parts = tool.split('/')
            tool = f'{parts[-2]}/{parts[-1]}'
        # print(tool)
        data = test['data']
        if 'time_seconds' in data:
            t = data['time_seconds']
        else:
            t = 0
        status = data['status']
        # if status == 'success':
        #     passed.append(tool)
        # elif status == 'failure':
        #     failed.append(tool)
        # elif status == 'error':
        #     errored.append(tool)
        # elif status == 'skip':
        #     skipped.append(tool)
        # else:
        #     print(f"Unknown status '{status}'")

        # lines.append(f"{tool},{status}{t}")
        print(f"{type},{chunk},{timestamp},{tool},{status},{t}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("No results file given")
    else:
        run(sys.argv[1])
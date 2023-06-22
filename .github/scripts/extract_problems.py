import os
import pprint
import sys
import json


def run(dirname: str):
    json_file = f'{dirname}/results.json'
    with open(json_file) as f:
        # print(f"Reading {json_file}")
        results = json.load(f)

    test_name = json_file.split('/')[3]
    test_segments = test_name.split('-')
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
        data = test['data']
        status = data['status']
        if 'execution_problem' in data:
            print(f"{type},execution,{timestamp},{tool},{status},{data['execution_problem']}")
        if 'output_problems' in data:
            for problem in data['output_problems']:
                print(f"{type},output,{timestamp},{tool},{status},{problem.splitlines()[0]}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("No results file given")
    else:
        run(sys.argv[1])
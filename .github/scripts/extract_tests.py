import os
import sys
import json

"""
A script to extract the test results from the results.json file generated
by planemo.
"""

def main(infile):
    with open(infile) as f:
        data = json.load(f)

    copy = {}
    for key in ['version', 'suitename', 'results']:
        copy[key] = data[key]

    extracted = []
    for t in data['tests']:
        if t['data']['status'] != 'success':
            extracted.append(t)
    copy['tests'] = extracted
    print(json.dumps(copy, indent=4))


if __name__ == "__main__":
    if len(sys.argv)  != 2:
        print(f"USAGE: python {sys.argv[0]} /path/to/results.json")
        sys.exit(1)

    infile = sys.argv[1]
    if not os.path.exists(infile):
        print(f"Unable to find the file {infile}")
        sys.exit(1)

    main(infile)
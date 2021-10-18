import yaml
import json
import sys
from datetime import datetime

args = sys.argv
infile = args[1]
outdir = args[2]
today = datetime.today()
weekday = today.weekday()
time_of_day = 0 if today.strftime("%p") == 'AM' else 1
runs_per_day = 2 # run twice a day
total_chunks = 7 * runs_per_day

github_base = "https://github.com/anvilproject/galaxy-ci/blob/main"
preview_base = "https://htmlpreview.github.io/?{}".format(github_base)

with open(infile, 'r') as f:
    out = yaml.safe_load(f.read())

l = out.get('tools', [])
num_per_run = int(len(l)/total_chunks)
weekly_num = weekday * runs_per_day + time_of_day
daily_num = today.hour % total_chunks
# Default to cycling every week
current_num = weekly_num

# option to override which section to run
if len(args) > 3:
    chunk_args = args[3]
    try:
        new_num = int(args[3])
        if new_num in range(0, total_chunks):
            current_num = new_num
        elif not new_num == 999:
            print(f"Given input {new_num} is out of the valid range [0:{total_chunks-1}]")
    except ValueError:
        if "week" in chunk_args:
            current_num = weekly_num
        elif "dai" in chunk_args or "day" in chunk_args:
            current_num = daily_num
        else:
            print(f"Given input {args[3]} is invalid")
        pass

start = current_num * num_per_run
end = (current_num + 1) * num_per_run

print(f'Running on chunk {current_num}')
print(f'Index range: [{start}:{end}]')

end = len(l) if end > len(l) else end
out['tools'] = l[start:end]


with open(f'{outdir}/tools.yaml', 'w') as f:
    f.write(yaml.safe_dump(out))

chunk = {}
chunk[str(current_num)] = {"run1": "{}/{}/results.html".format(preview_base, outdir),
                           "date1": today.strftime("%a %b %d %H:%M:%S %Y"), 
                           "tools": "{}/{}/tools.yaml".format(github_base, outdir)}

with open(f'{outdir}/chunk.json', 'w') as f:
    f.write(json.dumps(chunk, indent=4))

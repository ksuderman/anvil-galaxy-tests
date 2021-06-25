import json
import sys
args = sys.argv

with open(args[1], "r") as f:
    contents = json.load(f)

with open(args[2], "r") as f:
    second = json.load(f)

contents["tests"].extend(second["tests"])

cleaned = {}
for m in contents['tests']:
    l = cleaned.get(m['id'], [])
    l.append(m)
    cleaned[m['id']] = l
for k in cleaned.keys():
    if len(cleaned[k]) > 1:
        if cleaned[k][0].get('data', {}).get('status') == cleaned[k][1].get('data', {}).get('status') and cleaned[k][0].get('data', {}).get('execution_problem') == cleaned[k][1].get('data', {}).get('execution_problem'):
              cleaned[k] = [cleaned[k][1]]
        elif 'unreachable' in cleaned[k][0].get('data', {}).get('execution_problem', '') or 'aborted' in cleaned[k][0].get('data', {}).get('execution_problem', ''):
            cleaned[k] = [cleaned[k][1]]
        elif 'unreachable' in cleaned[k][1].get('data', {}).get('execution_problem', '') or 'aborted' in cleaned[k][1].get('data', {}).get('execution_problem', ''):
            cleaned[k] = [cleaned[k][0]]
        elif cleaned[k][0].get('data', {}).get('status') == 'success':
            cleaned[k] = [cleaned[k][0]]
        elif cleaned[k][1].get('data', {}).get('status') == 'success':
            cleaned[k] = [cleaned[k][1]]
        elif cleaned[k][0].get('data', {}).get('status') == 'error' and cleaned[k][1].get('data', {}).get('status') != 'error':
            cleaned[k] = [cleaned[k][1]]
        elif cleaned[k][1].get('data', {}).get('status') == 'error' and cleaned[k][0].get('data', {}).get('status') != 'error':
            cleaned[k] = [cleaned[k][0]]
        elif cleaned[k][1].get('data', {}).get('status') == 'error' and cleaned[k][0].get('data', {}).get('status') == 'error':
            if len(cleaned[k][0].get('data', {}).get('execution_problem')) > len(cleaned[k][1].get('data', {}).get('execution_problem')):
                cleaned[k] = [cleaned[k][0]]
            else:
                cleaned[k] = [cleaned[k][1]]
        else:
            print("unhandled case")
            print(str(k))
            print(cleaned[k][0].get('data', {}).get('status'))
            print(cleaned[k][1].get('data', {}).get('status'))
            print(cleaned[k][0].get('data', {}).get('execution_problem'))
            print(cleaned[k][1].get('data', {}).get('execution_problem'))
end = []
for k in cleaned.keys():
    if len(cleaned[k]) == 1:
        end.append(cleaned[k][0])
    else:
        print(k)
        print(cleaned[k])

contents['tests'] = end

with open(args[3], 'w') as f:
    json.dump(contents, f)


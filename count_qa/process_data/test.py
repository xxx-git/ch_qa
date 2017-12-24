import json

file = 'tag_rel_dict'
with open(file) as fin:
    ll = json.load(fin, encoding='utf-8')
print(ll)
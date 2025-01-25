import ast
from ossapi import Ossapi
api = Ossapi("[redacted]","[redacted]")
has_diff_list = []

with open("DMCA_mapper_dict.txt", 'r') as file:
    file_content = file.read()
    dmca_player = ast.literal_eval(file_content)
    
with open("unchecked.txt", 'r') as file:
    file_content = file.read()
    mapper_dict = ast.literal_eval(file_content)
    
for k,v in mapper_dict.items():
    try:
        str_change = False
        user = api.user(v)
        k = user.username
        if ' ' in k: # spaces are pain
            continue
        if user.previous_usernames: # skip those with previous username for now bc it's an additional headache
            continue
        if k.endswith('_old'):
            search_prompt = k.replace('_old','')
            str_change = True
        if k.startswith('-'):
            search_prompt = '/' + k + '/'
            str_change = True
        if not str_change:
            search_prompt = k
        result = (api.search_beatmapsets(query=search_prompt,explicit_content='show',sort="ranked_asc").total)
        compare = user.ranked_and_approved_beatmapset_count + user.loved_beatmapset_count + user.guest_beatmapset_count
        
        if k in dmca_player:
            compare -= dmca_player[k] # minus how many dmca'd maps are there in a profile
        diff = result - compare
        if diff < 500 and diff != 0: # there might be some maps with gds that aren't tagged properly or a mapper has a name change that were removed
            has_diff_list.append(k)
            print(f'{k}   {result}   {compare}   diff : {diff}')
    except:
        break
    
print(has_diff_list)

# I still have to make a script for cases where
# mapper has previous username
# mapper has previous username but removed it
# common noun names
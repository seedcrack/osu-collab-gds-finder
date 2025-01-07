import ast
from ossapi import Ossapi
api = Ossapi("[redacetd]","[redacted]")

with open("DMCA_mapper_dict.txt", 'r') as file: # I got this from the other respo I made
    file_content = file.read()
    dmca_player = ast.literal_eval(file_content)
    
with open("unchecked.txt", 'r') as file:
    file_content = file.read()
    search_prompt = ast.literal_eval(file_content)
    
for k,v in search_prompt.items():
    if (api.user(v)).previous_usernames or k.endswith('_old'): # skip those with previous username for now bc it's an additional headache
        continue
    result = (api.search_beatmapsets(query=k).total)
    user = api.user(v)
    compare = user.ranked_and_approved_beatmapset_count + user.loved_beatmapset_count + user.guest_beatmapset_count
    if k in dmca_player:
        compare -= dmca_player[k] # minus how many dmca'd maps are there in a profile
    if compare > result: # there might be some maps with gds that aren't tagged properly or a mapper has a name change that were removed
        continue  # skipped for now bc it's a headache
    diff = result - compare
    if diff < 200 and compare != result: # capped at 200 bc it's unreasonable and most likely mean that the name is a common noun
        print(f'{k}   {result}   {compare}   diff : {diff}')

# I still have to make a script for cases where
# mapper has previous username
# mapper has previous username but removed it
# common noun names
        

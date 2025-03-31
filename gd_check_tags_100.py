# This is probably the final ver.

import ast
import webbrowser
from ossapi import Ossapi
api = Ossapi("[redacted]","[redacted]")
blacklisted_maps = {754402, 814850, 597000, 445835, 714729, 794048, 1080535, 396643, 973421, 1670545, 283595, 32883, 685539, 1524066, 50777, 592397, 526397, 5918, 803906, 63732, 118768}

with open("tags_dict.txt", 'r') as file:
    file_content = file.read()
    tags_dict = ast.literal_eval(file_content)
    
with open("tags_dict_list.txt", 'r') as file2:
    file_content = file2.read()
    tags_dict_list = ast.literal_eval(file_content)
    
with open("removed_names_dict.txt", 'r') as file3:
    file_content = file3.read()
    removed_names_dict = ast.literal_eval(file_content)

def remove_bn(mappers,noms):
    out = []
    bn = []
    for info in noms:
        bn.append(info.user_id)
    for info in mappers:
        mapper = info['username']
        mapper_id = info['id']
        if mapper_id not in bn:
            out.append(mapper)
    return out

while True: # I think this is the best I can do without some over the top stuff
    n = 1
    user_gd_set = set()
    user_ranked_set = set()
    user_loved_set = set()
    username_list = []
    result = set()
    difference = set()
    temp_set = set()
    username_input = (input('username : ').replace("\\",'').replace("'",'').strip()) # miss input
    if username_input == 'end':
        break
    mapper = api.user(username_input)
    u_id = mapper.id
    username_list = mapper.previous_usernames
    username_list.append(username_input)
    username_set = set(username_list)
    
    if username_input in removed_names_dict:
        username_set |= removed_names_dict[username_input]
    for i in username_set:
        if ' ' in i:
            i = i.replace(' ', '_')
            temp_set.add(i)
            i = i.replace('_','')
            temp_set.add(i)       
    username_set |= temp_set
    
    for i in username_set:
        if ' ' not in i:
            print(i)
            for k,tag in tags_dict_list.items():
                if i.lower() in tag:
                    result.add(k)
        else:
            print(i)
            for k,tag in tags_dict.items():
                if i.lower() in tag:
                    result.add(k)
            
    user_gd = (api.user_beatmaps(u_id,type='guest',limit=500)) # for some reason it can't go above 100
    user_ranked = (api.user_beatmaps(u_id,type='ranked',limit=500))
    user_loved = (api.user_beatmaps(u_id,type='loved',limit=500))
    for i in user_gd:
        user_gd_set.add(i.id)
    for i in user_ranked:
        user_ranked_set.add(i.id)
    for i in user_loved:
        user_loved_set.add(i.id)
        
    leftover_gd_set = result - (user_gd_set | user_ranked_set | user_loved_set | blacklisted_maps)
        
    # alternative algorithm which uses related users instead
    # The runtime is so shit
    for i in leftover_gd_set:
        beatmap = api.beatmapset(i)
        related_users = beatmap.related_users
        noms = beatmap.current_nominations
        mappers = remove_bn(related_users,noms)
        if username_input not in mappers:
            difference.add(i)
    
    for i in difference:
        url = 'https://osu.ppy.sh/beatmapsets/' + str(i) + '/'
        print(url)
        if n < 11: # prevents getting 429'd
            webbrowser.open(url)
        if n == 10:
            print('429 preventer activated')
        n += 1
            
# basically what this does is it prints out whatever is in the search result but not in the user's gd


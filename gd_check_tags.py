# This is probably the final ver.

import ast
import webbrowser
from ossapi import Ossapi
api = Ossapi("[redacted]","[redacted]")
more_than_100_gds = ['Alace', 'ignorethis', 'Andrea', 'climbb65588', 'lepidopodus', 'kanpakyin', 'OnosakiHito', 'riffy', 'bossandy', 'No_Gu', '-kevincela-', 'fanzhen0019', 'Sekai', 'Laurier', 'alacat', 'Kyouren', 'Hinsvar', 'Skystar', 'Flask', 'Xinely', 'Gero', 'pregnant_man', 'Irreversible', 'Momochikun', 'toybot', 'HabiHolic', 'yf_bmp', 'IamKwaN', 'Nardoxyribonucleic', 'Rizia', 'Spectator', 'captin1', 'Delis', 'Annabel', 'KoldNoodl', 'pishifat', 'Kibbleru', 'Amateurre', 'arronchu1207', 'Karen', 'Pata-Mon', 'Garden', 'Critical_Star', 'Ayesha Altugle', 'Ascendance', 'JBHyperion', 'Dailycare', 'Sotarks', 'Akitoshi', 'SnowNiNo_', 'Djulus', 'Affirmation', 'Lasse', 'Irohas', 'Gorou', 'Kalibe', 'A r M i N', 'Agatsu', 'Mir', 'kowari', 'Kujinn', 'Nao Tomori', 'schoolboy', 'Genjuro', 'Kojio', 'gaston_2199', 'Mirash', 'Trynna', 'AirinCat', 'PandaHero', 'Hivie', 'Faputa', 'Jemzuu', 'Pepekcz', 'Xen', 'Tachibana_', 'Mocaotic', 'Shiyun', 'AsuKow', 'iRedi', 'Ryxliee']
# actually I need centurian mapper list but I'm lazy to make one
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

while True: # I think this is the best I can do without some over the top stuff
    n = 1
    total_search_amount = 0
    user_gd_set = set()
    user_ranked_set = set()
    user_loved_set = set()
    username_list = []
    result = set()
    temp_set = set()
    username_result_dict = {}
    username_input = input('username : ').replace("\\",'').replace("'",'').strip() # miss input
    print('')
    if username_input == 'end':
        break
    if username_input in more_than_100_gds:
        print('This guy has more than 100 gds')
        continue
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
        username_result_dict[i] = set()
        
    for k,v in username_result_dict.items():
        if ' ' not in k:
            individual_result = set()
            for map_id,tag in tags_dict_list.items():
                if k.lower() in tag and banned_tag.lower() not in tag:
                    username_result_dict[k].add(map_id)
                    individual_result.add(map_id)
        else:
            individual_result = set()
            for map_id,tag in tags_dict.items():
                if k.lower() in tag and banned_tag.lower() not in tag:
                    username_result_dict[k].add(map_id)
                    individual_result.add(map_id)
            
    user_gd = api.user_beatmaps(u_id,type='guest',limit=500) # for some reason it can't go above 100
    user_ranked = api.user_beatmaps(u_id,type='ranked',limit=500)
    user_loved = api.user_beatmaps(u_id,type='loved',limit=500)
    for i in user_gd:
        user_gd_set.add(i.id)
    for i in user_ranked:
        user_ranked_set.add(i.id)
    for i in user_loved:
        user_loved_set.add(i.id)
        
    for k,v in username_result_dict.items():
        result |= v
        
    left_over = result - (user_gd_set | user_ranked_set | user_loved_set | blacklisted_maps)
    
    for k,v in username_result_dict.items():
        username_result_dict[k] &= left_over
        
    print('Names       amount') # too lazy to set up pandas
    for k,v in username_result_dict.items():
        print(f'{k}     {len(v)}')
        total_search_amount += len(v)
        
    if total_search_amount != len(left_over):
        print('WARNING: Some beatmaps have multiple aliases of the mapper in the tags')
        

    for i in left_over:
        url = 'https://osu.ppy.sh/beatmapsets/' + str(i) + '/'
        print(url)
        if n % 10 != 0: # prevents getting 429'd
            webbrowser.open(url)
        else:
            input_pause = input('''enter to continue, type 'end' to abort: ''')
            if input_pause == 'end':
                break
        n += 1
        
    print('DONE')
# basically what this does is it prints out whatever is in the search result but not in the user's gd

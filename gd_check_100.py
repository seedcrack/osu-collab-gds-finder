import webbrowser
from ossapi import Ossapi
api = Ossapi("[redacted]","[redacted]")

def search_by_month(search_compare,year):
    temp_list = []
    for i in range(1,13): # 12 months in a year
        search_prompt = search_compare + ' ranked=' + year + '-' + str(i)
        search_result = api.search_beatmapsets(query=search_prompt, explicit_content='show', sort="ranked_desc")
        total_check = search_result.total
        if total_check > 50:
            print('Holy fuck, does this guy have no life?') # seriously I don't think you can rank 50 maps or gds in a month
        for i in search_result.beatmapsets:
            temp_list.append(i)
    return temp_list

def search_by_year(search_compare):
    result = []
    for i in range(7,25): # from 2007 to 2024
        if i < 10:
            year = '200' + str(i)
        else:
            year = '20' + str(i)
        search_prompt = search_compare + ' ranked=' + year
        search_result = api.search_beatmapsets(query=search_prompt, explicit_content='show', sort="ranked_desc")
        total_check = search_result.total
        if total_check > 50:
            beatmaps = search_by_month(search_compare,year)
        else:
            beatmaps = search_result.beatmapsets
        for i in beatmaps:
            result.append(i)
    return result

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

while True: # this is still manual lol
    n = 1
    user_gd_links = []
    search_gd_links = []
    difference = []
    leftover_gd_links = []
    username_input = input('username : ').strip() # automation one day
    if username_input == 'end':
        break
    u_id = api.user(username_input).id
    if username_input.startswith('-'):
        search_compare = '/' + username_input + '/'
    else:
        search_compare = username_input
    search_prompt = search_compare + ' ranked<2024-12-09'
    search_result = api.search_beatmapsets(query=search_prompt, explicit_content='show', sort="ranked_desc")
    total_check = search_result.total
    if total_check > 50: # You need a special method for this case
        result = search_by_year(search_compare)
    else:
        result = search_result.beatmapsets
    for i in result:
        tags = i.tags
        if i.user_id != u_id and username_input.lower() in tags:
            search_gd_links.append(i.id) # append IDs that is potentially a gd
    
    user_gd = (api.user_beatmaps(u_id,type='guest',limit=500)) # for some reason it can't go above 100
    for i in user_gd:
        user_gd_links.append(i.id)
    for i in search_gd_links:
        if i not in user_gd_links:
            leftover_gd_links.append(i)
        
    # alternative algorithm which uses related users instead
    # The runtime is so shit
    for i in leftover_gd_links:
        beatmap = api.beatmapset(i)
        related_users = beatmap.related_users
        noms = beatmap.current_nominations
        mappers = remove_bn(related_users,noms)
        if username_input not in mappers:
            difference.append(i)
    
    for i in difference:
        url = 'https://osu.ppy.sh/beatmapsets/' + str(i) + '/'
        print(url)
        if n < 11: # prevents getting 429'd
            webbrowser.open(url)
        if n == 10:
            print('429 preventer activated')
        n += 1
            
# basically what this does is it prints out whatever is in the search result but not in the user's gd
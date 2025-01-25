import ast
import webbrowser
from ossapi import Ossapi
api = Ossapi("[redacted]","[redacted]")
more_than_100_gds = ['Alace', 'ignorethis', 'Andrea', 'climbb65588', 'lepidopodus', 'kanpakyin', 'OnosakiHito', 'riffy', 'bossandy', 'No_Gu', '-kevincela-', 'fanzhen0019', 'Sekai', 'Laurier', 'alacat', 'Kyouren', 'Hinsvar', 'Skystar', 'Flask', 'Xinely', 'Gero', 'pregnant_man', 'Irreversible', 'Momochikun', 'toybot', 'HabiHolic', 'yf_bmp', 'IamKwaN', 'Nardoxyribonucleic', 'Rizia', 'Spectator', 'captin1', 'Delis', 'Annabel', 'KoldNoodl', 'pishifat', 'Kibbleru', 'Amateurre', 'arronchu1207', 'Karen', 'Pata-Mon', 'Garden', 'Critical_Star', 'Ayesha', 'Ascendance', 'JBHyperion', 'Dailycare', 'Sotarks', 'Akitoshi', 'SnowNiNo_', 'Djulus', 'Affirmation', 'Lasse', 'Irohas', 'Gorou', 'Kalibe', 'A', 'Agatsu', 'Mir', 'kowari', 'Kujinn', 'Nao', 'schoolboy', 'Genjuro', 'Kojio', 'gaston_2199', 'Mirash', 'Trynna', 'AirinCat', 'PandaHero', 'Hivie', 'Faputa', 'Jemzuu', 'Pepekcz', 'Xen', 'Tachibana_', 'Mocaotic', 'Shiyun', 'AsuKow', 'iRedi', 'Ryxliee']

with open("unchecked.txt", 'r') as file:
    file_content = file.read()
    difference_list = ast.literal_eval(file_content)

def search_by_month(search_compare,year):
    temp_list = []
    for i in range(1,13): # 12 months in a year
        search_prompt = search_compare + ' ranked=' + year + '-' + str(i)
        search_result = api.search_beatmapsets(query=search_prompt, explicit_content='show', sort="ranked_asc")
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
        search_result = api.search_beatmapsets(query=search_prompt, explicit_content='show', sort="ranked_asc")
        total_check = search_result.total
        if total_check > 50:
            beatmaps = search_by_month(search_compare,year)
        else:
            beatmaps = search_result.beatmapsets
        for i in beatmaps:
            result.append(i)
    return result

for username_input in difference_list:
    user_gd_links = []
    search_gd_links = set()
    difference_check = []
    if username_input in more_than_100_gds:
        continue
    u_id = api.user(str(username_input)).id
    if username_input.startswith('-'):
        search_compare = '/' + username_input + '/' # osu! search algo sucks lol
    else:
        search_compare = username_input
    search_prompt = search_compare + ' ranked<2024-12-09'
    search_result = api.search_beatmapsets(query=search_prompt, explicit_content='show', sort="ranked_asc")
    total_check = search_result.total
    if total_check == 0:
        continue
    if total_check > 50: # You need a special method for this case
        result = search_by_year(search_compare)
    else:
        result = search_result.beatmapsets
    for i in result:
        tags = i.tags
        if i.user_id != u_id and username_input.lower() in tags:
            search_gd_links.add(i.id) # append IDs that is potentially a gd
            
    user_gd = (api.user_beatmaps(u_id,type='guest',limit=500)) # for some reason it can't go above 100
    for i in user_gd:
        user_gd_links.append(i.id)
    
    for i in search_gd_links:
        if i not in user_gd_links:
            difference_check.append(i)
            
    if difference_check:
        print(f'{username_input}     {len(difference_check)}')
            
# basically what this does is it prints out whatever is in the search result but not in the user's gd

import webbrowser
from ossapi import Ossapi
api = Ossapi("[redacted]","[redacted]")

# This code only works if the search result is lower than 50

while True: # this is still manual lol
    user_gd_links = []
    search_gd_links = []
    search_compare = input('username : ') # automation one day
    if search_compare == 'end':
        break
    u_id = int(input('ID : '))
    result = api.search_beatmapsets(query=search_compare).beatmapsets
    for i in result:
        if i.user_id != u_id: # this only exclude the mapper being the host
            search_gd_links.append(i.id) # append IDs that is potentially a gd
            
    user_gd = (api.user_beatmaps(u_id,type='guest',limit=500)) # for some reason it can't go above 100
    for i in user_gd:
        user_gd_links.append(i.id)
    
    for i in search_gd_links:
        if i not in user_gd_links:
            url = 'https://osu.ppy.sh/beatmapsets/' + str(i) + '/'
            print(url)
            webbrowser.open(url)
    # basically what this does is it prints out whatever is in the search result but not in the user's gd
    
# I still have to make a script for cases where
# mapper has more than 100 gds
# mapper has more than 50 search results
# this script should only search by tags and not any other thing (having names in songs' title can throw away the search result)

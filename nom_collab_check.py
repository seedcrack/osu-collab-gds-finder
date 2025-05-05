from ossapi import Ossapi
import ast
api = Ossapi("[redacted]","[redacted]")

with open("unchecked_nom_collab.txt", 'r') as file:
    file_content = file.read()
    all_map = ast.literal_eval(file_content)

def blatant_nom_error(beatmap,bn,mappers,host):
    if host == 2:
        return False
    for i in mappers:
        if i in bn:
            return True
    return False

def no_host_collab(beatmap,mappers,host):
    diff_name = beatmap.version
    if 'collab' in diff_name.lower():
        if len(mappers) == 1 and list(mappers)[0] != host:
            return True
    return False

nom_error = set()
host_collab_fix = set()

for i in all_map:
    try:
        map_id = []
        bn = []
        map_set = api.beatmapset(i)
        host = map_set.user_id
        noms = map_set.current_nominations
        for info in noms:
            bn.append(info.user_id)
        maps = map_set.beatmaps
        for j in maps:
            map_id.append(j.id)
        for j in map_id:
            mappers = set()
            beatmap = api.beatmap(j)
            raw_mappers = beatmap.owners
            for k in raw_mappers:
                mappers.add(k.id)
            if no_host_collab(beatmap,mappers,host):
                print('collab found')
                host_collab_fix.add(i)
            
            if blatant_nom_error(beatmap,bn,mappers,host):
                print('weird nom found')
                nom_error.add(i)
    except:
        print(f'current ID : {i}')
        break

print(host_collab_fix)
print(nom_error)
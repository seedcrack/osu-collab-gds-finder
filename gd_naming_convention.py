from ossapi import Ossapi
import ast
api = Ossapi("[redacted]","[redacted]")
deleted_user = ['jakads', 'kloyd', 'asami', '-lolist-', 'riven', 'kqrth']

with open("unchecked_naming convention.txt", 'r') as file:
    file_content = file.read()
    all_map = ast.literal_eval(file_content)
    
with open("custom_diffname_owner_dict.txt", 'r') as file1:
    file_content = file1.read()
    custom_diffname_owner_dict = ast.literal_eval(file_content)
    
with open("custom_diffname_beatmap_dict.txt", 'r') as file2:
    file_content = file2.read()
    custom_diffname_beatmap_dict = ast.literal_eval(file_content)
    
with open("custom_diffname_beatmapset_dict.txt", 'r') as file3:
    file_content = file3.read()
    custom_diffname_beatmapset_dict = ast.literal_eval(file_content)

for i in all_map:
    try:
        map_set = api.beatmapset(i)
        maps = map_set.beatmaps
        for j in maps:
            mappers = set()
            diff_name = (j.version).lower()
            raw_mappers = j.owners
            for k in raw_mappers:
                mappers.add(k.username)
            tuple_mappers = tuple(sorted(mappers))
            if "'s" in diff_name:
                diff_name_processed = diff_name.split("'s")
                supposed_owner = diff_name_processed[0].strip()
                        
                if supposed_owner not in custom_diffname_owner_dict:
                    custom_diffname_owner_dict[supposed_owner] = set()
                    custom_diffname_owner_dict[supposed_owner].add(tuple_mappers)
                    custom_diffname_beatmap_dict[supposed_owner] = set()
                    custom_diffname_beatmap_dict[supposed_owner].add(j.id)
                    custom_diffname_beatmapset_dict[supposed_owner] = set()
                    custom_diffname_beatmapset_dict[supposed_owner].add(map_set.id)
                    
                elif tuple_mappers not in custom_diffname_owner_dict[supposed_owner]:
                    custom_diffname_owner_dict[supposed_owner].add(tuple_mappers)
                    custom_diffname_beatmap_dict[supposed_owner].add(j.id)
                    custom_diffname_beatmapset_dict[supposed_owner].add(map_set.id)
                else:
                    custom_diffname_beatmap_dict[supposed_owner].add(j.id)
                    custom_diffname_beatmapset_dict[supposed_owner].add(map_set.id)
                    
            if "s'" in diff_name:
                diff_name_processed = diff_name.split("'")
                supposed_owner = diff_name_processed[0].strip()
                
                if len(raw_mappers) == 1:
                    if map_set.user_id == (raw_mappers[0]).id and supposed_owner not in deleted_user:
                        print(f'auto gd sucks : {i}')
                        
                if supposed_owner not in custom_diffname_owner_dict:
                    custom_diffname_owner_dict[supposed_owner] = set()
                    custom_diffname_owner_dict[supposed_owner].add(tuple_mappers)
                    custom_diffname_beatmap_dict[supposed_owner] = set()
                    custom_diffname_beatmap_dict[supposed_owner].add(j.id)
                    custom_diffname_beatmapset_dict[supposed_owner] = set()
                    custom_diffname_beatmapset_dict[supposed_owner].add(map_set.id)
                    
                elif tuple_mappers not in custom_diffname_owner_dict[supposed_owner]:
                    custom_diffname_owner_dict[supposed_owner].add(tuple_mappers)
                    custom_diffname_beatmap_dict[supposed_owner].add(j.id)
                    custom_diffname_beatmapset_dict[supposed_owner].add(map_set.id)
                    
                else:
                    custom_diffname_beatmap_dict[supposed_owner].add(j.id)
                    custom_diffname_beatmapset_dict[supposed_owner].add(map_set.id)
                    
    except:
        break
        
print(custom_diffname_owner_dict)
print('\n')
print(custom_diffname_beatmap_dict)
print('\n')
print(custom_diffname_beatmapset_dict)
print('\n')
print(f'current ID {i}')
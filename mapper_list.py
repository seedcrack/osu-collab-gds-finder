import ast
from ossapi import Ossapi
print('The script is currently running DO NOT SHUT DOWN')

with open("all_in_one.txt", 'r') as file:
    file_content = file.read()
    data = ast.literal_eval(file_content) # this is a list

api = Ossapi("34837","TkpakvCBFyBx8cObjqSP9809Uk31JE2b17KseMYJ")
dict_of_mapper = {}
mapper_list = []

for i in data:
    try:
        bn = []
        beatmap = api.beatmapset(i)
        mappers = beatmap.related_users
        noms = beatmap.current_nominations
        for info in noms:
            bn.append(info.user_id)
        for info in mappers:
            mapper = info['username']
            mapper_id = info['id']
            if mapper_id not in bn:
                if mapper not in dict_of_mapper:
                    dict_of_mapper[mapper] = mapper_id
                if mapper not in mapper_list:
                    mapper_list.append(mapper)
    except:
        print(f'the current ID is {i}')
        break

print('done')
print(dict_of_mapper)
print()
print(mapper_list)
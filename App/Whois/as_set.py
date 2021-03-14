from re import match

def origins_and_sets(members: list, as_set_name: str) -> tuple:
    as_set_list = list()
    origins_list = list()
    for member in members:
        # sanitize removing comments
        # and removing spaces in the end
        member = member.split('#')[0].strip()
        member = member.strip()
        
        if member == as_set_name: continue
        
        if match('AS-|AS.*:AS-', member):
            as_set_list.append(member)
        else:
            origins_list.append(member)
            
    return (origins_list, as_set_list)
            

def as_set_to_dict(irr_object: str) -> dict:
    lines = irr_object.split('\n')
    new_object = dict()
    as_set_name = ''
    
    for line in lines:
        if line == '': continue
        try:
            header, data = line.split(sep=':', maxsplit=1)
        except ValueError:
            continue
        
        data = data.strip()
        
        if header == 'as-set':
            as_set_name = data
        
        if header == 'members':
            # o primeiro item da tupla sera uma lista de origens
            # o segundo item da tupla representa outros as-sets presentes
            new_members = tuple()
            
            members = origins_and_sets(data.split(','), as_set_name)
            
            if header not in new_object:
                new_object[header] = members
            else:
                new_object[header][0].extend(members[0])
                new_object[header][1].extend(members[1])
            
        else:
            new_object[header] = data
            
    # sometimes as-set don't have any member,
    # so i create a empty member just to later representations
    if 'members' not in new_object:
        new_object['members'] = [list(), list()]    
        
    return new_object
def all_fields(sch, prefix='', is_array = False):
    ret = set()
    for key, value in sch.items():
        if value['type'] == 'dict':
            ret = ret | all_fields(value['schema'], key)
        elif value['type'] == 'list':
            ret = ret | all_fields(value['schema'], key, is_array=True)
        else:
            if prefix == '':
                ret.add(key)
            elif is_array:
                ret.add(prefix + '.$.' + key)
            else:
                ret.add(prefix + '.' + key)
    return ret

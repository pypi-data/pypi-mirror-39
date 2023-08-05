def all_fields(sch, prefix=''):
    ret = set()
    for key, value in sch.items():
        if value['type'] == 'dict':
            ret = ret | all_fields(value['schema'], key)
        else:
            if prefix == '':
                ret.add(key)
            else:
                ret.add(prefix + '.' + key)
    return ret

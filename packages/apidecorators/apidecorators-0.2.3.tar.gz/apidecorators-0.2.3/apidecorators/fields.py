def all_fields(sch, prefix='', is_array=False, without=None):
    if without is None:
        without = []
    ret = set()
    for key, value in sch.items():
        if key in without:
            continue
        if value['type'] == 'dict':
            if prefix == '':
                next_prefix = key
            else:
                next_prefix = prefix + '.' + key
            ret = ret | all_fields(value['schema'], prefix=next_prefix)
        elif value['type'] == 'list':
            next_prefix = key + '.$'
            ret = ret | all_fields(value['schema'], prefix=next_prefix, is_array=True)
        else:
            if prefix == '':
                ret.add(key)
            else:
                ret.add(prefix + '.' + key)
    return ret

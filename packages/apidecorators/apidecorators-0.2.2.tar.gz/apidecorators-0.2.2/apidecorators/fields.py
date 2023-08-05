def all_fields(sch, prefix='', is_array=False, without=None):
    if without is None:
        without = []
    ret = set()
    for key, value in sch.items():
        if key in without:
            continue
        if value['type'] == 'dict':
            ret = ret | all_fields(value['schema'], prefix=key)
        elif value['type'] == 'list':
            ret = ret | all_fields(value['schema'], prefix=key, is_array=True)
        else:
            if prefix == '':
                ret.add(key)
            elif is_array:
                ret.add(prefix + '.$.' + key)
            else:
                ret.add(prefix + '.' + key)
    return ret

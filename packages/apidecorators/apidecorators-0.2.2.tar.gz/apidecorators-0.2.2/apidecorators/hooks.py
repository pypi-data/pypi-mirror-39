_on_insert = {}
_on_update = {}
_on_push = {}
_on_pull = {}

#marcalos como async si es que al final decido usarlos

def on_insert(col):
    def decorator(f):
        _on_insert[col] = f
        return f
    return decorator

def on_update(col):
    def decorator(f):
        _on_update[col] = f
        return f
    return decorator

def on_push(col):
    def decorator(f):
        _on_push[col] = f
        return f
    return decorator

def on_pull(col):
    def decorator(f):
        _on_pull[col] = f
        return f
    return decorator
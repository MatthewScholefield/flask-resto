def recursive_merge(a, b):
    """Returns a generator of a merged dict of a and b"""
    for k in set(a.keys()) | set(b.keys()):
        if k in a and k in b:
            if isinstance(a[k], dict) and isinstance(b[k], dict):
                yield k, dict(recursive_merge(a[k], b[k]))
            else:
                yield k, b[k]
        elif k in a:
            yield k, a[k]
        else:
            yield k, b[k]

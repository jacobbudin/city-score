NULL_DISPLAY = '?'

def dimension(title):
    def decorator(f):
        def wrapper(*args, **kwargs):
            if len(args) == 0:
                def inner_wrapper(*args):
                    value = f(*args, **kwargs)
                    if value is None:
                        return NULL_DISPLAY
                    return value
                inner_wrapper.title = title.format(**kwargs)
                return inner_wrapper
            value = f(*args, **kwargs)
            if value is None:
                return NULL_DISPLAY
            return value
        wrapper.title = title
        return wrapper
    return decorator

def scorer(title):
    def decorator(f):
        def wrapper(*args, **kwargs):
            weight = kwargs.get('weight', 1)
            if 'weight' in kwargs:
                del kwargs['weight']
            def inner_wrapper(*inner_args, **inner_kwargs):
                inner_kwargs.update(kwargs)
                return round(f(*inner_args + args, **inner_kwargs) * weight)
            return inner_wrapper
        wrapper.title = title
        return wrapper
    return decorator

def criterion(title):
    def decorator(f):
        def wrapper(*args, **kwargs):
            def inner_wrapper(*inner_args, **inner_kwargs):
                inner_kwargs.update(kwargs)
                return f(*inner_args + args, **inner_kwargs)
            return inner_wrapper
        wrapper.title = title
        return wrapper
    return decorator
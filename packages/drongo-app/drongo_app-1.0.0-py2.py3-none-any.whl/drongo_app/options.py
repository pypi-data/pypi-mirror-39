def evaluate(options, env):
    if isinstance(options, str):
        try:
            return options.format(**env)
        except KeyError:
            return None

    elif isinstance(options, dict):
        if '$or' in options:
            result = None
            for item in options['$or']:
                item = evaluate(item, env)
                result = result or item
            return result
        else:
            result = {}
            for k, v in options.items():
                result[k] = evaluate(v, env)
            return result
    else:
        return options

    return None

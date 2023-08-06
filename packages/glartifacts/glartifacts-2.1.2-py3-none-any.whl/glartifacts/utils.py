import functools

def indent(val, amount=2):
    if not val:
        return val
    space = " "*amount
    return val.strip().replace("\n", "\n"+space)

def tabulate(rows, sortby=None):
    col_sizes = autosize(rows)
    print_row(rows.pop(0), col_sizes)
    if 'key' in sortby:
        sortby = [sortby]
    for term in sortby:
        rows.sort(key=term['key'], reverse=term.get('reverse', False))

    print_spacer(col_sizes)
    for r in rows:
        print_row(r, col_sizes)

def print_row(row, col_sizes):
    for i, col in enumerate(row):
        print(str(col).ljust(col_sizes[i]), end="")
    print("")

def print_spacer(col_sizes):
    spacer = []
    for c in col_sizes:
        spacer.append("-"*(c-1))
    print_row(spacer, col_sizes)

def autosize(rows):
    sizes = []
    for r in rows:
        col_count = len(r) - len(sizes)
        if col_count > 0:
            sizes.extend([0]*col_count)

        for i, col in enumerate(r):
            col = str(col)
            if len(col) >= sizes[i]:
                sizes[i] = len(col)+1

    return sizes

def humanize_size(size):
    size_format = '{:.2f} {}'
    for unit in ['B', 'KiB', 'MiB']:
        if size < 1024:
            return size_format.format(size, unit)

        size = size / 1024

    return size_format.format(size, "GiB")

def humanize_datetime(datetime):
    return datetime.date().isoformat() + " " + datetime.strftime('%X')

def memoize(key=None):
    def decorator(func):
        cache = {}

        @functools.wraps(func)
        def cacheable(*args):
            # reduce arguments using cache key callable
            cache_args = key(args) if key else args

            cache_key = '|'.join([str(a) for a in cache_args])
            if cache_key in cache:
                return cache[cache_key]

            result = func(*args)
            cache[cache_key] = result
            return result

        return cacheable

    return decorator

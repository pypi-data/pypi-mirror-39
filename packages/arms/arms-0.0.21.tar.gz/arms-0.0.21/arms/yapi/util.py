import re


def prefix(lines, f):
    for line in lines:
        tmp = f(line)
        if tmp:
            yield tmp
        else:
            break


def extract_include(line):
    if not line: return None
    if line.startswith('`:include ') and line[-1] == '`':
        return line[1:-1].split(':include', 1)[-1].strip()
    else:
        return None


def lined_group(lines, starter, ender):
    def get(p):
        return lines[p] if p < len(lines) else None

    def single_group(p):
        next = ''
        isGrouping = False
        first = last = None
        for i in range(p, len(lines) + 1):
            prev, next = next, get(i)
            if not isGrouping and starter(prev, next):
                first, isGrouping = i, True
            elif isGrouping and ender(prev, next):
                last = i
                return (first, last)
        return (first, last)

    i = 0
    while True:
        first, last = single_group(i)
        if first is None or last is None:
            break
        yield lines[first:last]
        i = last


def mdtitle_level(line):
    """
    >>> mdtitle_level("#### hehe")
    4
    >>> mdtitle_level("#haha")
    1
    >>> mdtitle_level(".#haha")
    0
    """
    segs = re.findall("^#+", line)
    return len(segs[0]) if segs else 0


def big_mdtitle_group(lines):
    for group in lined_group(
            lines,
            lambda _, next: next is not None and mdtitle_level(next) == 1,
            lambda _, next: next is None or mdtitle_level(next) == 1):
        yield group


def small_mdtitle_group(lines):
    for group in lined_group(
            lines,
            lambda _, next: next is not None and mdtitle_level(next) >= 2,
            lambda _, next: next is None or mdtitle_level(next) >= 2):
        yield group


def mdyaml_group(lines):
    for group in lined_group(
            lines,
            lambda _, next: next is not None and next == '```yaml',
            lambda prev, next: next is None or prev == '```'):
        yield group


def pathparam_names(path):
    """
    >>> pathparam_names("/school/{schoolId}")
    ['schoolId']
    >>> pathparam_names("/{school}/{schoolId}")
    ['school', 'schoolId']
    >>> pathparam_names("/schools")
    []
    """
    return re.findall(r'\{([^/]+)\}', path)


def merge_dicts(dicts):
    """
    >>> merge_dicts([{'a':1, 'b':2}, {'c':3, 'b':4}])
    {'a': 1, 'b': 4, 'c': 3}
    """
    ret = {}
    for d in dicts:
        ret.update(d)
    return ret


def parse_comment(value):
    """
    >>> parse_comment('int hehe||22')
    ('int', 'hehe', '22')
    >>> parse_comment('str(50) hehe||\"22\"')
    ('str(50)', 'hehe', '"22"')
    >>> parse_comment('int ||2')
    ('', 'int ', '2')
    """
    if isinstance(value, str) and '||' in value:
        comment, realvalue = value.split('||', 1)
        try:
            pytype, comment = comment.strip().split(None, 1)
        except:
            pytype = ''
        realvalue = realvalue.strip()
    else:
        comment = ''
        realvalue = value
        pytype = str(type(value))
    return pytype, comment, realvalue


def is_utf8mb4(text):
    if hasattr(text, 'decode'):
        text = text.decode('utf8')
    return any(ord(c) >= 256 for c in text)

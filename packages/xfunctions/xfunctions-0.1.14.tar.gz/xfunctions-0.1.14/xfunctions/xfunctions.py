# coding:utf-8


def sleep(t: int):
    import time
    import xprint as xp
    xp.wr(xp.Fore.LIGHTBLUE_EX +
          ' - [' + '-' * t + '] sleep 0/%s s' % t + '\r')
    xp.fi()

    for i in range(1, t + 1):
        time.sleep(1)
        xp.wr(xp.Fore.LIGHTBLUE_EX +
              ' - [' + '>' * i + '-' * (t - i) + '] sleep %s/%s s' % (i, t) + '\r')
        xp.fi()

    xp.fi(inline=False)


def list_unique(source: list):
    r = []
    for el in source:
        if el not in r:
            r.append(el)
    return r


def list_strip(source):
    r = []
    for value in source:
        if isinstance(value, str):
            r.append(value.strip())
        else:
            r.append(value)
    return r


def list_remove(source: list, els=None):
    els = els or ['', None]
    if isinstance(els, list):
        for el in els:
            while el in source:
                source.remove(el)
    else:
        while els in source:
            source.remove(els)

    return source


def list_strip_and_remove(source: list, els=None):
    source = list_strip(source=source)
    source = list_remove(source=source, els=els)
    return source


def path_to(base_dir: str, to: str):
    import os

    to = list_strip_and_remove(to.split('/'))
    r = base_dir
    for p in to:
        r = os.path.join(r, p)

    return r


def read_to_list(path_to_file: str):
    try:
        with open(path_to_file) as f:
            lines = f.read().splitlines()
            lines = list_strip_and_remove(lines)
            return lines
    except FileNotFoundError:
        return []


def path_join(base_dir: str, paths):
    if type(paths) not in [list, str]:
        raise Exception('Param "paths" must be list or str.')

    import os

    if isinstance(paths, str):
        return os.path.join(base_dir, paths)

    r = base_dir
    for p in paths:
        r = os.path.join(r, p)

    return r


def get_dict_by_keys(source, keys: list or dict, default_none: bool = True):
    """
    Get a dict, by keys.

    :param source:
        json_string, dict, or a object
    :param keys:
        list or dict
    :param default_none:
        whether default value is None or ignore it, when the value does not exist.
        available only if keys is a list,
    :return:
        dict
    """
    r = {}
    if isinstance(source, str):
        try:
            import json
            source = json.loads(source)
        except Exception:
            return r
        return get_dict_by_keys(source, keys=keys, default_none=default_none)
    elif isinstance(source, dict):
        if isinstance(keys, list):
            for key in keys:
                if key in source.keys():
                    r[key] = source[key]
                else:
                    if default_none:
                        r[key] = None
        else:
            for key, value in keys.items():
                if key in source.keys():
                    r[key] = source[key]
                else:
                    r[key] = value
    else:
        if isinstance(keys, list):
            for key in keys:
                if default_none:
                    r[key] = getattr(source, key, None)
                elif hasattr(source, key):
                    r[key] = getattr(source, key)
        else:
            for key, value in keys.items():
                r[key] = getattr(source, key, value)
    return r


def x_mix(list_in_list, i=1, target=None):
    # results with '|||'
    ss = []

    if 1 > len(list_in_list):
        return ss

    if 1 == len(list_in_list):
        return list_in_list[0]

    if target is None:
        target = list_in_list[0]

    for s in target:
        for e in list_in_list[i]:
            if not e.strip():
                r = e
            else:
                r = '%s|||%s' % (s, e)

            if r not in ss:
                ss.append(r)

    if i < len(list_in_list) - 1:
        return x_mix(list_in_list, i=i + 1, target=ss)

    # results without '|||'
    results = []
    for row in ss:
        results.append(row.split('|||'))

    return results


def orm_row_may_update_by_dict(row, row_dict: dict):
    should_update = False

    for key, value in row_dict.items():
        if getattr(row, key) != value:
            setattr(row, key, value)
            should_update = True

    if should_update:
        row.save()

    return row


def orm_row_may_update(row, source, keys):
    """
    On-demand Save

    :param row:     orm row
    :param source:  source dict/object
    :param keys:    keys/attributes
    :return:        orm row
    """

    row_dict = get_dict_by_keys(
        source=source,
        keys=keys,
    )

    return orm_row_may_update_by_dict(row, row_dict)


def orm_row_gcu_by_id(orm_model, row_id: int, source, keys):
    """
    Get_or_create, may update

    :param orm_model:   orm model
    :param row_id:      id
    :param source:      source dict/object
    :param keys:        keys/attributes
    :return:            orm row
    """
    row_dict = get_dict_by_keys(
        source=source,
        keys=keys,
    )

    row, created = orm_model.objects.get_or_create(
        id=row_id,
        defaults=row_dict,
    )

    if created:
        return row

    return orm_row_may_update_by_dict(row, row_dict)


def re_findall(patterns, string: str):
    import re

    r = []
    if isinstance(patterns, str) or isinstance(patterns, re.Pattern):
        r = re.findall(patterns, string)
    elif isinstance(patterns, list):
        for pattern in patterns:
            r.extend(re.findall(pattern, string))
    else:
        return r

    return list_unique(r)


def re_find_http_urls(string: str):
    pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    return re_findall(pattern, string)


def markdown_right(s, width: int = 19):
    return '`{s}`'.format(s=s.rjust(width))

# -- encoding: UTF-8 --
def birange(start, end, backwards=False):
    if start > end:
        start, end = end, start
    if backwards:
        return range(end - 1, start, -1)
    else:
        return range(start, end)

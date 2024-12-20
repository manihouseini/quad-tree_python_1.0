def lerp(a, b, t):
    return (1 - t) * a + t * b


def ilerp(a, b, c):
    return (c - a) / (b - a)


def remap(c, a, b, a2, b2):
    return lerp(a2, b2, ilerp(a, b, c))

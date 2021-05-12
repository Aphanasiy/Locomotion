def countdown(start = 10):
    while start > 0:
        yield start
        start -= 1
    return start


def countdown2(start = 10):
    while start >= 0:
        yield start
        start -= 1
    return


from profile import Profile


def profile(func):
    def wrapper(*args, **kwargs):
        profiler = Profile()
        value = profiler.runcall(func, *args, **kwargs)
        profiler.dump_stats('/tmp/{}.prof'.format(func.__name__))
        return value
    return wrapper

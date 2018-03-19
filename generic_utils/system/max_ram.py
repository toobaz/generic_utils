import resource

# https://stackoverflow.com/a/49361727/2858145
def format_size(size):
    # 2**10 = 1024
    power = 2**10
    n = 0
    Dic_powerN = {0 : '', 1: 'kilo', 2: 'mega', 3: 'giga', 4: 'tera'}
    while size > power:
        size /=  power
        n += 1
    return size, Dic_powerN[n]+'bytes'

def max_ram():
    bytes = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1000
    print("Max RAM usage {:.2f} {}".format(*format_size(bytes)))

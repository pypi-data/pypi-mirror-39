from .functions import group

def pretty_print(filter_list):
    cnf = group(filter_list)
    s = ''
    for i, and_group in enumerate(cnf):
        if i > 0:
            s += '\nand '
        for j, or_filt in enumerate(and_group):
            if j > 0:
                s += '\n\tor '
            s += or_filt['name']
    return s



def filename(filter_list):
    cnf = group(filter_list)
    s = ''
    for i, and_group in enumerate(cnf):
        if i > 0:
            s+='_and'
        for j, or_filt in enumerate(and_group):
            s += '_' + or_filt['name']
            if j < len(and_group) - 1:
                s += '_or'
    return s


def flatstr(filter_list):
    cnf = group(filter_list)
    s = ''
    for i, and_group in enumerate(cnf):
        if i > 0:
            s+='_and'
        for j, or_filt in enumerate(and_group):
            s += '_' + or_filt['name']
            if j < len(and_group) - 1:
                s += '_or'
    return s

import os

from .print import (flatstr, pretty_print)
from .functions import (group, apply)

def filelines(full_filename:str):
    with open(full_filename, 'r') as file:
        return sum(1 for line in file)
    return None

def ofilename(ifilename:str, filters:list):
    odir = os.path.dirname(ifilename)
    bn, xt = os.path.splitext(os.path.basename(ifilename))
    file = '{}_{}.{}'.format(bn, flatstr(filters), xt)
    return os.path.join(odir, file)


filter_msg1 = lambda: '''Applying user specified filters named:
    {}
to lines defined in:
    {}
'''.format(pretty_print(filters), input_file)
filter_msg2 = lambda: '''Filtering complete.
{} lines pass filters.
{}% of starting lines.
Results stored in:
    {}
'''.format(
    lines_in_output,
    round(lines_in_output/lines_in_input*100,2),
    output_file
)

from sil import Sil
def filter_file(
    input_file:str,
    filters:list,
    output_file:str = None,
    header:bool     = False,
    delim:str       = '\t',
    newline:str     = '\n',
    sil_opts:dict   = {'every': 1000, 'length': 40},
    verbose         = True
):
    lines_in_input = filelines(input_file)
    if lines_in_input is None: return

    sil = Sil(lines_in_input, **sil_opts)
    grp = group(filters)

    if output_file is None: output_file = ofilename(input_file, filters)
    if not os.path.isdir(os.path.dirname(output_file)): os.makedirs(output_file)

    if verbose: print(filter_msg1())

    with \
    open(input_file, 'r') as input_file_object, \
    open(output_file, 'w') as output_file_object:

        if header:
            output_file_object.write(input_file_object.readline())
            if verbose: sil.tick()

        for line in input_file_object:
            fields = line.rstrip(newline).split(delim)
            if apply(grp, fields): output_file_object.write(line)
            if verbose: sil.tick()

    if verbose:
        lines_in_output = filelines(output_file)
        if header: lines_in_output -= 1
        print(filter_msg2())

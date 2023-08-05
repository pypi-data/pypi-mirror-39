def group(filter_list:list)->list:
    grouped = []

    for i, filt in enumerate(filter_list):
        # error handling if logic not specified
        logic = 'and'

        # if specified, use it
        if 'logic' in filt: logic = filt['logic']

        # regardless if specified, if first in list, must be and
        if i == 0: logic = 'and'

        # start new group
        if logic == 'and': grouped.append([filt])

        # append to last sublist
        else: grouped[-1].append(filt)

    return grouped


def apply(grouped_filters:list, *lambda_args):
    return all([any([filt['lambda'](*lambda_args) for filt in or_filters]) for or_filters in grouped_filters])
    '''
    Don't let this one-liner scare you.
    CNF is a list of logical operations:

        (a or b or c or ...) and (x or y or ...) and ...

    The function "group" will give us a list of lists, where each sublist are
    all the "or" statements. Thus to evaluate those, we just need to call any on
    that sublist:

        any([a, b, c])

    To test the ands, we just need to call all on the list of ORs:

        all([ any([<OR-statments>]) for <OR-statments> in grouped ])

    Recall that each of our "filters" are represented by a dictionary with three
    keys:

        {
            'logic':    a string which is either 'and' or 'or'
            'lambda':   a lambda function to be applied to something
            'name':     a name which can help with keeping things clear
        }

    Thus, for each filter, we call the lambda function with the unnamed arguments


    all([
        any([
            filt['lambda'](*lambda_args) for filt in grouped_or
        ])
        for grouped_or in grouped_filters
    ])
    '''

from operator import itemgetter

def dict_sort(list_dict, sort_keys=None):
    """Get sorted list of dictonaries

    Keyword arguments:
    list_dict -- list of dictionary to be sorted eg:- [{'name':'alex', 'age':10}, {'name':'mike', 'age':20}]
    sort_keys -- list of key on to which sorting needs to be done. eg:- ['age']

    @author : Anshul Gupta (anshulgupta217@gmail.com)
    """

    if sort_keys is not None:
        return sorted(list_dict, key=itemgetter(*sort_keys))
    else:
        print("Please provide sort_keys list to sort given dictionary")
        return None


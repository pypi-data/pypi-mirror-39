"""This is the "nester.py" module, and it offers one function named print_lol()
which prints lists that either have or do not have nested lists. Additional arguments
are provided to offer what the the first version (3.6.5) could do, and more."""
def print_lol(the_list, indent=False, level=0):
    """This function takes a positional argument called "the_list", which is any
    Python list (of, possibly, nested lists). Each data item in from the list is
    (recursively) printed to the screen on its own line.
    A second argument called 'indent' enables the indent feature to display list-items
    and their indentations as they were written into the list.
    A third argument called 'level' is used to insert tab-stops when a nested
    list is encountered."""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level+1)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t", end='')
            print(each_item)

"""This is the "nester.py" module and it provides one function called print_lol() which prints lists that may or may not include nested lists."""

def print_lol(the_list, indent=False, level=0):
    """This function takes one positional argument called "the_list", which is any python list (of - possibly - nested lists). Each data item in the provided list is (recursively) printed to the screen on it's own line.
 The second argument, "indent" determines whether the indentation feature is to be included or not in displaying the data items. It is set to a default value of False, so that no indentation occurs in the display of the data items of the list, except the user requires indentation (by altering it's value to true). A third argument called "level" is used to insert tab-stops when a nested list is encountered"""
    
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level+1)
        else:
            if indent:
                for tab_stop in range(level): 
                    print("\t", end='')
            print(each_item)


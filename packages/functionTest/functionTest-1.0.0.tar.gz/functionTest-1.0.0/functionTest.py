""" This is function.py and it provides one funciton called print_deep_level to print the list"""
def print_deep_level(data):
    """ print the list data"""
    if isinstance(data,list):
        for entity in data:
            print_deep_level(entity)
    else:
        print(data)
""" This is function.py and it provides one funciton called print_deep_level to print the list,位置参数控制Tab键"""

def print_deep_level(data,level):
    """ print the list data"""
    if isinstance(data,list):
        for entity in data:
            print_deep_level(entity,level+1)
    else:
        for num in range(level):
            print("\t",end='')
        print(data)
""" This is function.py and it provides one funciton called print_deep_level to print the list,位置参数控制Tab键"""

def print_deep_level(data,level=0):
    """ print the list data"""
    for entity in data:
        if isinstance(entity,list):
            print_deep_level(entity,level+1)
        else:
            for num in range(level):
                print("\t",end='')
            print(entity)
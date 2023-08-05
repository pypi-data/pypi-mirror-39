""" This is function.py and it provides one funciton called print_deep_level to print the list
    \*data*\ is the data source
     \*need*\ control whether  print Tab 
     \*level*\ the number of printing Tab
"""

def print_deep_level(data,need=False,level=0):
    """ print the list data"""
    for entity in data:
        if isinstance(entity,list):
            print_deep_level(entity,level+1)
        else:
            if(need):
                for num in range(level):
                    print("\t",end='')
            print(entity)
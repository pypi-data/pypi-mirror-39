#!/usr/bin/python
def asd123(the_list):
    for each_item in the_list:
        if isinstance(each_item, list):
            asd123(each_item)
        else:
            print(each_item)

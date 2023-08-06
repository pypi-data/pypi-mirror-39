'''
       这是“marho”模块，提供一个print_lol()的函数，这个函数的作用是打印列表的列表，
其中有可能包含（也可能不包含）嵌套列表
'''
def print_lol(the_list,num1=0):
    '''这个函数取一个位置参数，名为‘the_list’,这可以是任何Pyhon列表（也可以包含嵌套的列表的列表）。
所指定的列表中的每个数据项会递归输出到屏幕上，各数据项各占一行。
第二个参数(level)，用来遇到嵌套列表时插入制表符'''
    for each_item in the_list:
         if isinstance(each_item,list):
             print_lol(each_item,num1+1)
         else:
             for tab_stop in range(num1):
                 print('\t',end=' ')
             print(each_item)

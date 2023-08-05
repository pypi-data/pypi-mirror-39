"""这是"lits_01"模块，提供了一个名为print_list的函数。这个函数的作用是打印列表，包含嵌套列表。"""
def print_list(the_list,level=0):
        """ 这个函数取一个位置参数，命为"the_list".这个参数可以是任何python列表。
所指定的列表中的每个数据项都会递归的输入到屏幕上，各数据项各占一行。
第二个参数（level）用来在发现嵌套列表时插入制表符(第二参数不输入默认为0)。"""
        for a in the_list:
                if isinstance(a,list):
                        print_list(a,level+1)
                else:
                        for tab_stop in range(level):
                                print("\t",end='')
                        print(a)

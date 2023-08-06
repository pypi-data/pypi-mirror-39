"""这个函数去一个位置参数，为the_list,可以是任何列表，指定的列表中的每个数据项会递归地
输出到屏幕上，个数据项占一行"""
def print1991(the_list,level):
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item,level+1)
		else:
                        for num in level:
                                print('\t',end='')
			print(each_item)

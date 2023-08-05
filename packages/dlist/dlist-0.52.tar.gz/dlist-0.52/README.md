# dlist

A list of dict.<br>
Each dict-element has only one key.<br>
Such as: `[ {k1:v1},{k2:v2},{k3,v3}]`

## Documents
>https://ihgazni2.github.io/dlist/

## Functions
###   &nbsp;&nbsp;&nbsp;&nbsp;`is_dlist(obj)`<br>
			from dlist import *
			rslts[0] = (is_dlist([]) == True)
			rslts[1] = (is_dlist([{1:'a'},{2:'b'}]) == True)
			rslts[2] = (is_dlist([{1:'a',2:'b'},{3:'c',4:'d'}]) == False)
###   &nbsp;&nbsp;&nbsp;&nbsp;`dict2dlist(this_dict,**kwargs)`<br>
			from dlist import *
			d = {1:2,3:4,5:6,7:8}
			rslts[3] = (dict2dlist(d) == [{1: 2}, {3: 4}, {5: 6}, {7: 8}])
###   &nbsp;&nbsp;&nbsp;&nbsp;`dlist2dict(dict_list,**kwargs)`<br>
                	from dlist import *
                	d = {1:2,3:4,5:6,7:8}
                	dl = [{1: 2}, {3: 4}, {5: 6}, {7: 8}]
                	rslts[4] = (dlist2dict(dl) == d)
###   &nbsp;&nbsp;&nbsp;&nbsp;`kvlist2dlist(klist,vlist,**kwargs)`<br>
###   &nbsp;&nbsp;&nbsp;&nbsp;`dlist2kvlist(dict_list,**kwargs)`<br>
                        from dlist import *
                        d = {1:2,3:4,5:6,7:8}
                        dl = [{1: 2}, {3: 4}, {5: 6}, {7: 8}]
                        kl = [1,3,5,7]
                        vl = [2,4,6,8]
                        rslts[5] = (dlist2kvlist(dl) == (kl,vl))
                        rslts[6] = (kvlist2dlist(kl,vl) == dl)
###   &nbsp;&nbsp;&nbsp;&nbsp;`extend(dict_list_1,dict_list_2,**kwargs)`<br>
                        from dlist import *
                        dl1 = [{1:2},{3:4}]
                        dl2 = [{5:6},{7:8}]
                        extend(dl1,dl2)
                        rslts[7] = (dl1 == [{1: 2}, {3: 4}, {5: 6}, {7: 8}])
###   &nbsp;&nbsp;&nbsp;&nbsp;`prextend(dict_list_1,dict_list_2,**kwargs)`<br>
                        dl1 = [{1:2},{3:4}]
                        dl2 = [{5:6},{7:8}]
                        prextend(dl1,dl2)
                        rslts[8] = (dl1 == [{5: 6}, {7: 8},{1: 2}, {3: 4}])
###   &nbsp;&nbsp;&nbsp;&nbsp;`concat(dict_list_1,dict_list_2,**kwargs)`<br>
                        dl1 = [{1:2},{3:4}]
                        dl2 = [{5:6},{7:8}]
                        dl = concat(dl1,dl2)
                        rslts[9] = (dl == [{1: 2}, {3: 4}, {5: 6}, {7: 8}])
###   &nbsp;&nbsp;&nbsp;&nbsp;`first_islice(dict_list,**kwargs)`<br>
                        from dlist import *
                        dl = [{1:2},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'}]
                        rslts[10] = (first_islice(dl,key='a') == [1, 2])
                        rslts[11] = (first_islice(dl,mode='value',value='b') == [3, 4])
                        rslts[12] = (first_islice(dl,mode='kv',key='c',value='c') == [5, 6])
###   &nbsp;&nbsp;&nbsp;&nbsp;`last_islice(dict_list,**kwargs)`<br>
                        from dlist import *
                        dl = [{1:2},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'}]
                        rslts[13] = (last_islice(dl,key='a') == [7, 8])
                        rslts[14] = (last_islice(dl,mode='value',value='b') == [9, 10])
                        rslts[15] = (last_islice(dl,mode='kv',key='c',value='c') == [11, 12])
###   &nbsp;&nbsp;&nbsp;&nbsp;`all_islice(dict_list,**kwargs)`<br>
                        from dlist import *
                        dl = [{1:2},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'}]
                        rslts[16] = (all_islice(dl,key='a') == [[1, 2], [7, 8]])
                        rslts[17] = (all_islice(dl,mode='value',value='b') == [[3, 4], [9, 10]])
                        rslts[18] = (all_islice(dl,mode='kv',key='c',value='c') == [[5, 6], [11, 12]])
###   &nbsp;&nbsp;&nbsp;&nbsp;`indexes(dict_list,value,**kwargs)`<br>
                        from dlist import *
                        dl = [{1:2},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'}]
                        rslts[19] = (indexes(dl,key='a') == [1, 2, 7, 8]])
                        rslts[20] = (indexes(dl,mode='value',value='b') == [3, 4, 9, 10])
                        rslts[21] = (indexes(dl,mode='kv',key='a',value='y') == [2,8])
###   &nbsp;&nbsp;&nbsp;&nbsp;`first_index(dict_list,**kwargs)`<br>
                        from dlist import *
                        dl = [{1:2},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'}]
                        rslts[22] = (first_index(dl,key='a') == 1)
                        rslts[23] = (first_index(dl,mode='value',value='b') == 3)
                        rslts[24] = (first_index(dl,mode='kv',key='a',value='y') == 2)
###   &nbsp;&nbsp;&nbsp;&nbsp;`last_index(dict_list,**kwargs)`<br>
                        from dlist import *
                        dl = [{1:2},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'}]
                        rslts[25] = (last_index(dl,key='a') == 8)
                        rslts[26] = (last_index(dl,mode='value',value='b') == 10)
                        rslts[27] = (last_index(dl,mode='kv',key='a',value='y') == 8)
###   &nbsp;&nbsp;&nbsp;&nbsp;`append(dict_list,key,value,**kwargs)`<br>
###   &nbsp;&nbsp;&nbsp;&nbsp;`prepend(dict_list,key,value,**kwargs)`<br>
                        from dlist import *
                        dl = [{1:'a'},{2:'b'},{3:'c'}]
                        rslts[28] = (append(dl,'k','v') == [{1: 'a'}, {2: 'b'}, {3: 'c'}, {'k': 'v'}])
                        dl = [{1:'a'},{2:'b'},{3:'c'}]
                        rslts[29] = (prepend(dl,'k','v') == [{'k': 'v'}, {1: 'a'}, {2: 'b'}, {3: 'c'}])
###   &nbsp;&nbsp;&nbsp;&nbsp;`clear(dict_list,**kwargs)`<br>
###   &nbsp;&nbsp;&nbsp;&nbsp;`insert(dict_list,index,key,value,**kwargs)`<br>
###   &nbsp;&nbsp;&nbsp;&nbsp;`insert_dlist(dict_list_1,index,dict_list_2,**kwargs)`<br>
                        from dlist import *
                        dl = [{1:'a'},{2:'b'},{3:'c'}]
                        rslts[30] = (insert(dl,1,'k','v') == [{1: 'a'}, {'k': 'v'},{2: 'b'}, {3: 'c'}])
                        dl = [{1:'a'},{2:'b'},{3:'c'}]
                        dl2 = [{'k1':'v1'},{'k2':'v2'}]
                        rslts[31] = (insert_dlist(dl,1,dl2) == [{1: 'a'}, {'k1':'v1'},{'k2':'v2'},{'k': 'v'},{2: 'b'}, {3: 'c'}])
###   &nbsp;&nbsp;&nbsp;&nbsp;`include(dict_list,**kwargs)`<br>
                        from dlist import *
                        dl = [{1:2},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'}]
                        rslts[32] = (include(dl,key='b') == False)
                        rslts[33] = (include(dl,mode='value',value='b') == True)
                        rslts[34] = (include(dl,mode='kv',key='a',value='y') == True)
###   &nbsp;&nbsp;&nbsp;&nbsp;`count(dict_list,**kwargs)`<br>
                        from dlist import *
                        dl = [{1:2},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'}]
                        rslts[35] = (count(dl,key='a') == 4)
                        rslts[36] = (count(dl,mode='value',value='b') == 4)
                        rslts[37] = (count(dl,mode='kv',key='a',value='y') == 2)
###   &nbsp;&nbsp;&nbsp;&nbsp;`pop(dict_list,**kwargs)`<br>
###   &nbsp;&nbsp;&nbsp;&nbsp;`pop_range(dict_list,start,end,**kwargs)`<br>
###   &nbsp;&nbsp;&nbsp;&nbsp;`pop_seqs(dict_list,seqs_set,**kwargs)`<br>
                        from dlist import *
                        dl = [{1:2},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'}]
                        pop(dl,index=1)
                        dl = [{1:2},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'}]
                        rslts[38] = (pop(dl,mode='key',key='a') == [{'a': 'x'}, {'a': 'y'}, {'a': 'x'}, {'a': 'y'}])
                        rslts[39] = (dl == [{1: 2}, {3: 'b'}, {5: 'b'}, {'c': 'c'}, {'c': 'c'}, {3: 'b'}, {5: 'b'}, {'c': 'c'}, {'c': 'c'}] )
                        dl = [{1:2},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'}]
                        rslts[40] = (pop_range(dl,1,4) == [{'a': 'x'}, {'a': 'y'}, {3: 'b'}])
                        rslts[41] = (dl == [{1: 2}, {5: 'b'}, {'c': 'c'}, {'c': 'c'}, {'a': 'x'}, {'a': 'y'}, {3: 'b'}, {5: 'b'}, {'c': 'c'}, {'c': 'c'}])
                        dl = [{1:2},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'}]
                        rslts[42] = (pop_seqs(dl,[0,2,4]) == [{1: 2}, {'a': 'y'}, {5: 'b'}])
                        rslts[43] = (dl = [{'a': 'x'}, {3: 'b'}, {'c': 'c'}, {'c': 'c'}, {'a': 'x'}, {'a': 'y'}, {3: 'b'}, {5: 'b'}, {'c': 'c'}, {'c': 'c'}])
###   &nbsp;&nbsp;&nbsp;&nbsp;`rm_first(dict_list,**kwargs)`<br>
                        from dlist import *
                        dl = [{1:2},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'}]
                        rslts[44] = (rm_first(dl,key='a') == [{1: 2}, {'a': 'y'}, {3: 'b'}, {5: 'b'}, {'c': 'c'}, {'c': 'c'}, {'a': 'x'}, {'a': 'y'}, {3: 'b'}, {5: 'b'}, {'c': 'c'}, {'c': 'c'}])
                        dl = [{1:2},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'}]
                        rslts[45] = (rm_first(dl,mode='value',value='b') == [{1: 2}, {'a': 'x'}, {'a': 'y'}, {5: 'b'}, {'c': 'c'}, {'c': 'c'}, {'a': 'x'}, {'a': 'y'}, {3: 'b'}, {5: 'b'}, {'c': 'c'}, {'c': 'c'}])
                        dl = [{1:2},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'}]
                        rslts[46] = (rm_first(dl,mode='kv',key='a',value='y') == [{1: 2}, {'a': 'x'}, {3: 'b'}, {5: 'b'}, {'c': 'c'}, {'c': 'c'}, {'a': 'x'}, {'a': 'y'}, {3: 'b'}, {5: 'b'}, {'c': 'c'}, {'c': 'c'}])
###   &nbsp;&nbsp;&nbsp;&nbsp;`rm_last(dict_list,**kwargs)`<br>
                        from dlist import *
                        dl = [{1:2},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'}]
                        rslts[47] = (rm_last(dl,key='a') == [{1: 2}, {'a': 'x'}, {'a': 'y'}, {3: 'b'}, {5: 'b'}, {'c': 'c'}, {'c': 'c'}, {'a': 'x'}, {3: 'b'}, {5: 'b'}, {'c': 'c'}, {'c': 'c'}])
                        dl = [{1:2},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'}]
                        rslts[48] = (rm_last(dl,mode='value',value='b') == [{1: 2}, {'a': 'x'}, {'a': 'y'}, {3: 'b'}, {5: 'b'}, {'c': 'c'}, {'c': 'c'}, {'a': 'x'}, {'a': 'y'}, {3: 'b'}, {'c': 'c'}, {'c': 'c'}])
                        dl = [{1:2},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'}]
                        rslts[49] = (rm_last(dl,mode='kv',key='a',value='y') == [{1: 2}, {'a': 'x'}, {'a': 'y'}, {3: 'b'}, {5: 'b'}, {'c': 'c'}, {'c': 'c'}, {'a': 'x'}, {3: 'b'}, {5: 'b'}, {'c': 'c'}, {'c': 'c'}])
###   &nbsp;&nbsp;&nbsp;&nbsp;`rm_all(dict_list,**kwargs)`<br>
                        from dlist import *
                        dl = [{1:2},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'}]
                        rslts[47] = (rm_all(dl,key='a') == [{1: 2}, {3: 'b'}, {5: 'b'}, {'c': 'c'}, {'c': 'c'}, {3: 'b'}, {5: 'b'}, {'c': 'c'}, {'c': 'c'}])
                        dl = [{1:2},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'}]
                        rslts[48] = (rm_all(dl,mode='value',value='b') == [{1: 2}, {'a': 'x'}, {'a': 'y'}, {'c': 'c'}, {'c': 'c'}, {'a': 'x'}, {'a': 'y'}, {'c': 'c'}, {'c': 'c'}])
                        dl = [{1:2},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'}]
                        rslts[49] = (rm_all(dl,mode='kv',key='a',value='y') == [{1: 2}, {'a': 'x'}, {3: 'b'}, {5: 'b'}, {'c': 'c'}, {'c': 'c'}, {'a': 'x'}, {3: 'b'}, {5: 'b'}, {'c': 'c'}, {'c': 'c'}])
###   &nbsp;&nbsp;&nbsp;&nbsp;`reverse(dict_list,**kwargs)`<br>
                        from dlist import *
                        dl = [{1:2},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'}]
                        rslts[53] =(reverse(dl)  == [{'c': 'c'}, {'c': 'c'}, {5: 'b'}, {3: 'b'}, {'a': 'y'}, {'a': 'x'}, {'c': 'c'}, {'c': 'c'}, {5: 'b'}, {3: 'b'}, {'a': 'y'}, {'a': 'x'}, {1: 2}])
###   &nbsp;&nbsp;&nbsp;&nbsp;`sort(dict_list,**kwargs)`<br>
                        from dlist import *
                        dl = [{1:2},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'}]
                        rslts[54] = (sort(dl)  == [{1: 2}, {3: 'b'}, {3: 'b'}, {5: 'b'}, {5: 'b'}, {'a': 'x'}, {'a': 'x'}, {'a': 'y'}, {'a': 'y'}, {'c': 'c'}, {'c': 'c'}, {'c': 'c'}, {'c': 'c'}])
                        dl = [{1:2},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'}]
                        rslts[55] = (sort(dl,mode='vk') == [{1: 2}, {3: 'b'}, {3: 'b'}, {5: 'b'}, {5: 'b'}, {'c': 'c'}, {'c': 'c'}, {'c': 'c'}, {'c': 'c'}, {'a': 'x'}, {'a': 'x'}, {'a': 'y'}, {'a': 'y'}])
                        dl = [{1:2},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'}]
                        rslts[56] = (sort(dl,mode='key')  == [{1: 2}, {3: 'b'}, {3: 'b'}, {5: 'b'}, {5: 'b'}, {'a': 'x'}, {'a': 'y'}, {'a': 'x'}, {'a': 'y'}, {'c': 'c'}, {'c': 'c'}, {'c': 'c'}, {'c': 'c'}])
                        dl = [{1:2},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'},{'a':'x'},{'a':'y'},{3:'b'},{5:'b'},{'c':'c'},{'c':'c'}]
                        rslts[57] = (sort(dl,mode='value') == [{1: 2}, {3: 'b'}, {5: 'b'}, {3: 'b'}, {5: 'b'}, {'c': 'c'}, {'c': 'c'}, {'c': 'c'}, {'c': 'c'}, {'a': 'x'}, {'a': 'x'}, {'a': 'y'}, {'a': 'y'}])
###   &nbsp;&nbsp;&nbsp;&nbsp;`comprise(dict_list1,dict_list2,**kwargs)`<br>
                        from dlist import *
                        dl1 = [{1:2},{3:4},{5:6},{7:8}]
                        dl2 = [{3:4},{5:6}]
                        rslts[58] = (comprise(dl1,dl2) == True)
                        rslts[59] = (comprise(dl1,dl2,strict=True) == False)
###   &nbsp;&nbsp;&nbsp;&nbsp;`tuple2dict(t)`<br>
###   &nbsp;&nbsp;&nbsp;&nbsp;`dict2tuple(d)`<br>
                        from dlist import *
                        d = {1:2}
                        rslts[62] = (dict2tuple(d) == (1, 2))
                        t = (1, 2)
                        rslts[63] = (tuple2dict(t) == {1:2})
###   &nbsp;&nbsp;&nbsp;&nbsp;`dlist2tlist(dl)`<br>
###   &nbsp;&nbsp;&nbsp;&nbsp;`tlist2dlist(tl)`<br>
                        from dlist import *
                        dl = [{1:2},{3:4},{5:6},{7:8}]
                        rslts[60] = (dlist2tlist(dl) == [(1, 2), (3, 4), (5, 6), (7, 8)])
                        tl = [(1, 2), (3, 4), (5, 6), (7, 8)]
                        rslts[61] = (tlist2dlist(tl) == [{1:2},{3:4},{5:6},{7:8}])
###   &nbsp;&nbsp;&nbsp;&nbsp;`cmp_dele(d1,d2,**kwargs)`<br>
                        from dlist import *
                        d1 = {1:2}
                        d2 = {2:1}
                        rslts[64] = (cmp_dele(d1,d2,mode='key') == -1)
                        rslts[65] = (cmp_dele(d1,d2,mode='value') == 1)
                        d3 = {3:4}
                        d4 = {3:5}
                        rslts[66] = (cmp_dele(d3,d4,mode='kv') == -1)
                        d5 = {7:6}
                        d6 = {8:6}
                        rslts[67] = (cmp_dele(d5,d6,mode='vk') == 1)
                        rslts[68] = (cmp_dele(d5,d5) == 0)



import copy
from operator import itemgetter
import functools

def is_dlist(obj):
    if(isinstance(obj,list)):
        pass
    else:
        return(False)
    if(obj == []):
        return(True)
    else:
        for each in obj:
            if(isinstance(each,dict)):
                if(each.__len__()==1):
                    pass
                else:
                    return(False)
            else:
                return(False)
    return(True)

def dict2dlist(this_dict,**kwargs):
    '''
        >>> dict2dlist({1:2,3:4})
        [{1: 2}, {3: 4}]
        >>>
    ''' 
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(isinstance(this_dict,dict)):
            pass
        else:
            return(None)
    else:
        pass
    if('deepcopy' in kwargs):
        deepcopy = kwargs['deepcopy']
    else:
        deepcopy = 1
    dict_list = []
    if(deepcopy):
        new = copy.deepcopy(this_dict)
    else:
        new = this_dict
    for key in this_dict:
        value = this_dict[key]
        dict_list.append({key:value})
    return(dict_list)

def dlist2dict(dict_list,**kwargs):
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_dlist(dict_list)):
            pass
        else:
            return(None)
    else:
        pass
    if('deepcopy' in kwargs):
        deepcopy = kwargs['deepcopy']
    else:
        deepcopy = 1
    d = {}
    length = dict_list.__len__()
    if(deepcopy):
        new = copy.deepcopy(dict_list)
    else:
        new = dict_list
    for i in range(0,length):
        temp = new[i]
        key = list(temp.keys())[0]
        value = list(temp.values())[0]
        d[key] = value
    return(d)

def kvlist2dlist(klist,vlist,**kwargs):
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(isinstance(klist,list)):
            pass
        else:
            return(None)
        if(isinstance(vlist,list)):
            pass
        else:
            return(None)
        if(klist.__len__()==vlist.__len__()):
            pass
        else:
            return(None)
    else:
        pass
    if('deepcopy' in kwargs):
        deepcopy = kwargs['deepcopy']
    else:
        deepcopy = 1
    dict_list = []
    len = klist.__len__()
    if(deepcopy):
        newk = copy.deepcopy(klist)
        newv = copy.deepcopy(vlist)
    else:
        newk = klist
        newv = vlist
    for i in range(0,len):
        key = newk[i]
        value = newv[i]
        dict_list.append({key:value})
    return(dict_list)

def dlist2kvlist(dict_list,**kwargs):
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_dlist(dict_list)):
            pass
        else:
            return(None)
    else:
        pass
    if('deepcopy' in kwargs):
        deepcopy = kwargs['deepcopy']
    else:
        deepcopy = 1
    kl = []
    vl = []
    len = dict_list.__len__()
    if(deepcopy):
        new = copy.deepcopy(dict_list)
    else:
        new = dict_list
    for i in range(0,len):
        temp = new[i]
        key = list(temp.keys())[0]
        value = list(temp.values())[0]
        kl.append(key)
        vl.append(value)
    return((kl,vl))

#180
def extend(dict_list_1,dict_list_2,**kwargs):
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_dlist(dict_list_1) & is_dlist(dict_list_2)):
            pass
        else:
            return(None)
    else:
        pass
    if('deepcopy_1' in kwargs):
        deepcopy_1 = kwargs['deepcopy_1']
    else:
        deepcopy_1 = 0
    if('deepcopy_2' in kwargs):
        deepcopy_2 = kwargs['deepcopy_2']
    else:
        deepcopy_2 = 0
    if(deepcopy_1):
        new_1 = copy.deepcopy(dict_list_1)
    else:
        new_1 = dict_list_1
    if(deepcopy_2):
        new_2 = copy.deepcopy(dict_list_2)
    else:
        new_2 = copy.copy(dict_list_2)
    len_1 = new_1.__len__()
    len_2 = new_2.__len__()
    for i in range(0,len_2):
        new_1.append(new_2[i])
    return(new_1)

def prextend(dict_list_1,dict_list_2,**kwargs):
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_dlist(dict_list_1) & is_dlist(dict_list_2)):
            pass
        else:
            return(None)
    else:
        pass
    if('deepcopy_1' in kwargs):
        deepcopy_1 = kwargs['deepcopy_1']
    else:
        deepcopy_1 = 0
    if('deepcopy_2' in kwargs):
        deepcopy_2 = kwargs['deepcopy_2']
    else:
        deepcopy_2 = 0
    if(deepcopy_1):
        new_1 = copy.deepcopy(dict_list_1)
    else:
        new_1 = dict_list_1
    if(deepcopy_2):
        new_2 = copy.deepcopy(dict_list_2)
    else:
        new_2 = copy.copy(dict_list_2)
    len_1 = new_1.__len__()
    len_2 = new_2.__len__()
    for i in range(0,len_2):
        new_1.append(new_2[i])
    return(new_1)

def concat(dict_list_1,dict_list_2,**kwargs):
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_dlist(dict_list_1) & is_dlist(dict_list_2)):
            pass
        else:
            return(None)
    else:
        pass
    if('deepcopy_1' in kwargs):
        deepcopy_1 = kwargs['deepcopy_1']
    else:
        deepcopy_1 = 1
    if('deepcopy_2' in kwargs):
        deepcopy_2 = kwargs['deepcopy_2']
    else:
        deepcopy_2 = 1
    if(deepcopy_1):
        new_1 = copy.deepcopy(dict_list_1)
    else:
        new_1 = dict_list_1
    if(deepcopy_2):
        new_2 = copy.deepcopy(dict_list_2)
    else:
        new_2 = dict_list_2
    len_1 = new_1.__len__()
    len_2 = new_2.__len__()
    new = []
    for i in range(0,len_1):
        new.append(new_1[i])
    for i in range(0,len_2):
        new.append(new_2[i])
    return(new)
#287
def first_islice(dict_list,**kwargs):
    if('mode' in kwargs):
        mode = kwargs['mode']
    else:
        mode = 'key'
    if('key' in kwargs):
        key = kwargs['key']
    if('value' in kwargs):
        value = kwargs['value']
    if('start' in kwargs):
        start = kwargs['start']
    else:
        start = 0
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_dlist(dict_list)):
            pass
        else:
            return(None)
    else:
        pass
    rslt = []
    begin = 0
    for i in range(start,dict_list.__len__()):
        temp = dict_list[i]
        k = list(temp.keys())[0]
        v = list(temp.values())[0]
        if(mode == 'key'):
            if(k == key):
                rslt.append(i)
                begin = i+1
                break
            else:
                pass
        elif(mode == 'value'):
            if(v == value):
                rslt.append(i)
                begin = i+1
                break
            else:
                pass
        else:
            if((v == value)&(k == key)):
                rslt.append(i)
                begin = i+1
                break
            else:
                pass
    for i in range(begin,dict_list.__len__()):
        temp = dict_list[i]
        k = list(temp.keys())[0]
        v = list(temp.values())[0]
        if(mode == 'key'):
            if(k == key):
                rslt.append(i)
            else:
                break
        elif(mode == 'value'):
            if(v == value):
                rslt.append(i)
            else:
                break
        else:
            if((v == value)&(k == key)):
                rslt.append(i)
            else:
                break
    return(rslt)
#359
def last_islice(dict_list,**kwargs):
    if('mode' in kwargs):
        mode = kwargs['mode']
    else:
        mode = 'key'
    if('key' in kwargs):
        key = kwargs['key']
    if('value' in kwargs):
        value = kwargs['value']
    if('start' in kwargs):
        start = kwargs['start']
    else:
        start = -1
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_dlist(dict_list)):
            pass
        else:
            return(None)
    else:
        pass
    if(start==-1):
        start = dict_list.__len__()-1
    rslt = []
    begin = 0
    for i in range(start,-1,-1):
        temp = dict_list[i]
        k = list(temp.keys())[0]
        v = list(temp.values())[0]
        if(mode == 'key'):
            if(k == key):
                rslt.append(i)
                begin = i-1
                break
            else:
                pass
        elif(mode == 'value'):
            if(v == value):
                rslt.append(i)
                begin = i-1
                break
            else:
                pass
        else:
            if((v == value)&(k == key)):
                rslt.append(i)
                begin = i-1
                break
            else:
                pass
    for i in range(begin,-1,-1):
        temp = dict_list[i]
        k = list(temp.keys())[0]
        v = list(temp.values())[0]
        if(mode == 'key'):
            if(k == key):
                rslt.append(i)
            else:
                break
        elif(mode == 'value'):
            if(v == value):
                rslt.append(i)
            else:
                break
        else:
            if((v == value)&(k == key)):
                rslt.append(i)
            else:
                break
    rslt.reverse()
    return(rslt)
#434
def all_islice(dict_list,**kwargs):    
    if('mode' in kwargs):
        mode = kwargs['mode']
    else:
        mode = 'key'
    if('key' in kwargs):
        key = kwargs['key']
    if('value' in kwargs):
        value = kwargs['value']
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_dlist(dict_list)):
            pass
        else:
            return(None)
    else:
        pass
    len = dict_list.__len__()
    sarray = []
    start = 0
    while(start < len):
        if(mode == 'key'):
            rslt = first_islice(dict_list,key=key,start=start,check=0,mode='key')
        elif(mode == 'value'):
            rslt = first_islice(dict_list,value=value,start=start,check=0,mode='value')
        else:
            rslt = first_islice(dict_list,key=key,value=value,start=start,check=0,mode='key_value')
        if(rslt.__len__()==0):
            break
        else:
            sarray.append(rslt)
            start = rslt[-1] +1
    return(sarray)

def indexes(dict_list,**kwargs):
    if('mode' in kwargs):
        mode = kwargs['mode']
    else:
        mode = 'key'
    if('key' in kwargs):
        key = kwargs['key']
    if('value' in kwargs):
        value = kwargs['value']
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_dlist(dict_list)):
            pass
        else:
            return(None)
    else:
        pass
    rslt = []
    for i in range(0,dict_list.__len__()):
        temp = dict_list[i]
        k = list(temp.keys())[0]
        v = list(temp.values())[0]
        if(mode == 'key'):
            if(k == key):
                rslt.append(i)
            else:
                pass
        elif(mode == 'value'):
            if(v == value):
                rslt.append(i)
            else:
                pass
        else:
            if((v == value)&(k == key)):
                rslt.append(i)
            else:
                pass
    return(rslt)

def first_index(dict_list,**kwargs):
    if('mode' in kwargs):
        mode = kwargs['mode']
    else:
        mode = 'key'
    if('key' in kwargs):
        key = kwargs['key']
    if('value' in kwargs):
        value = kwargs['value']
    if('start' in kwargs):
        start = kwargs['start']
    else:
        start = 0
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_dlist(dict_list)):
            pass
        else:
            return(None)
    else:
        pass
    for i in range(start,dict_list.__len__()):
        temp = dict_list[i]
        k = list(temp.keys())[0]
        v = list(temp.values())[0]
        k = list(temp.keys())[0]
        v = list(temp.values())[0]
        if(mode == 'key'):
            if(k == key):
                return(i)
            else:
                pass
        elif(mode == 'value'):
            if(v == value):
                return(i)
            else:
                pass
        else:
            if((v == value)&(k == key)):
                return(i)
            else:
                pass
    return(None)

def last_index(dict_list,**kwargs):
    if('mode' in kwargs):
        mode = kwargs['mode']
    else:
        mode = 'key'
    if('key' in kwargs):
        key = kwargs['key']
    if('value' in kwargs):
        value = kwargs['value']
    if('start' in kwargs):
        start = kwargs['start']
    else:
        start = -1
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_dlist(dict_list)):
            pass
        else:
            return(None)
    else:
        pass
    if(start == -1):
        start = dict_list.__len__() - 1
    for i in range(start,-1,-1):
        temp = dict_list[i]
        k = list(temp.keys())[0]
        v = list(temp.values())[0]
        if(mode == 'key'):
            if(k == key):
                return(i)
            else:
                pass
        elif(mode == 'value'):
            if(v == value):
                return(i)
            else:
                pass
        else:
            if((v == value)&(k == key)):
                return(i)
            else:
                pass
    return(None)

def append(dict_list,key,value,**kwargs):
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_dlist(dict_list)):
            pass
        else:
            return(None)
    else:
        pass
    if('deepcopy' in kwargs):
        deepcopy = kwargs['deepcopy']
    else:
        deepcopy = 1
    if(deepcopy):
        new = copy.deepcopy(dict_list)
    else:
        new = dict_list
    new.append({key:value})
    return(new)

def prepend(dict_list,key,value,**kwargs):
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_dlist(dict_list)):
            pass
        else:
            return(None)
    else:
        pass
    if('deepcopy' in kwargs):
        deepcopy = kwargs['deepcopy']
    else:
        deepcopy = 1
    if(deepcopy):
        new = copy.deepcopy(dict_list)
    else:
        new = dict_list
    len = dict_list.__len__()
    swap = []
    swap.append({key:value})
    for i in range(0,len):
        swap.append(new[i])
    return(swap)

def clear(dict_list,**kwargs):
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_dlist(dict_list)):
            pass
        else:
            return(None)
    else:
        pass
    if('deepcopy' in kwargs):
        deepcopy = kwargs['deepcopy']
    else:
        deepcopy = 0
    if(deepcopy):
        new = []
    else:
        new = dict_list
        new.clear()
    return(new)

def copy(dict_list,**kwargs):
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_dlist(dict_list)):
            pass
        else:
            return(None)
    else:
        pass
    dict_list = dict_list.copy()
    return(dict_list)

def deepcopy(dict_list,**kwargs):
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_dlist(dict_list)):
            pass
        else:
            return(None)
    else:
        pass
    dict_list = copy.deepcopy(dict_list)
    return(dict_list)

def insert(dict_list,index,key,value,**kwargs):
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_dlist(dict_list)):
            pass
        else:
            return(None)
    else:
        pass
    if('deepcopy' in kwargs):
        deepcopy = kwargs['deepcopy']
    else:
        deepcopy = 1
    if(deepcopy):
        new = copy.deepcopy(dict_list)
    else:
        new = dict_list
    new.insert(index,{key:value})
    return(new)


def insert_dlist(dict_list_1,index,dict_list_2,**kwargs):
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_dlist(dict_list_1) & is_dlist(dict_list_2)):
            pass
        else:
            return(None)
    else:
        pass
    if('deepcopy_1' in kwargs):
        deepcopy_1 = kwargs['deepcopy_1']
    else:
        deepcopy_1 = 1
    if('deepcopy_2' in kwargs):
        deepcopy_2 = kwargs['deepcopy_2']
    else:
        deepcopy_2 = 1
    if(deepcopy_1):
        new_1 = copy.deepcopy(dict_list_1)
    else:
        new_1 = dict_list_1
    if(deepcopy_2):
        new_2 = copy.deepcopy(dict_list_2)
    else:
        new_2 = dict_list_2
    len_1 = new_1.__len__()
    len_2 = new_2.__len__()
    if(index >= len_1):
        return(new_1)
    else:
        pass
    swap = []
    for i in range(0,index):
        swap.append(new_1[i])
    for i in range(index,index + len_2):
        swap.append(new_2[i-index])
    for i in range(index + len_2,len_1+len_2):
        swap.append(new_1[i-len_2])
    return(swap)


def include(dict_list,**kwargs):
    if('mode' in kwargs):
        mode = kwargs['mode']
    else:
        mode = 'key'
    if('key' in kwargs):
        key = kwargs['key']
    if('value' in kwargs):
        value = kwargs['value']
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_dlist(dict_list)):
            pass
        else:
            return(None)
    else:
        pass
    if(mode =='key'):
        for i in range(0,dict_list.__len__()):
            temp = dict_list[i]
            k = list(temp.keys())[0]
            v = list(temp.values())[0]
            if(k == key):
                return(True)
    elif(mode == 'value'):
        for i in range(0,dict_list.__len__()):
            temp = dict_list[i]
            k = list(temp.keys())[0]
            v = list(temp.values())[0]
            if(v == value):
                return(True)
    else:
        for i in range(0,dict_list.__len__()):
            temp = dict_list[i]
            k,v = dict2tuple(temp)
            if((k==key)&(v==value)):
                return(True)
    return(False)


def count(dict_list,**kwargs):
    if('mode' in kwargs):
        mode = kwargs['mode']
    else:
        mode = 'key'
    if('key' in kwargs):
        key = kwargs['key']
    if('value' in kwargs):
        value = kwargs['value']
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_dlist(dict_list)):
            pass
        else:
            return(None)
    else:
        pass
    num = 0
    if(mode =='key'):
        for i in range(0,dict_list.__len__()):
            temp = dict_list[i]
            k = list(temp.keys())[0]
            v = list(temp.values())[0]
            if(k == key):
                num = num + 1
    elif(mode == 'value'):
        for i in range(0,dict_list.__len__()):
            temp = dict_list[i]
            k = list(temp.keys())[0]
            v = list(temp.values())[0]
            if(v == value):
                num = num + 1
    else:
        for i in range(0,dict_list.__len__()):
            temp = dict_list[i]
            k,v = dict2tuple(temp)
            if((k==key)&(v==value)):
                num = num + 1
    return(num)

def pop(dict_list,**kwargs):
    if('mode' in kwargs):
        mode = kwargs['mode']
    else:
        mode = 'index'
    if('key' in kwargs):
        key = kwargs['key']
    if('index' in kwargs):
        index = kwargs['index']
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_dlist(dict_list)):
            pass
        else:
            return(None)
    else:
        pass
    if('deepcopy' in kwargs):
        deepcopy = kwargs['deepcopy']
    else:
        deepcopy = 0
    if(deepcopy):
        new = copy.deepcopy(dict_list)
    else:
        new = dict_list
    len = dict_list.__len__()
    if(mode == 'index'):
        if(index in range(0,len)):
            rslt = new.pop(index)
        else:
            rslt = None
    else:
        rslt = []
        ndl = []
        for i in range(0,dict_list.__len__()):
            temp = dict_list[i]
            k = list(temp.keys())[0]
            v = list(temp.values())[0]
            if(k == key):
                rslt.append(dict_list[i])
            else:
                ndl.append(dict_list[i])
        dict_list.clear()
        for i in range(0,ndl.__len__()):
            dict_list.append(ndl[i])
    return(rslt)

def pop_range(dict_list,start,end,**kwargs):
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_dlist(dict_list)):
            pass
        else:
            return(None)
    else:
        pass
    if('deepcopy' in kwargs):
        deepcopy = kwargs['deepcopy']
    else:
        deepcopy = 0
    if(deepcopy):
        new = copy.deepcopy(dict_list)
    else:
        new = dict_list
    lngth = dict_list.__len__()
    rslt = []
    ndl = []
    for i in range(0,start):
        ndl.append(new[i])
    for i in range(start,end):
        rslt.append(new[i])
    for i in range(end,lngth):
        ndl.append(new[i])
    new.clear()
    for i in range(0,ndl.__len__()):
        new.append(ndl[i])
    return(rslt)

def pop_seqs(dict_list,seqs_set,**kwargs):
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_dlist(dict_list)):
            pass
        else:
            return(None)
    else:
        pass
    if('deepcopy' in kwargs):
        deepcopy = kwargs['deepcopy']
    else:
        deepcopy = 0
    if(deepcopy):
        new = copy.deepcopy(dict_list)
    else:
        new = dict_list
    rslt = []
    if(isinstance(seqs_set,list)):
        real_seqs = seqs_set
    elif(isinstance(seqs_set,set)):
        real_seqs = list(seqs_set)
    else:
        print("Error: <seqs_set> Invalid")
        return(None)
    seqs = sorted(real_seqs)
    count = 0
    rslt = []
    for i in range(0,seqs.__len__()):
        rslt.append(new[seqs[i]])
    for i in range(0,seqs.__len__()):
        seq = seqs[i]
        seq = seq -count
        new.pop(seq)
        count = count + 1
    return(rslt)    

def rm_first(dict_list,**kwargs):
    if('mode' in kwargs):
        mode = kwargs['mode']
    else:
        mode = 'key'
    if('key' in kwargs):
        key = kwargs['key']
    if('value' in kwargs):
        value = kwargs['value']
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_dlist(dict_list)):
            pass
        else:
            return(None)
    else:
        pass
    if('deepcopy' in kwargs):
        deepcopy = kwargs['deepcopy']
    else:
        deepcopy = 0
    if(deepcopy):
        new = copy.deepcopy(dict_list)
    else:
        new = dict_list
    len = new.__len__()
    if(mode =='key'):
        for i in range(0,dict_list.__len__()):
            temp = dict_list[i]
            k = list(temp.keys())[0]
            v = list(temp.values())[0]
            if(k == key):
                new.remove(temp)
                break
    elif(mode == 'value'):
        for i in range(0,dict_list.__len__()):
            temp = dict_list[i]
            k = list(temp.keys())[0]
            v = list(temp.values())[0]
            if(v == value):
                new.remove(temp)
                break
    else:
        for i in range(0,dict_list.__len__()):
            temp = dict_list[i]
            k,v = dict2tuple(temp)
            if((k==key)&(v==value)):
                new.remove(temp)
                break
    return(new)

def rm_last(dict_list,**kwargs):
    if('mode' in kwargs):
        mode = kwargs['mode']
    else:
        mode = 'key'
    if('key' in kwargs):
        key = kwargs['key']
    if('value' in kwargs):
        value = kwargs['value']
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_dlist(dict_list)):
            pass
        else:
            return(None)
    else:
        pass
    if('deepcopy' in kwargs):
        deepcopy = kwargs['deepcopy']
    else:
        deepcopy = 0
    if(deepcopy):
        new = copy.deepcopy(dict_list)
    else:
        new = dict_list
    len = new.__len__()
    if(mode =='key'):
        for i in range(len-1,-1,-1):
            temp = dict_list[i]
            k = list(temp.keys())[0]
            v = list(temp.values())[0]
            if(k == key):
                new.pop(i)
                break
    elif(mode == 'value'):
        for i in range(len-1,-1,-1):
            temp = dict_list[i]
            k = list(temp.keys())[0]
            v = list(temp.values())[0]
            if(v == value):
                new.pop(i)
                break
    else:
        for i in range(len-1,-1,-1):
            temp = dict_list[i]
            k,v = dict2tuple(temp)
            if((k==key)&(v==value)):
                new.pop(i)
                break
    return(new)

def rm_all(dict_list,**kwargs):
    if('mode' in kwargs):
        mode = kwargs['mode']
    else:
        mode = 'key'
    if('key' in kwargs):
        key = kwargs['key']
    if('value' in kwargs):
        value = kwargs['value']
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_dlist(dict_list)):
            pass
        else:
            return(None)
    else:
        pass
    if('deepcopy' in kwargs):
        deepcopy = kwargs['deepcopy']
    else:
        deepcopy = 0
    if(deepcopy):
        new = copy.deepcopy(dict_list)
    else:
        new = dict_list
    len = new.__len__()
    ndl = []
    if(mode =='key'):
        for i in range(0,dict_list.__len__()):
            temp = dict_list[i]
            k = list(temp.keys())[0]
            v = list(temp.values())[0]
            if(k == key):
                pass
            else:
                ndl.append(temp)
    elif(mode == 'value'):
        for i in range(0,dict_list.__len__()):
            temp = dict_list[i]
            k = list(temp.keys())[0]
            v = list(temp.values())[0]
            if(v == value):
                pass
            else:
                ndl.append(temp)
    else:
        for i in range(0,dict_list.__len__()):
            temp = dict_list[i]
            k,v = dict2tuple(temp)
            if((k==key)&(v==value)):
                pass
            else:
                ndl.append(temp)
    new.clear()
    for i in range(0,ndl.__len__()):
        new.append(ndl[i])
    return(new)

def reverse(dict_list,**kwargs):
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_dlist(dict_list)):
            pass
        else:
            return(None)
    else:
        pass
    if('deepcopy' in kwargs):
        deepcopy = kwargs['deepcopy']
    else:
        deepcopy = 0
    if(deepcopy):
        new = copy.deepcopy(dict_list)
    else:
        new = dict_list
    new.reverse()
    return(new)


#######
#key
#value
#kv
#vk

def sort(dict_list,**kwargs):
    if('mode' in kwargs):
        mode = kwargs['mode']
    else:
        mode = 'kv'
    if('inverse' in kwargs):
        inverse = kwargs['inverse']
    else:
        inverse = False
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 0
    if(check):
        if(is_dlist(dict_list)):
            pass
        else:
            return(None)
    else:
        pass
    if('deepcopy' in kwargs):
        deepcopy = kwargs['deepcopy']
    else:
        deepcopy = 0
    if(deepcopy):
        new = copy.deepcopy(dict_list)
    else:
        new = dict_list
    def cmpvk(d1,d2):
        return(cmp_dele(d1,d2,mode='vk'))
    def cmpkv(d1,d2):
        return(cmp_dele(d1,d2,mode='kv'))
    if(mode == 'key'):
        new = sorted(new,reverse=inverse)
    elif(mode == 'value'):
        new = sorted(new, key=itemgetter(1),reverse=inverse)
    elif(mode == 'vk'):
        new = sorted(ndl,key=functools.cmp_to_key(cmpvk),reverse=inverse)
    else:
        new = sorted(ndl,key=functools.cmp_to_key(cmpkv),reverse=inverse)
    return(new)

#
def comprise(dict_list1,dict_list2,**kwargs):
    if('strict' in kwargs):
        strict = kwargs['strict']
    else:
        strict = 0
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_dlist(dict_list1)):
            pass
        else:
            return(None)
        if(is_dlist(dict_list2)):
            pass
        else:
            return(None)
    else:
        pass
    len_1 = dict_list1.__len__()
    len_2 = dict_list2.__len__()
    if(len_2>len_1):
        return(False)
    else:
        if(strict):
            if(dict_list2 == dict_list1[:len_2]):
                return(True)
            else:
                return(False)
        else:
            end = len_1 - len_2
            for i in range(0,end+1):
                if(dict_list2 == dict_list1[i:(i+len_2)]):
                    print(i)
                    return(i)
                else:
                    pass
            return(False)
           

#-----------------------------------
def tuple2dict(t):
    return({t[0]:t[1]})

def dict2tuple(d):
    return((list(d.keys())[0],list(d.values())[0]))


def dlist2tlist(dl):
    tl = []
    for i in range(0,dl.__len__()):
        ele = dict2tuple(dl[i])
        tl.append(ele)
    return(tl)

def tlist2dlist(tl):
    dl = []
    for i in range(0,tl.__len__()):
        ele = tuple2dict(tl[i])
        dl.append(ele)
    return(dl)


#------------------------

#dele {k:v}

def cmp_dele(d1,d2,**kwargs):
    def default_eq_func(value1,value2):
        cond = (value1 == value2)
        return(cond)
    def default_gt_func(value1,value2):
        cond = (value1 > value2)
        return(cond)
    def default_lt_func(value1,value2):
        cond = (value1 < value2)
        return(cond)
    if('eq_func' in kwargs):
        eq_func = kwargs['eq_func']
    else:
        eq_func = default_eq_func
    if('gt_func' in kwargs):
        gt_func = kwargs['gt_func']
    else:
        gt_func = default_gt_func
    if('lt_func' in kwargs):
        lt_func = kwargs['lt_func']
    else:
        lt_func = default_lt_func
    if('mode' in kwargs):
        mode = kwargs['mode']
    else:
        mode = 'kv'
    k1,v1 = dict2tuple(d1)
    k2,v2 = dict2tuple(d2)
    if(mode == 'key'):
        if(eq_func(k1,k2)):
            return(0)
        elif(gt_func(k1,k2)):
            return(1)
        else:
            return(-1)
    elif(mode == 'value'):
        if(eq_func(v1,v2)):
            return(0)
        elif(gt_func(v1,v2)):
            return(1)
        else:
            return(-1)
    elif(mode == 'vk'):
        if(eq_func(v1,v2)):
            if(eq_func(k1,k2)):
                return(0)
            elif(gt_func(k1,k2)):
                return(1)
            else:
                return(-1)
        elif(gt_func(v1,v2)):
            return(1)
        else:
            return(-1)
    else:
        if(eq_func(k1,k2)):
            if(eq_func(v1,v2)):
                return(0)
            elif(gt_func(v1,v2)):
                return(1)
            else:
                return(-1)
        elif(gt_func(k1,k2)):
            return(1)
        else:
            return(-1)


import elist.elist as elel
import copy
from operator import itemgetter
import functools

def is_tlist(obj,**kwargs):
    '''
        is_tlist([(1,2),(3,4)]) 
        is_tlist([(1,2,3),(4,5,6)])
        is_tlist([(1,2,3),(4,5,6)],width=3)
        
        is_tlist([(1,2),(3,)])
        is_tlist([(1,),(2,)])
        is_tlist([(1,),(2,)],width=1)
        
        
    '''
    if('width' in kwargs):
        width = kwargs['width']
    else:
        width = 2
    if(isinstance(obj,list)):
        pass
    else:
        return(False)
    if(obj == []):
        return(True)
    else:
        cond = True
        for each in obj:
            if(isinstance(each,tuple)):
                if(each.__len__()==width):
                    pass
                else:
                    return(False)
            else:
                return(False)
        return(cond)

#tlist2dict

def tlist2dict(tuple_list,**kwargs):
    '''
        #duplicate keys will lost
        tl = [(1,2),(3,4),(1,5)]
        tlist2dict(tl)
    '''
    if('deepcopy' in kwargs):
        deepcopy = kwargs['deepcopy']
    else:
        deepcopy = 1
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_tlist(tuple_list)):
            pass
        else:
            return(None)
    else:
        pass
    j = {}
    if(deepcopy):
        new = copy.deepcopy(tuple_list)
    else:
        new = tuple_list
    for i in range(0,new.__len__()):
        temp = new[i]
        key = temp[0]
        value = temp[1]
        j[key] = value
    return(j)

def dict2tlist(this_dict,**kwargs):
    '''
        #sequence will be losted
        d = {'a':'b','c':'d'}
        dict2tlist(d)
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
    tuple_list = []
    if(deepcopy):
        new = copy.deepcopy(this_dict)
    else:
        new = this_dict
    i = 0
    for key in this_dict:
        value = this_dict[key]
        tuple_list.append((key,value))
    return(tuple_list)

#kvlists     key-value-lists
#klist       key-list
#vlist       value-list

#tl          tuple-list

def kvlists2tl(klist,vlist,**kwargs):
    '''
        klist = ['k1','k2','k3']
        vlist = ['v1','v2','v3']
        kvlists2tlist(klist,vlist)
    '''
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
    tuple_list = []
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
        tuple_list.append((key,value))
    return(tuple_list)

kvlists2tlist = kvlists2tl

#
def tl2kvlists(tuple_list,**kwargs):
    '''
        tl = [('k1', 'v1'), ('k2', 'v2'), ('k3', 'v3')]
        kl,vl = tl2kvlists(tl)
        kl
        vl 
    '''
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_tlist(tuple_list)):
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
    len = tuple_list.__len__()
    if(deepcopy):
        new = copy.deepcopy(tuple_list)
    else:
        new = tuple_list
    for i in range(0,len):
        temp = new[i]
        key = temp[0]
        value = temp[1]
        kl.append(key)
        vl.append(value)
    return((kl,vl))


def _extend(tuple_list_1,tuple_list_2,**kwargs):
    '''
        tl1 = [('k1', 'v1'), ('k2', 'v2'), ('k3', 'v3')]
        tl2 = [('k4', 'v4'), ('k5', 'v5'), ('k6', 'v6')]
        extend(tl1,tl2)
    '''
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_tlist(tuple_list_1) & is_tlist(tuple_list_2)):
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
        new_1 = copy.deepcopy(tuple_list_1)
    else:
        new_1 = tuple_list_1
    if(deepcopy_2):
        new_2 = copy.deepcopy(tuple_list_2)
    else:
        new_2 = copy.copy(tuple_list_2)
    len_1 = new_1.__len__()
    len_2 = new_2.__len__()
    for i in range(0,len_2):
        new_1.append(new_2[i])
    return(new_1)

def _prextend(tuple_list_1,tuple_list_2,**kwargs):
    '''
        tl1 = [('k1', 'v1'), ('k2', 'v2'), ('k3', 'v3')]
        tl2 = [('k4', 'v4'), ('k5', 'v5'), ('k6', 'v6')]
        prexpend(tl1,tl2)
    '''
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_tlist(tuple_list_1) & is_tlist(tuple_list_2)):
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
        new_1 = copy.deepcopy(tuple_list_1)
    else:
        new_1 = tuple_list_1
    if(deepcopy_2):
        new_2 = copy.deepcopy(tuple_list_2)
    else:
        new_2 = copy.copy(tuple_list_2)
    len_1 = new_1.__len__()
    len_2 = new_2.__len__()
    swap = []
    for i in range(0,len_2):
        swap.append(new_2[i])
    for i in range(0,len_1):
        swap.append(new_1[i])
    return(swap)

def _concat(tuple_list_1,tuple_list_2,**kwargs):
    '''
        tl1 = [('k1', 'v1'), ('k2', 'v2'), ('k3', 'v3')]
        tl2 = [('k4', 'v4'), ('k5', 'v5'), ('k6', 'v6')]
        concat(tl1,tl2)
    '''
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_tlist(tuple_list_1) & is_tlist(tuple_list_2)):
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
        new_1 = copy.deepcopy(tuple_list_1)
    else:
        new_1 = tuple_list_1
    if(deepcopy_2):
        new_2 = copy.deepcopy(tuple_list_2)
    else:
        new_2 = tuple_list_2
    len_1 = new_1.__len__()
    len_2 = new_2.__len__()
    new = []
    for i in range(0,len_1):
        new.append(new_1[i])
    for i in range(0,len_2):
        new.append(new_2[i])
    return(new)

def first_continuous_indexes_slice(tuple_list,**kwargs):
    '''
        tl = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k31','v3'),('k32','v3'),('k33','v3'),('k4','v4'),('k4','v4'),('k5','v5')]
        first_continuous_indexes_slice(tl,key='k2')
        first_continuous_indexes_slice(tl,value='v3')
        first_continuous_indexes_slice(tl,kv=('k4','v4'))
        
    '''
    # if('mode' in kwargs):
        # mode = kwargs['mode']
    # else:
        # mode = 'key'
    if('kv' in kwargs):
        key = kwargs['kv'][0]
        value = kwargs['kv'][1]
        mode = 'kv'
    elif('key' in kwargs):
        key = kwargs['key']
        mode = 'key'
    elif('value' in kwargs):
        value = kwargs['value']
        mode = 'value'
    else:
        raise Exception("key or value or kv needed")
    if('start' in kwargs):
        start = kwargs['start']
    else:
        start = 0
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_tlist(tuple_list)):
            pass
        else:
            return(None)
    else:
        pass
    rslt = []
    begin = 0
    for i in range(start,tuple_list.__len__()):
        temp = tuple_list[i]
        k = temp[0]
        v = temp[1]
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
    for i in range(begin,tuple_list.__len__()):
        temp = tuple_list[i]
        k = temp[0]
        v = temp[1]
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

def last_continuous_indexes_slice(tuple_list,**kwargs):
    '''
        tl = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k31','v3'),('k32','v3'),('k33','v3'),('k2','v24'),('k2','v24'),('k5','v5')]
        last_continuous_indexes_slice(tl,key='k2')
        last_continuous_indexes_slice(tl,value='v3')
        last_continuous_indexes_slice(tl,kv=('k4','v4'))
        
    '''
    if('kv' in kwargs):
        key = kwargs['kv'][0]
        value = kwargs['kv'][1]
        mode = 'kv'
    elif('key' in kwargs):
        key = kwargs['key']
        mode = 'key'
    elif('value' in kwargs):
        value = kwargs['value']
        mode = 'value'
    else:
        raise Exception("key or value or kv needed")
    if('start' in kwargs):
        start = kwargs['start']
    else:
        start = -1
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_tlist(tuple_list)):
            pass
        else:
            return(None)
    else:
        pass
    if(start==-1):
        start = tuple_list.__len__()-1
    rslt = []
    begin = 0
    for i in range(start,-1,-1):
        temp = tuple_list[i]
        k = temp[0]
        v = temp[1]
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
        temp = tuple_list[i]
        k = temp[0]
        v = temp[1]
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

def all_continuous_indexes_slices(tuple_list,**kwargs):
    '''
        tl = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k31','v3'),('k32','v3'),('k33','v3'),('k2','v24'),('k2','v24'),('k5','v5')]
        all_continuous_indexes_slices(tl,key='k2')
        all_continuous_indexes_slices(tl,value='v3')
        all_continuous_indexes_slices(tl,kv=('k4','v4'))
        
    '''
    if('kv' in kwargs):
        key = kwargs['kv'][0]
        value = kwargs['kv'][1]
        mode = 'kv'
    elif('key' in kwargs):
        key = kwargs['key']
        mode = 'key'
    elif('value' in kwargs):
        value = kwargs['value']
        mode = 'value'
    else:
        raise Exception("key or value or kv needed")
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_tlist(tuple_list)):
            pass
        else:
            return(None)
    else:
        pass
    if('start' in kwargs):
        start = kwargs['start']
    else:
        start = 0
    lngth = tuple_list.__len__()
    sarray = []
    tl = tuple_list
    cursor = start
    rslt = ['dummy']
    while(rslt.__len__()!=0):
        rslt = first_continuous_indexes_slice(tl,start=cursor,**kwargs)
        if(rslt.__len__()==0):
            break
        else:
            sarray.append(rslt)
            cursor = rslt[-1]+1
    return(sarray)

def _indexes_all(tuple_list,**kwargs):
    '''
        tl = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k31','v3'),('k32','v3'),('k33','v3'),('k2','v24'),('k2','v24'),('k5','v5')]
        _indexes_all(tl,value = 'v3')
        _indexes_all(tl,key = 'k2')
        _indexes_all(tl,kv = ('k4','v4'))
        _indexes_all(tl,kv = ('k5','v5'))
    '''
    if('kv' in kwargs):
        key = kwargs['kv'][0]
        value = kwargs['kv'][1]
        mode = 'kv'
    elif('key' in kwargs):
        key = kwargs['key']
        mode = 'key'
    elif('value' in kwargs):
        value = kwargs['value']
        mode = 'value'
    else:
        raise Exception("key or value or kv needed")
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_tlist(tuple_list)):
            pass
        else:
            return(None)
    else:
        pass
    rslt = []
    for i in range(0,tuple_list.__len__()):
        temp = tuple_list[i]
        k = temp[0]
        v = temp[1]
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

def _index_first(tuple_list,**kwargs):
    '''
        tl = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k31','v3'),('k32','v3'),('k33','v3'),('k2','v24'),('k2','v24'),('k5','v5')]
        index_first(tl,value = 'v3')
        index_first(tl,key = 'k2')
        index_first(tl,kv = ('k4','v4'))
        index_first(tl,kv = ('k5','v5'))
    '''
    if('mode' in kwargs):
        mode = kwargs['mode']
    else:
        mode = 'key'
    if('kv' in kwargs):
        key = kwargs['kv'][0]
        value = kwargs['kv'][1]
        mode = 'kv'
    elif('key' in kwargs):
        key = kwargs['key']
        mode = 'key'
    elif('value' in kwargs):
        value = kwargs['value']
        mode = 'value'
    else:
        raise Exception("key or value or kv needed")
    if('start' in kwargs):
        start = kwargs['start']
    else:
        start = 0
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_tlist(tuple_list)):
            pass
        else:
            return(None)
    else:
        pass
    for i in range(start,tuple_list.__len__()):
        temp = tuple_list[i]
        k = temp[0]
        v = temp[1]
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

def _index_last(tuple_list,**kwargs):
    '''
        tl = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k31','v3'),('k32','v3'),('k33','v3'),('k2','v24'),('k2','v24'),('k5','v5')]
        index_last(tl,value = 'v3')
        index_last(tl,key = 'k2')
        index_last(tl,kv = ('k4','v4'))
        index_last(tl,kv = ('k5','v5'))
    '''
    if('kv' in kwargs):
        key = kwargs['kv'][0]
        value = kwargs['kv'][1]
        mode = 'kv'
    elif('key' in kwargs):
        key = kwargs['key']
        mode = 'key'
    elif('value' in kwargs):
        value = kwargs['value']
        mode = 'value'
    else:
        raise Exception("key or value or kv needed")
    if('start' in kwargs):
        start = kwargs['start']
    else:
        start = -1
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_tlist(tuple_list)):
            pass
        else:
            return(None)
    else:
        pass
    if(start == -1):
        start = tuple_list.__len__() - 1
    for i in range(start,-1,-1):
        temp = tuple_list[i]
        k = temp[0]
        v = temp[1]
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

def _append(tuple_list,*args,**kwargs):
    '''
        tl = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k31','v3'),('k32','v3'),('k33','v3'),('k2','v24'),('k2','v24'),('k5','v5')]
        append(tl,'k6','v6')
        append(tl,('k6','v6'))
    '''
    args = list(args)
    if(args.__len__() == 1):
        key,value = args[0]
    else:
        key = args[0]
        value = args[1]
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_tlist(tuple_list)):
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
        new = copy.deepcopy(tuple_list)
    else:
        new = tuple_list
    new.append((key,value))
    return(new)

def _prepend(tuple_list,*args,**kwargs):
    '''
        tl = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k31','v3'),('k32','v3'),('k33','v3'),('k2','v24'),('k2','v24'),('k5','v5')]
        prepend(tl,'k6','v6')
        prepend(tl,('k6','v6'))
    '''
    args = list(args)
    if(args.__len__() == 1):
        key,value = args[0]
    else:
        key = args[0]
        value = args[1]
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_tlist(tuple_list)):
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
        new = copy.deepcopy(tuple_list)
    else:
        new = tuple_list
    len = tuple_list.__len__()
    swap = []
    swap.append((key,value))
    for i in range(0,len):
        swap.append(new[i])
    return(swap)

def _clear(tuple_list,**kwargs):
    '''
    '''
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_tlist(tuple_list)):
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
        new = []
    else:
        new = tuple_list
        new.clear()
    return(new)

def _deepcopy(tuple_list,**kwargs):
    '''
    '''
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_tlist(tuple_list)):
            pass
        else:
            return(None)
    else:
        pass
    tuple_list = copy.deepcopy(tuple_list)
    return(tuple_list)

def _insert(tuple_list,index,*args,**kwargs):
    '''
        tl = [('k1','v1'),('k2','v2'),('k3','v3'),('k4','v4')]
        insert(tl,0,'k6','v6')
        insert(tl,1,('k6','v6'))
        insert(tl,2,'k6','v6')
        insert(tl,3,('k6','v6'))
        insert(tl,4,'k6','v6')
        
        tl
        insert(tl,2,'k6','v6',deepcopy=0)
        tl
    '''
    lngth = tuple_list.__len__()
    index = elel.uniform_index(index,lngth)
    args = list(args)
    if(args.__len__() == 1):
        key,value = args[0]
    else:
        key = args[0]
        value = args[1]
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_tlist(tuple_list)):
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
        new = copy.deepcopy(tuple_list)
    else:
        new = tuple_list
    new.insert(index,(key,value))
    return(new)

def _insert_sec(tuple_list_1,index,tuple_list_2,**kwargs):
    '''
        tl1 = [("k1","v1"),("k2","v2"),("k3","v3")]
        tl2 = [("k4","v4"),("k5","v5"),("k6","v6")]
        insert_sec(tl1,0,tl2)
        insert_sec(tl1,1,tl2)
        insert_sec(tl1,2,tl2)
        insert_sec(tl1,3,tl2)
    '''
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_tlist(tuple_list_1) & is_tlist(tuple_list_2)):
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
        new_1 = copy.deepcopy(tuple_list_1)
    else:
        new_1 = tuple_list_1
    if(deepcopy_2):
        new_2 = copy.deepcopy(tuple_list_2)
    else:
        new_2 = copy.copy(tuple_list_2)
    rslt = elel.insert_section(tuple_list_1,tuple_list_2,index)
    return(rslt)

def _includes(tuple_list,**kwargs):
    '''
        tl = [('k1','v1'),('k2','v2'),('k3','v3'),('k4','v4')]
        includes(tl,key='k2')
        includes(tl,value='v3')
        includes(tl,kv=('k2','v3'))
        includes(tl,kv=('k2','v2'))
        includes(tl,kv=('k4','v4'))
    '''
    if('kv' in kwargs):
        key = kwargs['kv'][0]
        value = kwargs['kv'][1]
        mode = 'kv'
    elif('key' in kwargs):
        key = kwargs['key']
        mode = 'key'
    elif('value' in kwargs):
        value = kwargs['value']
        mode = 'value'
    else:
        raise Exception("key or value or kv needed")
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_tlist(tuple_list)):
            pass
        else:
            return(None)
    else:
        pass
    if(mode =='key'):
        for i in range(0,tuple_list.__len__()):
            temp = tuple_list[i]
            k = temp[0]
            v = temp[1]
            if(k == key):
                return(True)
    elif(mode == 'value'):
        for i in range(0,tuple_list.__len__()):
            temp = tuple_list[i]
            k = temp[0]
            v = temp[1]
            if(v == value):
                return(True)
    else:
        for i in range(0,tuple_list.__len__()):
            temp = tuple_list[i]
            k = temp[0]
            v = temp[1]
            if((k==key)&(v==value)):
                return(True)
    return(False)

def _count(tuple_list,**kwargs):
    '''
        tl = [('k1','v1'),('k2','v21'),('k2','v22'),('k31','v3'),('k3','v3'),('k4','v4'),('k4','v4')]
        count(tl,key='k2')
        count(tl,value='v3')
        count(tl,kv=('k2','v2'))
        count(tl,kv=('k4','v4'))
    '''
    if('kv' in kwargs):
        key = kwargs['kv'][0]
        value = kwargs['kv'][1]
        mode = 'kv'
    elif('key' in kwargs):
        key = kwargs['key']
        mode = 'key'
    elif('value' in kwargs):
        value = kwargs['value']
        mode = 'value'
    else:
        raise Exception("key or value or kv needed")
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_tlist(tuple_list)):
            pass
        else:
            return(None)
    else:
        pass
    num = 0
    if(mode =='key'):
        for i in range(0,tuple_list.__len__()):
            temp = tuple_list[i]
            k = temp[0]
            v = temp[1]
            if(k == key):
                num = num + 1
    elif(mode == 'value'):
        for i in range(0,tuple_list.__len__()):
            temp = tuple_list[i]
            k = temp[0]
            v = temp[1]
            if(v == value):
                num = num + 1
    else:
        for i in range(0,tuple_list.__len__()):
            temp = tuple_list[i]
            k = temp[0]
            v = temp[1]
            if((k==key)&(v==value)):
                num = num + 1
    return(num)

def _pop_all(tuple_list,*args,**kwargs):
    '''
        tl = [('k1','v1'),('k2','v21'),('k2','v22'),('k31','v3'),('k3','v3'),('k4','v4'),('k4','v4')]
        pop_all(tl,key='k2')
        tl
        tl = [('k1','v1'),('k2','v21'),('k2','v22'),('k31','v3'),('k3','v3'),('k4','v4'),('k4','v4')]
        pop_all(tl,1)
        tl
        tl = [('k1','v1'),('k2','v21'),('k2','v22'),('k31','v3'),('k3','v3'),('k4','v4'),('k4','v4')]
        pop_all(tl,3)
        tl
    '''
    args = list(args)
    if('key' in kwargs):
        key = kwargs['key']
        mode = 'key'
    elif('value' in kwargs):
        value = kwargs['value']
        mode = 'value'
    elif(args.__len__()>0):
        index = args[0]
        mode = 'index'
    else:
        raise Exception("key or value or kv needed")
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_tlist(tuple_list)):
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
        new = copy.deepcopy(tuple_list)
    else:
        new = tuple_list
    len = tuple_list.__len__()
    if(mode == 'index'):
        if(index in range(0,len)):
            rslt = new.pop(index)
        else:
            rslt = None
    else:
        rslt = []
        seqs = _indexes_all(tuple_list,**kwargs)
        rslt = elel.pop_indexes(tuple_list,seqs,mode='original')
    return(rslt)

def _pop_range(tuple_list,start,end,**kwargs):
    '''
        tl = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k3','v3'),('k2','v24'),('k4','v4')]
        pop_range(tl,0,2,key='k2')
        tl
        tl = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k3','v3'),('k2','v24'),('k4','v4')]
        pop_range(tl,1,4,key='k2')
        tl
        tl = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k3','v3'),('k2','v24'),('k4','v4')]
        pop_range(tl,1,4)
        tl
        tl = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k3','v3'),('k2','v24'),('k4','v4')]
        pop_range(tl,3,5)
        tl
    '''
    if('key' in kwargs):
        key = kwargs['key']
        mode = 'key'
    elif('value' in kwargs):
        value = kwargs['value']
        mode = 'value'
    else:
        mode = 'index'
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_tlist(tuple_list)):
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
        new = copy.deepcopy(tuple_list)
    else:
        new = tuple_list
    if(mode == 'index'):
        rslt = elel.pop_range(tuple_list,start,end,mode='original')
    else:
        seqs = _indexes_all(tuple_list,**kwargs)
        seqs = seqs[start:end]
        rslt = elel.pop_indexes(tuple_list,seqs,mode='original')
    return(rslt)

def _pop_seqs(tuple_list,seqs,**kwargs):
    '''
        tl = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k3','v3'),('k2','v24'),('k4','v4')]
        pop_seqs(tl,{0,2},key='k2')
        tl
        tl = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k3','v3'),('k2','v24'),('k4','v4')]
        pop_seqs(tl,{1,3},key='k2')
        tl
        tl = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k3','v3'),('k2','v24'),('k4','v4')]
        pop_seqs(tl,{1,4})
        tl
        tl = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k3','v3'),('k2','v24'),('k4','v4')]
        pop_seqs(tl,{3,5})
        tl
    '''
    if('key' in kwargs):
        key = kwargs['key']
        mode = 'key'
    elif('value' in kwargs):
        value = kwargs['value']
        mode = 'value'
    else:
        mode = 'index'
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_tlist(tuple_list)):
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
        new = copy.deepcopy(tuple_list)
    else:
        new = tuple_list
    len = new.__len__()
    rslt = []
    if(isinstance(seqs,list)):
        pass
    elif(isinstance(seqs,set)):
        seqs = list(seqs)
    else:
        print("Error: <seqs> Invalid")
        return(None)
    if(mode == 'index'):
        rslt = elel.pop_indexes(tuple_list,seqs,mode='original')
    else:
        all_matched = _indexes_all(tuple_list,**kwargs)
        seqs = elel.select_seqs(all_matched,seqs)
        rslt = elel.pop_indexes(tuple_list,seqs,mode='original')
    return(rslt)



def _remove_first(tuple_list,**kwargs):
    '''
        tl = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k3','v3'),('k2','v24'),('k4','v4')]
        remove_first(tl,key='k2')
        tl
        tl = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k3','v3'),('k2','v24'),('k4','v4')]
        remove_first(tl,value='v3')
        tl
        tl = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k3','v3'),('k2','v24'),('k4','v4')]
        remove_first(tl,kv=('k4','v4'))
        tl
        tl = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k3','v3'),('k2','v24'),('k4','v4')]
        remove_first(tl,kv=('k1','v1'))
        tl
    '''
    if('kv' in kwargs):
        key = kwargs['kv'][0]
        value = kwargs['kv'][1]
        mode = 'kv'
    elif('key' in kwargs):
        key = kwargs['key']
        mode = 'key'
    elif('value' in kwargs):
        value = kwargs['value']
        mode = 'value'
    else:
        raise Exception("key or value or kv needed")
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_tlist(tuple_list)):
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
        new = copy.deepcopy(tuple_list)
    else:
        new = tuple_list
    len = new.__len__()
    if(mode =='key'):
        for i in range(0,tuple_list.__len__()):
            temp = tuple_list[i]
            k = temp[0]
            v = temp[1]
            if(k == key):
                new.remove(temp)
                break
    elif(mode == 'value'):
        for i in range(0,tuple_list.__len__()):
            temp = tuple_list[i]
            k = temp[0]
            v = temp[1]
            if(v == value):
                new.remove(temp)
                break
    else:
        for i in range(0,tuple_list.__len__()):
            temp = tuple_list[i]
            k = temp[0]
            v = temp[1]
            if((k==key)&(v==value)):
                new.remove(temp)
                break
    return(new)

def _remove_last(tuple_list,**kwargs):
    '''
        tl = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k3','v3'),('k2','v24'),('k4','v4')]
        remove_last(tl,key='k2')
        tl
        tl = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k3','v3'),('k2','v24'),('k4','v4')]
        remove_last(tl,value='v3')
        tl
        tl = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k3','v3'),('k2','v24'),('k4','v4')]
        remove_last(tl,kv=('k4','v4'))
        tl
        tl = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k3','v3'),('k2','v24'),('k4','v4')]
        remove_last(tl,kv=('k1','v1'))
        tl
    '''
    if('kv' in kwargs):
        key = kwargs['kv'][0]
        value = kwargs['kv'][1]
        mode = 'kv'
    elif('key' in kwargs):
        key = kwargs['key']
        mode = 'key'
    elif('value' in kwargs):
        value = kwargs['value']
        mode = 'value'
    else:
        raise Exception("key or value or kv needed")
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_tlist(tuple_list)):
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
        new = copy.deepcopy(tuple_list)
    else:
        new = tuple_list
    len = new.__len__()
    if(mode =='key'):
        for i in range(len-1,-1,-1):
            temp = tuple_list[i]
            k = temp[0]
            v = temp[1]
            if(k == key):
                new.remove(temp)
                break
    elif(mode == 'value'):
        for i in range(len-1,-1,-1):
            temp = tuple_list[i]
            k = temp[0]
            v = temp[1]
            if(v == value):
                new.remove(temp)
                break
    else:
        for i in range(len-1,-1,-1):
            temp = tuple_list[i]
            k = temp[0]
            v = temp[1]
            if((k==key)&(v==value)):
                new.remove(temp)
                break
    return(new)




def _remove_which(tuple_list,which,**kwargs):
    '''
        tl = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k3','v3'),('k2','v24'),('k4','v4')]
        _remove_which(tl,0,key='k2')
        tl
        tl = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k3','v3'),('k2','v24'),('k4','v4')]
        _remove_which(tl,1,value='v3')
        tl
        tl = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k3','v3'),('k2','v24'),('k4','v4')]
        _remove_which(tl,0,kv=('k4','v4'))
        tl
        tl = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k3','v3'),('k2','v24'),('k4','v4')]
        _remove_which(tl,1,kv=('k1','v1'))
        tl
    '''
    if('kv' in kwargs):
        key = kwargs['kv'][0]
        value = kwargs['kv'][1]
        mode = 'kv'
    elif('key' in kwargs):
        key = kwargs['key']
        mode = 'key'
    elif('value' in kwargs):
        value = kwargs['value']
        mode = 'value'
    else:
        raise Exception("key or value or kv needed")
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_tlist(tuple_list)):
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
        new = copy.deepcopy(tuple_list)
    else:
        new = tuple_list
    len = new.__len__()
    c = 0
    if(mode =='key'):
        for i in range(0,tuple_list.__len__()):
            temp = tuple_list[i]
            k = temp[0]
            v = temp[1]
            if(k == key):
                if(c == which):
                    new.remove(temp)
                    break
                else:
                    c = c + 1
            else:
                pass
    elif(mode == 'value'):
        for i in range(0,tuple_list.__len__()):
            temp = tuple_list[i]
            k = temp[0]
            v = temp[1]
            if(v == value):
                if(c == which):
                    new.remove(temp)
                    break
                else:
                    c = c + 1
            else:
                pass
    else:
        for i in range(0,tuple_list.__len__()):
            temp = tuple_list[i]
            k = temp[0]
            v = temp[1]
            if((k==key)&(v==value)):
                if(c == which):
                    new.remove(temp)
                    break
                else:
                    c = c + 1
            else:
                pass
    return(new)




def _remove_all(tuple_list,**kwargs):
    '''
        tl = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k3','v3'),('k2','v24'),('k4','v4')]
        remove_all(tl,key='k2')
        tl
        tl = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k3','v3'),('k2','v24'),('k4','v4')]
        remove_all(tl,value='v3')
        tl
        tl = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k3','v3'),('k2','v24'),('k4','v4')]
        remove_all(tl,kv=('k4','v4'))
        tl
        tl = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k3','v3'),('k2','v24'),('k4','v4')]
        remove_all(tl,kv=('k1','v1'))
        tl
    '''
    if('kv' in kwargs):
        key = kwargs['kv'][0]
        value = kwargs['kv'][1]
        mode = 'kv'
    elif('key' in kwargs):
        key = kwargs['key']
        mode = 'key'
    elif('value' in kwargs):
        value = kwargs['value']
        mode = 'value'
    else:
        raise Exception("key or value or kv needed")
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_tlist(tuple_list)):
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
        new = copy.deepcopy(tuple_list)
    else:
        new = tuple_list
    len = new.__len__()
    i = 0
    if(mode =='key'):
        for i in range(0,tuple_list.__len__()):
            temp = tuple_list[i]
            k = temp[0]
            v = temp[1]
            if(k == key):
                new.remove(temp)
    elif(mode == 'value'):
        for i in range(0,tuple_list.__len__()):
            temp = tuple_list[i]
            k = temp[0]
            v = temp[1]
            if(v == value):
                new.remove(temp)
    else:
        for i in range(0,tuple_list.__len__()):
            temp = tuple_list[i]
            k = temp[0]
            v = temp[1]
            if((k==key)&(v==value)):
                new.remove(temp)
    return(new)

def _reverse(tuple_list,**kwargs):
    '''
        tl = [('k1','v1'),('k2','v2'),('k3','v3'),('k4','v4')]
        reverse(tl)
    '''
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = 1
    if(check):
        if(is_tlist(tuple_list)):
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
        new = copy.deepcopy(tuple_list)
    else:
        new = tuple_list
    len = new.__len__()
    new.reverse()
    return(new)

def _sort(tuple_list,**kwargs):
    '''
        tl = [('k2','v1'),('k1','v2'),('k4','v3'),('k3','v4')]
        sort(tl)
        sort(tl,mode='key')
        sort(tl,mode='value')
        
        #first compare key, then compare value
        tl = [('k2','v1'),('k1','v2'),('k2','v3'),('k1','v4')]
        sort(tl,mode='kv')
        #first compare value, then compare key
        tl = [('k2','v1'),('k1','v4'),('k2','v1'),('k1','v4')]
        sort(tl,mode='vk')
    '''
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
        check = 1
    if(check):
        if(is_tlist(tuple_list)):
            pass
        else:
            return(None)
    else:
        pass
    def cmpkv(kv1,kv2):
        '''
        '''
        for i in range(0,2):
            key = i
            cond = (kv1[i] == kv2[i])
            if(cond):
                pass
            else:
                cond = (kv1[i] > kv2[i])
                if(cond):
                    return(1)
                else:
                    return(-1)
        return(0)
    def cmpvk(kv1,kv2):
        '''
        '''
        for i in range(1,-1,-1):
            key = i
            cond = (kv1[i] == kv2[i])
            if(cond):
                pass
            else:
                cond = (kv1[i] > kv2[i])
                if(cond):
                    return(1)
                else:
                    return(-1)
        return(0)
    if('deepcopy' in kwargs):
        deepcopy = kwargs['deepcopy']
    else:
        deepcopy = 1
    if(deepcopy):
        new = copy.deepcopy(tuple_list)
    else:
        new = tuple_list
    len = new.__len__()
    if(mode == 'key'):
        new = sorted(new,key=itemgetter(0),reverse=inverse)
    elif(mode == 'value'):
        new = sorted(new, key=itemgetter(1),reverse=inverse)
    elif(mode == 'kv'):
        new = sorted(new,key=functools.cmp_to_key(cmpkv),reverse=inverse)
    else:
        new = sorted(new,key=functools.cmp_to_key(cmpvk),reverse=inverse)
    return(new)

def _comprise(tuple_list1,tuple_list2,**kwargs):
    '''
        tl1 = [('k1','v1'),('k2','v2'),('k3','v3'),('k4','v4'),('k5','v5'),('k6','v6')]
        tl2 = [('k1','v1'),('k2','v2'),('k3','v3'),('k4','v4')]
        _comprise(tl1,tl2,mode='strict')
        tl1 = [('k1','v1'),('k2','v2'),('k3','v3'),('k4','v4'),('k5','v5'),('k6','v6')]
        tl2 = [('k2','v2'),('k3','v3'),('k4','v4')]
        _comprise(tl1,tl2,mode='strict')
        _comprise(tl1,tl2,mode='middle')
        tl1 = [('k1','v1'),('k2','v2'),('k3','v3'),('k4','v4'),('k5','v5'),('k6','v6')]
        tl2 = [('k3','v3'),('k4','v4'),('k2','v2')]
        _comprise(tl1,tl2,mode='middle')
        _comprise(tl1,tl2,mode='loose')
    '''
    if('mode' in kwargs):
        mode = kwargs['mode']
    else:
        mode = 'loose'
    if('check' in kwargs):
        check = kwargs['check']
    else:
        check = True
    if(check):
        if(is_tlist(tuple_list1)):
            pass
        else:
            return(None)
        if(is_tlist(tuple_list2)):
            pass
        else:
            return(None)
    else:
        pass
    len_1 = tuple_list1.__len__()
    len_2 = tuple_list2.__len__()
    if(len_2>len_1):
        return(False)
    else:
        if(mode == 'strict'):
            if(tuple_list2 == tuple_list1[:len_2]):
                return(True)
            else:
                return(False)
        elif(mode == 'middle'):
            end = len_1 - len_2
            for i in range(0,end+1):
                if(tuple_list2 == tuple_list1[i:(i+len_2)]):
                    return(True)
                else:
                    pass
            return(False)
        else:
            cond =True
            for each in tuple_list2:
                if(each in tuple_list1):
                    pass
                else:
                    return(False)
            return(cond)

def tlist2dlist(tl):
    '''
        tl1 = [('k1','v1'),('k2','v2'),('k3','v3'),('k4','v4'),('k5','v5'),('k6','v6')]
        dl = tlist2dlist(tl)
        pobj(dl)
    '''
    dl =[]
    for i in range(0,tl.__len__()):
        ele = {tl[i][0] : tl[i][1]}
        dl.append(ele)
    return(dl)

def dlist2tlist(dl):
    '''
        dl = [{'k2': 'v1'}, {'k1': 'v4'}, {'k2': 'v1'}, {'k1': 'v4'}]
        tl = dlist2tlist(dl)
        tl
    '''
    dl =[]
    for i in range(0,tl.__len__()):
        ele = {tl[i][0] : tl[i][1]}
        dl.append(ele)
    return(dl)

def set_which(tl,*args,**kwargs):
    '''
        tl1 = [('k1','v1'),('k1','v1'),('k31','v3'),('k32','v3'),('k4','v41'),('k4','v42'),('k1','v1')]
        set_which(tl1,'k1','v11',mode='key',which=1)
        tl1 = [('k1','v1'),('k1','v1'),('k31','v3'),('k32','v3'),('k4','v41'),('k4','v42'),('k1','v1')]
        set_which(tl1,'k1','v11',mode='key',which=2)
        tl1 = [('k1','v1'),('k1','v1'),('k31','v3'),('k32','v3'),('k4','v41'),('k4','v42'),('k1','v1')]
        set_which(tl1,'k3','v3',mode='value')
        tl1 = [('k1','v1'),('k1','v1'),('k31','v3'),('k32','v3'),('k4','v41'),('k4','v42'),('k1','v1')]
        set_which(tl1,'k3','v3',mode='kv',which=5)
    '''
    if('mode' in kwargs):
        mode = kwargs['mode']
    else:
        mode = 'key'
    if('which' in kwargs):
        which = kwargs['which']
    else:
        which = 'all'
    args = list(args)
    if(args.__len__() == 1):
        key,value = args[0]
    elif(args.__len__() == 2):
        key = args[0]
        value = args[1]
    else:
        raise Exception("key or value or kv needed")
    length = tl.__len__()
    cursor = 0
    for i in range(0,length):
        t = tl[i]
        k = t[0]
        v = t[1]
        if(mode == 'key'):
            match = (k == key)
        elif(mode == 'value'):
            match = (v == value)
        else:
            match = True
        if(match):
            if(which == 'all'):
                cond = True
            else:
                cond = (cursor == which)
            if(cond):
                nt = (key,value)
                tl[i] = nt
                if(which=='all'):
                    pass
                else:
                    break
            else:
                pass
            cursor = cursor + 1
        else:
            pass
    return(tl)

def get_value(tl,key,**kwargs):
    '''
        tl = [('k1','v11'),('k1','v12'),('k31','v3'),('k32','v3'),('k4','v41'),('k4','v42'),('k1','v13')]
        get_value(tl,'k1')
        get_value(tl,'k1',whiches=1)
        get_value(tl,'k1',whiches=[1,2])
        
    '''
    single = False
    if('mode' in kwargs):
        mode = kwargs['mode']
    else:
        mode = 'key'
    if('whiches' in kwargs):
        whiches = kwargs['whiches']
    else:
        whiches = 'all'
    if(isinstance(whiches,list)):
        pass
    elif(isinstance(whiches,int)):
        single = True
        whiches = [whiches]
    else:
        pass
    length = tl.__len__()
    rslt = []
    cursor = 0
    for i in range(0,length):
        t = tl[i]
        k = t[0]
        v = t[1]
        if(k == key):
            if(whiches == 'all'):
                cond = True
            else:
                cond = (cursor in whiches)
            if(cond):
                if(single==False):
                    rslt.append(v)
                else:
                    return(v)
            else:
                pass
            cursor = cursor + 1
        else:
            pass
    if(single == True):
        raise KeyError(key)
    else:
        return(rslt)

def get_key(tl,value,**kwargs):
    '''
        tl = [('k1','v11'),('k1','v12'),('k31','v3'),('k32','v3'),('k4','v41'),('k33','v3'),('k1','v13')]
        get_key(tl,'v3')
        get_key(tl,'v3',whiches=1)
        get_key(tl,'v3',whiches=[1,2])
        
    '''
    single = False
    if('mode' in kwargs):
        mode = kwargs['mode']
    else:
        mode = 'key'
    if('whiches' in kwargs):
        whiches = kwargs['whiches']
    else:
        whiches = 'all'
    if(isinstance(whiches,list)):
        pass
    elif(isinstance(whiches,int)):
        single = True
        whiches = [whiches]
    else:
        pass
    length = tl.__len__()
    rslt = []
    cursor = 0
    for i in range(0,length):
        t = tl[i]
        k = t[0]
        v = t[1]
        if(v == value):
            if(whiches == 'all'):
                cond = True
            else:
                cond = (cursor in whiches)
            if(cond):
                if(single==False):
                    rslt.append(k)
                else:
                    return(k)
            else:
                pass
            cursor = cursor + 1
        else:
            pass
    if(single == True):
        raise ValueError(value)
    else:
        return(rslt)

#######
def list2tl(arr):
    kl = elel.select_odds(arr)
    vl = elel.select_evens(arr)
    tl = kvlists2tl(kl,vl)
    return(tl)
####### 

#################

def uniqualize(tl,*args,**kwargs):
    kl,vl = tl2kvlists(tl)
    if('mode' in kwargs):
        mode = kwargs['mode']
    else:
        mode = "key"
    if(mode == "key"):
        key = args[0]
    elif(mode == "value"):
        value = args[0]
    else:
        key = args[0]
        value = args[1]
    lngth = kl.__len__()
    nkl = []
    nvl = []
    for i in range(0,lngth):
        k = kl[i]
        v = vl[i]
        if(mode == 'key'):
            cond = (k == key)
        elif(mode == "value"):
            cond = (v == value)
        else:
            cond = ((k == key)&(v == value))
        if(cond):
            if(k in nkl):
                pass
            else:
                nkl.append(k)
                nvl.append(v)
        else:
            nkl.append(k)
            nvl.append(v)
    ntl = kvlists2tl(nkl,nvl)
    return(ntl)


def uniqualize_all(tl,**kwargs):
    kl,vl = tl2kvlists(tl)
    if('mode' in kwargs):
        mode = kwargs['mode']
    else:
        mode = "key"
    lngth = kl.__len__()
    nkl = []
    nvl = []
    ntl = []
    for i in range(0,lngth):
        k = kl[i]
        v = vl[i]
        if(mode == "key"):
            cond = (k in nkl)
        elif(mode == "value"):
            cond = (v in nvl)
        else:
            cond = ((k,v) in ntl)
        if(cond):
            pass
        else:
            nkl.append(k)
            nvl.append(v)
            ntl.append((k,v))
    return(ntl)

#################
#tele  (k1,v1)

def cmp_tele(t1,t2,**kwargs):
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
    k1,v1 = t1
    k2,v2 = t2
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


#################

class Tlist():
    def __init__(self,*args,**kwargs):
        '''
            x = [('k1','v11'),('k2','v21'),('k3','v31')]
            tl = Tlist(x)
            tl
            
            x = {'k1': 'v11', 'k2': 'v21', 'k3': 'v31'}
            tl = Tlist(x)
            tl
            
            kl = ['k1', 'k2', 'k3']
            vl = ['v11', 'v21', 'v31']
            tl = Tlist(kl,vl)
            tl
            
        '''
        args = list(args)
        lngth = args.__len__()
        if(lngth == 1):
            x = args[0]
            if(isinstance(x,dict)):
                tl = dict2tlist(x)
            else:
                tl = x
        elif(lngth == 0):
            raise ValueError("dict-list or tuple-list or key-list+value-list needed")
        else:
            x = args[0]
            y = args[1]
            tl = kvlists2tl(x,y,**kwargs)
        self.tl = tl
    def __repr__(self):
        return(self.tl.__repr__())
    def __str__(self):
        return(self.tl.__str__())
    def __getitem__(self,*args,**kwargs):
        '''
            x = [('k1','v11'),('k1','v12'),('k31','v3'),('k32','v3'),('k4','v41'),('k4','v42'),('k1','v13')]
            tl = Tlist(x)
            tl['k1']
            tl['k1',0,2]
            tl['k1',0]
            tl['k1',1]
            tl['k1',2]
            tl['k31']
        ''' 
        if(isinstance(args[0],tuple)):
            #very special in __getitem__
            args = list(args[0])
            key = args[0]
            whiches = elel.array_map(args[1:],int)
            rslt = get_value(self.tl,key,whiches=whiches)
        else:
            #very special in __getitem__
            key = args[0]
            rslt = get_value(self.tl,key)
        if(rslt.__len__() == 1):
            return(rslt[0])
        else:
            return(rslt)
    def key(self,*args,**kwargs):
        '''
            x = [('k1','v11'),('k1','v12'),('k31','v3'),('k32','v3'),('k4','v41'),('k4','v42'),('k1','v13')]
            tl = Tlist(x)
            tl.key('v3')
            tl.key('v3',0)
            tl.key('v3',1)
            tl.key('k1',1)
            tl.key('k1',2)
            tl.key('v41')
        ''' 
        if(isinstance(args[0],tuple)):
            #very special in __getitem__
            args = list(args[0])
            value = args[0]
            whiches = elel.array_map(args[1:],int)
            rslt = get_key(self.tl,value,whiches=whiches)
        else:
            #very special in __getitem__
            value = args[0]
            rslt = get_key(self.tl,value)
        if(rslt.__len__() == 1):
            return(rslt[0])
        else:
            return(rslt)
    def __setitem__(self,*args,**kwargs):
        '''
            #set all 
            x = [('k1','v1'),('k1','v1'),('k31','v3'),('k32','v3'),('k4','v41'),('k4','v42'),('k1','v1')]
            tl = Tlist(x)
            tl
            tl['k1'] = 'v11'
            tl
            
            #set_which(tl1,'k1','v11',mode='key',which=1)
            x = [('k1','v1'),('k1','v1'),('k31','v3'),('k32','v3'),('k4','v41'),('k4','v42'),('k1','v1')]
            tl = Tlist(x)
            tl
            tl['k1',1] = 'v11'
            tl
            
            #set_which(tl1,'k1','v11',mode='key',which=2)
            x = [('k1','v1'),('k1','v1'),('k31','v3'),('k32','v3'),('k4','v41'),('k4','v42'),('k1','v1')]
            tl = Tlist(x)
            tl
            tl['k1',2] = 'v11'
            tl
            
            #
            x = [('k1','v1'),('k1','v1'),('k31','v3'),('k32','v3'),('k4','v41'),('k4','v42'),('k1','v1')]
            tl = Tlist(x)
            tl
            tl['k1',0,2] = 'v11'
            tl
            
        '''
        if(isinstance(args[0],tuple)):
            #very special in __getitem__
            value = args[-1]
            args = list(args[0])
            key = args[0]
            whiches = elel.array_map(args[1:],int)
            rslt = self.tl
            for which in whiches:
                rslt = set_which(rslt,key,value,which=which)
        else:
            #very special in __getitem__
            key = args[0]
            value = args[-1]
            rslt = set_which(self.tl,key,value,which='all')
        if(rslt.__len__() == 1):
            return(rslt[0])
        else:
            return(rslt)
    def dlist(self):
        '''
            x = [('k1','v1'),('k2','v2'),('k3','v3'),('k4','v4'),('k5','v5'),('k6','v6')]
            tl = Tlist(x)
            dl = tl.dlist()
            pobj(dl)
        '''
        dl = tlist2dlist(self.tl)
        return(dl)
    def comprise(self,tl2,**kwargs):
        '''
            x1 = [('k1','v1'),('k2','v2'),('k3','v3'),('k4','v4'),('k5','v5'),('k6','v6')]
            tl1 = Tlist(x1)
            x2 = [('k1','v1'),('k2','v2'),('k3','v3'),('k4','v4')]
            tl2 = Tlist(x2)
            tl1.comprise(tl2,mode='strict')
            
            x1 = [('k1','v1'),('k2','v2'),('k3','v3'),('k4','v4'),('k5','v5'),('k6','v6')]
            tl1 = Tlist(x1)
            x2 = [('k2','v2'),('k3','v3'),('k4','v4')]
            tl2 = Tlist(x2)
            tl1.comprise(tl2,mode='strict')
            tl1.comprise(tl2,mode='middle')
            
            
            x1 = [('k1','v1'),('k2','v2'),('k3','v3'),('k4','v4'),('k5','v5'),('k6','v6')]
            tl1 = Tlist(x1)
            x2 = [('k3','v3'),('k4','v4'),('k2','v2')]
            tl2 = Tlist(x2)
            
            tl1.comprise(tl2,mode='middle')
            tl1.comprise(tl2,mode='loose')
        '''
        return(_comprise(self.tl,tl2.tl,**kwargs))
    def sort(self,**kwargs):
        '''
            x = [('k2','v1'),('k1','v2'),('k4','v3'),('k3','v4')]
            tl = Tlist(x)
            tl.sort()
            tl
            
            x = [('k2','v1'),('k1','v2'),('k4','v3'),('k3','v4')]
            tl = Tlist(x)
            tl.sort(mode='key')
            tl
            
            x = [('k2','v1'),('k1','v2'),('k4','v3'),('k3','v4')]
            tl = Tlist(x)
            tl.sort(mode='value')
            tl
            
            #first compare key, then compare value
            x = [('k2','v1'),('k1','v2'),('k2','v3'),('k1','v4')]
            tl = Tlist(x)
            tl.sort(mode='kv')
            tl
            
            #first compare value, then compare key
            x = [('k2','v1'),('k1','v4'),('k2','v1'),('k1','v4')]
            tl = Tlist(x)
            tl.sort(mode='vk')
            tl
        '''
        self.tl = _sort(self.tl,**kwargs)
        return(self.tl)
    def reverse(self,**kwargs):
        '''
            x = [('k1','v1'),('k2','v2'),('k3','v3'),('k4','v4')]
            tl = Tlist(x)
            tl.reverse()
            tl
        '''
        self.tl = _reverse(self.tl)
    def remove_all(self,**kwargs):
        '''
            x = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k3','v3'),('k2','v24'),('k4','v4')]
            tl = Tlist(x)
            tl.remove_all(key='k2')
            tl
            
            x = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k3','v3'),('k2','v24'),('k4','v4')]
            tl = Tlist(x)
            tl.remove_all(value='v3')
            tl
            
            x = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k3','v3'),('k2','v24'),('k4','v4')]
            tl = Tlist(x)
            tl.remove_all(kv=('k4','v4'))
            tl
            
            x = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k3','v3'),('k2','v24'),('k4','v4')]
            tl = Tlist(x)
            tl.remove_all(kv=('k1','v1'))
            tl
        '''
        self.tl = _remove_all(self.tl,**kwargs)
    def remove_last(self,**kwargs):
        '''
            x = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k3','v3'),('k2','v24'),('k4','v4')]
            tl = Tlist(x)
            tl.remove_last(key='k2')
            tl
            
            x = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k3','v3'),('k2','v24'),('k4','v4')]
            tl = Tlist(x)
            tl.remove_last(value='v3')
            tl
            
            x = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k3','v3'),('k2','v24'),('k4','v4')]
            tl = Tlist(x)
            tl.remove_last(kv=('k4','v4'))
            tl
            
            
            x = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k3','v3'),('k2','v24'),('k4','v4')]
            tl = Tlist(x)
            tl.remove_last(kv=('k1','v1'))
            tl
        '''
        self.tl = _remove_last(self.tl,**kwargs)
    def remove_first(self,**kwargs):
        '''
            x = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k3','v3'),('k2','v24'),('k4','v4')]
            tl = Tlist(x)
            tl.remove_first(key='k2')
            tl
            
            x = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k3','v3'),('k2','v24'),('k4','v4')]
            tl = Tlist(x)
            tl.remove_first(value='v3')
            tl
            
            x = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k3','v3'),('k2','v24'),('k4','v4')]
            tl = Tlist(x)
            tl.remove_first(kv=('k4','v4'))
            tl
            
            x = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k3','v3'),('k2','v24'),('k4','v4')]
            tl = Tlist(x)
            tl.remove_first(kv=('k1','v1'))
            tl
        '''
        self.tl = _remove_first(self.tl,**kwargs)
    def remove_which(self,which,**kwargs):
        self.tl = _remove_which(self.tl,which,**kwargs)
    #########################
    #########################
    def pop_seqs(self,seqs,**kwargs):
        '''
            x = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k3','v3'),('k2','v24'),('k4','v4')]
            tl = Tlist(x)
            tl.pop_seqs({0,2},key='k2')
            tl
            
            x = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k3','v3'),('k2','v24'),('k4','v4')]
            tl = Tlist(x)
            tl.pop_seqs({1,3},key='k2')
            tl
            
            x = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k3','v3'),('k2','v24'),('k4','v4')]
            tl = Tlist(x)
            tl.pop_seqs({1,4})
            tl
            
            
            x = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k3','v3'),('k2','v24'),('k4','v4')]
            tl = Tlist(x)
            tl.pop_seqs({3,5})
            tl
        '''
        return(_pop_seqs(self.tl,seqs,**kwargs))
    def pop_range(self,start,end,**kwargs):
        '''
            x = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k3','v3'),('k2','v24'),('k4','v4')]
            tl = Tlist(x)
            tl.pop_range(0,2,key='k2')
            tl
            
            x = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k3','v3'),('k2','v24'),('k4','v4')]
            tl = Tlist(x)
            tl.pop_range(1,4,key='k2')
            tl
            
            x = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k3','v3'),('k2','v24'),('k4','v4')]
            tl = Tlist(x)
            tl.pop_range(1,4)
            tl
            
            x = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k3','v3'),('k2','v24'),('k4','v4')]
            tl = Tlist(x)
            tl.pop_range(3,5)
            tl
        '''
        return(_pop_range(self.tl,start,end,**kwargs))
    def pop_all(self,*args,**kwargs):
        '''
            x = [('k1','v1'),('k2','v21'),('k2','v22'),('k31','v3'),('k3','v3'),('k4','v4'),('k4','v4')]
            tl = Tlist(x)
            tl.pop_all(key='k2')
            tl
            
            x = [('k1','v1'),('k2','v21'),('k2','v22'),('k31','v3'),('k3','v3'),('k4','v4'),('k4','v4')]
            tl = Tlist(x)
            tl.pop_all(1)
            tl
            
            x = [('k1','v1'),('k2','v21'),('k2','v22'),('k31','v3'),('k3','v3'),('k4','v4'),('k4','v4')]
            tl = Tlist(x)
            tl.pop_all(3)
            tl
        '''
        return(_pop_all(self.tl,*args,**kwargs))
    def count(self,**kwargs):
        '''
            x = [('k1','v1'),('k2','v21'),('k2','v22'),('k31','v3'),('k3','v3'),('k4','v4'),('k4','v4')]
            tl = Tlist(x)
            tl.count(key='k2')
            tl.count(value='v3')
            tl.count(kv=('k2','v2'))
            tl.count(kv=('k4','v4'))
        '''
        return(_count(self.tl,**kwargs))
    def includes(self,**kwargs):
        '''
            x = [('k1','v1'),('k2','v2'),('k3','v3'),('k4','v4')]
            tl = Tlist(x)
            tl.includes(key='k2')
            tl.includes(value='v3')
            tl.includes(kv=('k2','v3'))
            tl.includes(kv=('k2','v2'))
            tl.includes(kv=('k4','v4'))
        '''
        return(_includes(self.tl,**kwargs))
    def insert_sec(self,index,tl2,**kwargs):
        '''
            x = [("k1","v1"),("k2","v2"),("k3","v3")]
            tl1 = Tlist(x)
            x = [("k4","v4"),("k5","v5"),("k6","v6")]
            tl2 = Tlist(x)
            insert_sec(tl1,0,tl2)
            insert_sec(tl1,1,tl2)
            insert_sec(tl1,2,tl2)
            insert_sec(tl1,3,tl2)
        '''  
        return(_insert_sec(self.tl,index,tl2.tl,**kwargs))
    def insert(self,index,*args,**kwargs):
        '''
            x = [('k1','v1'),('k2','v2'),('k3','v3'),('k4','v4')]
            tl = Tlist(x)
            tl
            tl.insert(0,'k6','v6')
            tl
            
            x = [('k1','v1'),('k2','v2'),('k3','v3'),('k4','v4')]
            tl = Tlist(x)
            tl.insert(1,('k6','v6'))
            tl
            
            x = [('k1','v1'),('k2','v2'),('k3','v3'),('k4','v4')]
            tl = Tlist(x)
            tl.insert(2,'k6','v6')
            tl
            
            x = [('k1','v1'),('k2','v2'),('k3','v3'),('k4','v4')]
            tl = Tlist(x)
            tl.insert(3,('k6','v6'))
            tl
            
            x = [('k1','v1'),('k2','v2'),('k3','v3'),('k4','v4')]
            tl = Tlist(x)
            tl.insert(4,'k6','v6',deepcopy=True)
            tl
        '''    
        if('deepcopy' in kwargs):
            pass
        else:
            kwargs['deepcopy'] = False
        return(_insert(self.tl,index,*args,**kwargs))
    def deepcopy(self,**kwargs):
        return(copy.deepcopy(self))
    def clear(self,**kwargs):
        self.tl.clear()
        return(self)
    def prepend(self,*args,**kwargs):
        '''
            x = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k31','v3'),('k32','v3'),('k33','v3'),('k2','v24'),('k2','v24'),('k5','v5')]
            tl = Tlist(x)
            tl
            tl.prepend('k6','v6')
            tl
            tl.prepend(('k6','v6'))
            tl
        '''
        if('deepcopy' in kwargs):
            pass
        else:
            kwargs['deepcopy'] = False
        self.tl = _prepend(self.tl,*args,**kwargs)
    def append(self,*args,**kwargs):
        '''
            x = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k31','v3'),('k32','v3'),('k33','v3'),('k2','v24'),('k2','v24'),('k5','v5')]
            tl = Tlist(x)
            tl
            tl.append('k6','v6')
            tl
            tl.append(('k6','v6'))
            tl
        '''
        if('deepcopy' in kwargs):
            pass
        else:
            kwargs['deepcopy'] = False
        self.tl = _append(self.tl,*args,**kwargs)
    def index_last(self,**kwargs):
        '''
            x = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k31','v3'),('k32','v3'),('k33','v3'),('k2','v24'),('k2','v24'),('k5','v5')]
            tl = Tlist(x)
            tl.index_last(tl,value = 'v3')
            tl.index_last(tl,key = 'k2')
            tl.index_last(tl,kv = ('k4','v4'))
            tl.index_last(tl,kv = ('k5','v5'))
        '''
        return(_index_last(tl.tl,**kwargs))
    def index_first(self,**kwargs):
        '''
            x = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k31','v3'),('k32','v3'),('k33','v3'),('k2','v24'),('k2','v24'),('k5','v5')]
            tl = Tlist(x)
            tl.index_first(value = 'v3')
            tl.index_first(key = 'k2')
            tl.index_first(kv = ('k4','v4'))
            tl.index_first(kv = ('k5','v5'))
        '''
        return(_index_first(tl.tl,**kwargs))
    def indexes_all(self,**kwargs):
        '''
            x = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k31','v3'),('k32','v3'),('k33','v3'),('k2','v24'),('k2','v24'),('k5','v5')]
            tl = Tlist(x)
            tl.indexes_all(value = 'v3')
            tl.indexes_all(key = 'k2')
            tl.indexes_all(kv = ('k4','v4'))
            tl.indexes_all(kv = ('k5','v5'))
        '''
        return(_indexes_all(tl.tl,**kwargs))
    def all_continuous(self,**kwargs):
        '''
            x = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k31','v3'),('k32','v3'),('k33','v3'),('k2','v24'),('k2','v24'),('k5','v5')]
            tl = Tlist(x)
            tl.all_continuous(key='k2')
            tl.all_continuous(value='v3')
            tl.all_continuous(kv=('k4','v4'))
            
        '''
        return(all_continuous_indexes_slices(self.tl,**kwargs))
    def last_continuous(self,**kwargs):
        '''
            x = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k31','v3'),('k32','v3'),('k33','v3'),('k2','v24'),('k2','v24'),('k5','v5')]
            tl = Tlist(x)
            tl.last_continuous(key='k2')
            tl.last_continuous(value='v3')
            tl.last_continuous(kv=('k4','v4'))
        '''
        return(last_continuous_indexes_slice(self.tl,**kwargs))
    def first_continuous(self,**kwargs):
        '''
            x = [('k1','v1'),('k2','v21'),('k2','v22'),('k2','v23'),('k31','v3'),('k32','v3'),('k33','v3'),('k4','v4'),('k4','v4'),('k5','v5')]
            tl = Tlist(x)
            tl.first_continuous(key='k2')
            tl.first_continuous(value='v3')
            tl.first_continuous(kv=('k4','v4'))
        '''
        return(first_continuous_indexes_slice(self.tl,**kwargs))
    def extend(self,tl2,**kwargs):
        '''
            x = [('k1', 'v1'), ('k2', 'v2'), ('k3', 'v3')]
            tl1 = Tlist(x)
            x = [('k4', 'v4'), ('k5', 'v5'), ('k6', 'v6')]
            tl2 = Tlist(x)
            tl1.extend(tl2)
            tl1
            tl2
        '''
        self.tl = _extend(self.tl,tl2.tl,**kwargs)
    def prextend(self,tl2,**kwargs):
        '''
            x = [('k1', 'v1'), ('k2', 'v2'), ('k3', 'v3')]
            tl1 = Tlist(x)
            x = [('k4', 'v4'), ('k5', 'v5'), ('k6', 'v6')]
            tl2 = Tlist(x)
            tl1.prextend(tl2)
            tl1
            tl2
        '''
        self.tl = _prextend(self.tl,tl2.tl,**kwargs)
    def kvlists(self,**kwargs):
        '''
            x = [('k1', 'v1'), ('k2', 'v2'), ('k3', 'v3')]
            tl = Tlist(x)
            kl,vl = tl.kvlists()
            kl
            vl 
        '''
        return(tl2kvlists(self.tl,**kwargs))       
    def uniqualize_all(self,**kwargs):
        self.tl = uniqualize_all(self.tl,**kwargs)
    def uniqualize(self,*args,**kwargs):
        self.tl = uniqualize(self.tl,*args,**kwargs) 

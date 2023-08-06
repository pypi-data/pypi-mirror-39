# -*- coding:utf-8 -*-
# writer: Mia at 16. 9. 9, 
# last revision: 오후 11:24

def read_file(f):
    with open(f,'r') as rf:
        return rf.read()


def read_file_utf8(f):
    from codecs import open as copen
    with copen(f, 'r','utf-8') as rf:
        return rf.read()

def read_file_kr(f):
    from codecs import open as copen
    with copen(f, 'r','euc-kr') as rf:
        return rf.read()

def read_pf(f):
    import pickle
    with open(f,'rb') as pf:
        return pickle.load(pf)


def write_file(f,String_obj):
    with open(f,'w') as wf:
        wf.write(String_obj)


def write_file_utf8(f,obj):
    from codecs import open as copen
    with copen(f,'w','utf-8') as wf:
        wf.write(obj)

def write_pf(f,obj):
    import pickle
    with open(f,'wb') as pf:
        pickle.dump(obj,pf)
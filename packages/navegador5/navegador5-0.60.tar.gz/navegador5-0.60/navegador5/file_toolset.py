from navegador5 import shell_cmd
import os
import json
import chardet
import csv
from xdict import utils
import re

def convert_code(to_codec="UTF8",**kwargs):
    fd = open(kwargs['fn'],"rb+")
    rslt = fd.read()
    fd.close()
    from_codec = chardet.detect(rslt)['encoding']
    rslt = rslt.decode(from_codec).encode(to_codec)
    os.remove(kwargs['fn'])
    fd = open(kwargs['fn'],"wb+")
    fd.write(rslt)
    fd.close()


def write_to_file(**kwargs):
    fd = open(kwargs['fn'],kwargs['op'])
    fd.write(kwargs['content'])
    fd.close()
    
def write_json(**kwargs):
    content = json.dumps(kwargs['json'])
    kwargs['content'] = content
    write_to_file(**kwargs)

def read_file_content(**kwargs):
    fd = open(kwargs['fn'],kwargs['op'])
    rslt = fd.read()
    fd.close()
    return(rslt)

def readfile(fn):
    fd = open(fn,'r+')
    rslt = fd.read()
    fd.close()
    return(rslt)




def read_json(**kwargs):
    rslt = read_file_content(**kwargs)
    js = json.loads(rslt)
    return(js)


def read_json_rplus(fn):
    fd = open(fn,'r+')
    raw = fd.read()
    fd.close()
    d = json.loads(raw)
    return(d)


def write_json_wplus(fn,js):
    fd = open(fn,'w+')
    s = json.dumps(js)
    fd.write(s)
    fd.close()


def file_replace_string(src,dst,**kwargs):
    if('rop' in kwargs):
        rop = kwargs['rop']
    else:
        rop = 'r+'
    if('wop' in kwargs):
        wop = kwargs['wop']
    else:
        wop = 'w+'
    kwargs['op'] = kwargs['rop']
    rslt = read_file_content(**kwargs)
    if('count' in kwargs):
        count = kwargs['count']
    else:
        count = 0
    if('flags' in kwargs):
        flags = kwargs['flags']
    else:
        flags = 0
    if(xdict.utils.is_regex(src)):
        #re.sub(pattern, repl, string, count=0, flags=0)
        rslt = re.sub(src,dst,rslt,count,flags) 
    else:
        rslt = rslt.replace(src,dst)
    if('inplace' in kwargs):
        inplace = True
    else:
        inplace = False
        ncp = kwargs['copyto']
    kwargs['op'] = kwargs['wop']
    write_to_file(**kwargs)


####
def write2csv(**kwargs):
    if('op' in kwargs):
        op = kwargs['op']
    else:
        op = 'w+'
    csvarr = kwargs['csvarr']
    fd = open(kwargs['fn'],op)
    writer = csv.writer(fd)
    writer.writerows(csvarr)
    fd.close()


def detect_file(fn):
    fd = open(fn,'rb+')
    byts = fd.read()
    fd.close()
    encd = chardet.detect(byts)['encoding']
    return(encd)
        

def readcsv(**kwargs):
    if('op' in kwargs):
        op = kwargs['op']
    else:
        op = 'r+'
    encd = detect_file(kwargs['fn'])
    fd = open(kwargs['fn'],op,encoding=encd)
    reader = csv.reader(fd)
    csvarr = []
    for row in reader:
        csvarr.append(row)
    fd.close()
    return(csvarr)

####


def prepend_to_file(prepend,**kwargs):
    prepend=bytes(prepend)
    fd = open(kwargs['fn'],"rb+")
    rslt = fd.read()
    fd.close()
    os.remove(kwargs['fn'])
    fd = open(kwargs['fn'],"wb+")
    fd.write(prepend+rslt)
    fd.close()


#mkdir
def mkdir(path,force=False):
    if(os.path.exists(path)):
        if(force):
            shell_cmd.pipe_shell_cmds({1:'rm -r '+path})
        else:
            pass
    else:
        os.makedirs(path)

#find all files recursively
def walkall_files(dirpath=os.getcwd()):
    fps = []
    for (root,subdirs,files) in os.walk(dirpath):
        for fn in files:
            path = os.path.join(root,fn)
            fps.append(path)
    return(fps)

#def file_recursive_rename

#find all subdirs recursively




#替换父目录的名字，祖父以上层级目录不变
def new_leaf_path(p,suffix):
    '''
    '''
    basename = os.path.basename(p)
    olp = os.path.dirname(p)
    nlp = os.path.basename(olp)+'_'+suffix
    pp = os.path.dirname(olp)
    np = pp+'/'+nlp
    os.makedirs(np)
    np = np +'/'+basename
    return(np)

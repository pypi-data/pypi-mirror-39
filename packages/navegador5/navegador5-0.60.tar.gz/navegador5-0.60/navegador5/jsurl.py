#https://www.cnblogs.com/shuiyi/p/5277233.html


import elist.elist as elel


URI_RESERVED = [';','/','?',':','@','&','=','+','$',',']
URI_UNESCAPED = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z','0','1','2','3','4','5','6','7','8','9','-','_','.','!','~','*',"'",'(',')']
POUND=['#']

def is_type1(c):
    cond = (c in URI_RESERVED)
    return(cond)

def is_type2(c):
    cond = (c in URI_UNESCAPED)
    return(cond)

def is_type3(c):
    cond = (c in POUND)
    return(cond)

def is_type4(c):
    cond1 = (c in URI_RESERVED)
    cond2 = (c in URI_UNESCAPED)
    cond3 = (c in POUND)
    cond = not( cond1 | cond2 | cond3)
    return(cond)


#TYPE51 = URI_RESERVED + URI_UNESCAPED + POUND
#TYPE51 = elel.array_map(TYPE51,quote_ch)i

TYPE51 = ['%3B', '%2F', '%3F', '%3A', '%40', '%26', '%3D', '%2B', '%24', '%2C', '%61', '%62', '%63', '%64', '%65', '%66', '%67', '%68', '%69', '%6A', '%6B', '%6C', '%6D', '%6E', '%6F', '%70', '%71', '%72', '%73', '%74', '%75', '%76', '%77', '%78', '%79', '%7A', '%41', '%42', '%43', '%44', '%45', '%46', '%47', '%48', '%49', '%4A', '%4B', '%4C', '%4D', '%4E', '%4F', '%50', '%51', '%52', '%53', '%54', '%55', '%56', '%57', '%58', '%59', '%5A', '%30', '%31', '%32', '%33', '%34', '%35', '%36', '%37', '%38', '%39', '%2D', '%5F', '%2E', '%21', '%7E', '%2A', '%27', '%28', '%29', '%23']


#TYPE52 = 




def quote_ch(c):
    es = hex(ord(c))[2:].upper()
    es = '0'+es
    es = '%'+es[-2:]
    return(es)

def unquote_ch(es):
    h = es.replace('%','0x')
    o = int(h,16)
    c = chr(o)
    return(c)

def encodeURI(s):
    rslt =''
    lngth = s.__len__()
    for i in range(0,lngth):
        c = s[i]
        cond = is_type4(c)
        if(cond):
            es = quote_ch(c)
        else:
            es = c
        rslt = rslt + es
    return(es)


def encodeURIComponent(s):
    rslt =''
    lngth = s.__len__()
    for i in range(0,lngth):
        c = s[i]
        cond1 = is_type1(c)
        cond3 = is_type3(c)
        cond4 = is_type4(c)
        cond = (cond1 | cond3 | cond4)
        if(cond):
            es = quote_ch(c)
        else:
            es = c
        rslt = rslt + es
    return(es)

 ###################



def URIstr2arr(s):
    arr = []
    lngth = s.__len__()
    i = 0
    while(i<lngth):
        c = s[i]
        if(c == '%'):
            arr.append(s[i:(i+3)])
            i = i + 3
        else:
            arr.append(c)
            i = i + 1
    return(arr)


def is_type51(es):
    cond = (es in TYPE51)
    return(cond)


def is_type52(es):
    c = unquote_ch(es)
    if(is_type4(c)):
        return(True)
    else:
        return(False)
    



def decodeURI(es):
    arr = URIstr2arr(es)
    lngth = arr.__len__()
    for i in range(0,lngth):
        e = arr[i]
        if('%' == e[0]):
            cond = is_type52(e)
            if(cond):
                arr[i] =  unquote_ch(e)
            else:
                pass
        else:
            pass
    s = elel.join(arr,'')
    return(s)


def decodeUTIComponent(es):
    arr = URIstr2arr(es)
    lngth = arr.__len__()
    for i in range(0,lngth):
        e = arr[i]
        if('%' == e[0]):
            cond1 = is_type52(e)
            cond2 = is_type51(e)
            cond = (cond1 | cond2)
            if(cond):
                arr[i] =  unquote_ch(e)
            else:
                pass
        else:
            pass
    s = elel.join(arr,'')
    return(s)


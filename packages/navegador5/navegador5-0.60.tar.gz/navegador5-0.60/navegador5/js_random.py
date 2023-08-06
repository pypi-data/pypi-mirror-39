import math
import random
import time

def js_clock_seconds(accuracy):
    accuracy = int(accuracy) - 1
    now = str(time.time())
    now = now.replace('.','')
    now = now[0:accuracy]
    return(int(now))

def jsRandomCalculator_f3(v1, v2, email):
    email_len = email.__len__()
    v3 = 0
    for i in range(0,email_len):
        char_code = ord(email[i])
        shift = (5 * i) % 32
        offset = char_code << shift
        offset = offset % (2**32)
        if(offset > 0x7fffffff):
            offset = offset - 2 **32
        else:
            offset = offset
        v3 = v3 + offset
    rslt = (v1 * v2 * v3) % 1000000007
    return(rslt)

def jsRandomCalculator_f2(vs, ts):
    sum = vs[0] + vs[1]
    n = sum % 3000
    m = sum % 10000
    p = ts % 10000
    if(n < 1000):
        return(((m + 12345)**2) + ((p + 34567)** 2))
    elif(n < 2000):
        return(((m + 23456)**2) + ((p + 23456)** 2))
    else:
        return(((m + 34567)**2) + ((p + 12345)** 2))

def jsRandomCalculator_f1(vs, ts):
    output = []
    output.append(vs[0] + vs[1] + vs[2])
    output.append((vs[0] % 100 + 30) * (vs[1] % 100 + 30) * (vs[2] % 100 + 30))
    for i in range(0,10):
        output[0] += (output[1] % 1000 + 500) * (ts % 1000 + 500)
        output[1] += (output[0] % 1000 + 500) * (ts % 1000 + 500)
    return(output)

def jsRandomCalculator_compute(n, email, ts):
    try:
        vs = n.split(":")
        ts = int(ts)
        vs_len = vs.__len__()
        for i in range(0,vs_len):
            vs[i] = int(vs[i], 10)
        f1_out = jsRandomCalculator_f1(vs, ts)
        f2_out = jsRandomCalculator_f2(f1_out, ts)
        if(f1_out[0] % 1000 > f1_out[1] % 1000):
            v = f1_out[0]
        else:
            v = f1_out[1]
        return(jsRandomCalculator_f3(v, f2_out, email))
    except Exception as err:
        return(-1)

def gen_client_n():
    b = []
    for c in range(0,3):
        temp = math.floor(9*(10**8) * random.random()) + 10**8
        b.append(str(temp)) 
    rslt = ':'.join((b[0],b[1],b[2]))
    return(rslt)

def gen_no_cache_url(url):
    try:
        q = url.index("?")
    except Exception as err:
        print(err)
        url = ''.join((url,"?"))
    else:
        url = ''.join((url,"&"))
    url = ''.join((url+ "_" + str(js_clock_seconds(13))))
    return(url)

def crypt_JS_mc(num):
    ret=""
    b="0123456789ABCDEF"
    if(num==ord(' ')):
        ret="+"
    elif((num<ord('0')  and num!=ord('-') and num!=ord('.'))|(num<ord('A') and num>ord('9'))|(num>ord('Z') and num<ord('a') and num!=ord('_'))|(num>ord('z'))):
        ret = "%"
        ret = ''.join((ret,b[num // 16]))
        ret = ''.join((ret,b[num % 16]))
    else:
        ret=chr(num)
    return(ret)
    
def crypt_JS_m(num):
    return(((num&1)<<7)|((num&(0x2))<<5)|((num&(0x4))<<3)|((num&(0x8))<<1)|((num&(0x10))>>1)|((num&(0x20))>>3)|((num&(0x40))>>5)|((num&(0x80))>>7))

def crypt_JS_md6_encode(clear_Text_Passwd):
    encryed_Passwd = "";
    c = 0xbb;
    for i in range(0,clear_Text_Passwd.__len__()):
        c = crypt_JS_m(ord(clear_Text_Passwd[i]))^(0x35^(i&0xff));
        encryed_Passwd = ''.join((encryed_Passwd,crypt_JS_mc(c)))
    return(encryed_Passwd)
        
        
def decrypt_JS_mc(old_Urlquote):
    if(old_Urlquote == '+'):
        return(' ')
    else:
        regex_JS_mc = re.compile('%(.*)')
        m = regex_JS_mc.search(old_Urlquote)
        if(m == None):
            return(ord(old_Urlquote))
        else:
            return(int(old_Urlquote.lstrip('%'),16))

def split_Encrypt_String(encrypted_Passwd):
    len = encrypted_Passwd.__len__()
    cursor = 0
    encry_Dict = {}
    count = 0
    temp = ''
    seq = 1
    while(cursor < len):
        if(encrypted_Passwd[cursor]=='%'):
            temp = encrypted_Passwd[cursor+1:cursor+3]
            encry_Dict[seq] = temp
            cursor = cursor + 3
            temp = ''
        else:
            temp = encrypted_Passwd[cursor]
            encry_Dict[seq] = temp
            cursor = cursor + 1
            temp = ''
        seq = seq + 1
    return(encry_Dict)
        
def crypt_JS_md6_decode(encrypted_Passwd):
    clear_Text_Passwd = ""
    encry_Dict = split_Encrypt_String(encrypted_Passwd)
    len = encry_Dict.__len__()
    for i in range(1,len+1):
        ele_Len = encry_Dict[i].__len__()
        if(ele_Len==2):
            num = int(encry_Dict[i],16)
        else:
            num = ord(encry_Dict[i])
        seq = i - 1
        temp_C = num ^ (0x35^(seq&0xff))
        orig_C = crypt_JS_m(temp_C)
        char = chr(orig_C)
        clear_Text_Passwd = ''.join((clear_Text_Passwd,char))
    return(clear_Text_Passwd)

#############################################
#UA random

def ums1():
    a = int(nvjq.jQuery_unix_now())
    b = random.randrange(200,1500)
    s1 = xjs.toString(a,16) + xjs.toString(b,16)
    return(s1)

def umsig_internal(a,b,h):
    c = 0
    d = 0
    for c in range(0,b.__len__()):
        d = d | (h[c] << (8*c))
    return(a^d)

def umsig(ua):
    k = 0
    h = []
    for i in range(0,ua.__len__()):
        g = eses.charCodeAt(ua,i)
        h = xjs.unshift(h,g&255)
        if(h.__len__()>=4):
            k = umsig1(k,h,h)
            h = []
        else:
            pass
    if(h.__len__()>0):
        k = umsig_internal(k,h,h)
    else:
        pass
    return(xjs.toString(k,16))

def get_um_cookie(ua):
    '''
        UM_distinctid=163beafb1ae4c-0ab6ca85f87c84-4c312b7b-100200-163beafb1af26
    '''
    screen_height = 768
    screen_width = 1366
    c = xjs.toString(screen_height*screen_width,16)
    rslt = ums1() + "-" 
    rslt = rslt + xjs.toString(int(str(random.random()).replace("0.","")),16)
    rslt = rslt + "-" + umsig(ua) + "-" + c + "-" + ums1()
    return(rslt)



############################################

import random
import time
import datetime
import re

def jQuery_random_number(bits_num = 17,result_format='str'):
    r = random.random();
    r_str = r.__str__().replace(".","")
    if(r_str.__len__()<=bits_num):
        padding = '0' * (bits_num - r_str.__len__())
        r_str = ''.join((r_str,padding))
    else:
        r_str = r_str[:bits_num]
    if(result_format=='str'):
        return(r_str)
    else:
        return(int(r_str))

def jQuery_expando(jquery_version_string='1.8.1'):
    r_str = jQuery_random_number();
    expando = ''.join(("jQuery",jquery_version_string,r_str))
    return(expando.replace(".",""))


def jQuery_unix_now(bits_num = 13,result_format='str'):
    now = time.time();
    unix_now_str = now.__str__().replace(".","")
    if(unix_now_str.__len__()<=bits_num):
        padding = '0' * (bits_num - unix_now_str.__len__())
        unix_now_str = ''.join((unix_now_str,padding))
    else:
        unix_now_str = unix_now_str[:bits_num]
    if(result_format=='str'):
        return(unix_now_str)
    else:
        return(int(unix_now_str))

def jQuery_get_random_jsonpCallback_name(expando=jQuery_expando()):
    unix_now = jQuery_unix_now()
    jsonpCallback_name = ''.join((expando,"_",unix_now))
    return(jsonpCallback_name)

def jQuery_get_jsonp_reply_arguments(resp_body,callback):
    if(isinstance(resp_body,bytes)):
        arguments = resp_body.decode()[:-1]
    elif(isinstance(resp_body,str)):
        arguments = resp_body[:-1]
    else:
        arguments = resp_body.__str__()
    arguments = arguments.replace(callback,"")
    arguments = arguments.lstrip("(").lstrip("'").lstrip('"')
    arguments = arguments.rstrip(")").rstrip("'").rstrip('"')
    return(arguments)

def jQuery_get_utcOffset(unit="min",result_format='str'):
    '''var t_utcOffset = function() {
        return (-(new Date).getTimezoneOffset()).toString()
    }'''
    ts = time.time()
    utc_now = datetime.datetime.utcfromtimestamp(ts)
    now = datetime.datetime.fromtimestamp(ts)
    utcOffset = now.timestamp() - utc_now.timestamp()
    if(unit=="seconds"):
        utcOffset = int(utcOffset)
    elif(unit=="min"):
        utcOffset = int(utcOffset/60)
    else:
        utcOffset = int(utcOffset/3600)
    if(result_format=='str'):
        return(utcOffset.__str__())
    else:
        return(utcOffset)

def jQuery_get_jsonp_params(ic):
    regex = re.compile('\[.*\]')
    txt = ic['resp_body_text']
    m = regex.search(txt)
    arr = json.loads(m.group(0))
    return(arr)



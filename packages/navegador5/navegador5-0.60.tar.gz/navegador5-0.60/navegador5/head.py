import operator
import re
from navegador5 import url_tool
from navegador5 import time_utils


#
HEAD_POOL = [
    '''User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2\r\nAccept-Encoding: gzip, deflate, br''',
    '''Accept: text/html, application/xhtml+xml, */*\r\nAccept-Language: zh-Hans-CN,zh-Hans;q=0.8,es-ES;q=0.7,es;q=0.5,en-IE;q=0.3,en;q=0.2\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393\r\nAccept-Encoding: gzip, deflate''',
    '''Accept: text/html, application/xhtml+xml, */*;q=0.5\r\nAccept-Language: zh-Hans-CN,zh-Hans;q=0.8,es-ES;q=0.7,es;q=0.5,en-IE;q=0.3,en;q=0.2\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko\r\nAccept-Encoding: gzip, deflate'''
]




#query post body
post_querydict_to_querystr = url_tool.urlencode
post_querystr_to_querydict = url_tool.urldecode




#resp 
#resp_head = resp.getheaders()  tuple_list
#resp_body_bytes = resp.read()

def split_one_header_str_to_tuple(header_String):
    regex_Header_String = re.compile('(.*?): (.*)')
    m = regex_Header_String.search(header_String)
    return((m.group(1),m.group(2)))

def split_http_headers_and_body(http_all):
    rslt = {'headers':'','body':''}
    arrs_rn = http_all.split('\r\n\r\n')
    arrs = http_all.split('\r\n')     
    if(arrs_rn.__len__()>1):
        rslt['headers'] = arrs_rn[0]
        rslt['body'] = arrs_rn[1]
        for i in range(1,arrs_rn.__len__()):
            rslt['body'] = ''.join((rslt['body'],arrs_rn[i],'\r\n\r\n'))
        rslt['body'] = rslt['body'].rstrip('\n')
        rslt['body'] = rslt['body'].rstrip('\r')
        rslt['body'] = rslt['body'].rstrip('\n')
        rslt['body'] = rslt['body'].rstrip('\r')
    else:
        regex_rstrip_one = re.compile('(.*)\r\n')
        regex_colon = re.compile('^[A-Z][a-zA-Z\-]+: ')
        label = -1
        for i in range(0,arrs.__len__()):
            if(regex_colon.search(arrs[i])):
                pass
            else:
                label = i
                break
        rslt['headers'] = ''
        rslt['body'] = ''
        for i in range(0,label):
            rslt['headers'] = ''.join((rslt['headers'],arrs[i],'\r\n'))
        rslt['headers'] = rslt['headers'].rstrip('\n')
        rslt['headers'] = rslt['headers'].rstrip('\r')
        for i in range(label,arrs.__len__()):
            rslt['body'] = ''.join((rslt['body'],arrs[i],'\r\n'))
        rslt['body'] = rslt['body'].rstrip('\n')
        rslt['body'] = rslt['body'].rstrip('\r')
        if(label == -1):
            rslt['headers'] = http_all
            rslt['body'] = None
    return(rslt)

def concat_http_headers_and_body(headers_dict,body_text):
    head_text = encode_http_headers(headers_dict)
    sp = '\r\n\r\n'
    rslt = ''.join((head_text,sp,body_text))
    return(rslt)

def decode_one_http_head(head_name,splitor,body_text,ordered=1):
    s_rep = ''.join((splitor,' '))
    body_text = body_text.replace(s_rep,splitor)
    #use ordered as possible as you can 
    regex = re.compile(''.join((head_name,': ')))
    m = regex.search(body_text)
    if(m):
        len = ''.join((head_name,': ')).__len__()
        body_text = body_text[len:]
    else:
        pass
    regex_colon = re.compile('^([A-Z][a-zA-Z\-]+): ')
    m = regex_colon.search(body_text)
    if(m):
        head_name = m.group(1)
        len = ''.join((head_name,': ')).__len__()
        body_text = body_text[len:]
    else:
        pass
    rslt = {}
    arrs = body_text.split(splitor)
    for i in range(0,arrs.__len__()):
        each = arrs[i]
        regex = re.compile('(.*?)=(.*)')
        m = regex.search(each)
        if(m):
            kv = [m.group(1),m.group(2)]
        else:
            kv = [each]
        key =kv[0]
        if(kv.__len__()==1):
            value = None
            if(ordered):
                rslt['name'] = head_name
                rslt[i] = ('',key)
            else:
                rslt[' '] = head_name
                rslt[''] = key
        else:
            value = kv[1]
            if(ordered):
                rslt['name'] = head_name 
                rslt[i] = (key,value)
            else:
                rslt[' '] = head_name
                rslt[key] = value
    return(rslt)

def encode_one_http_head(body_dict,head_name,splitor,include_head=0):
    body = ''
    if(include_head):
        rslt = ''.join((head_name,': '))
    else:
        rslt = ''
    ordered = 0
    for key in body_dict:
        if(type(body_dict[key]) == type(())):
            ordered = 1
            break
    if(ordered):
        for key in body_dict:
            if(type(key)==type(0)):
                kv = body_dict[key]
                k = kv[0]
                v = kv[1]
                if(k==''):
                    body = ''.join((body,splitor,v))
                else:
                    body = ''.join((body,splitor,k,'=',v))
    else:
        for key in body_dict:
            if(type(key)==type(0)):
                k = key
                v = body_dict[key]
                if(k==''):
                    body = ''.join((body,splitor,v))
                else:
                    body = ''.join((body,splitor,k,'=',v))
    len = splitor.__len__()                
    body = body[len:]
    rslt = ''.join((rslt,body))
    return(rslt)

def decode_http_headers(headers_text,ordered=1):
    rslt = {}
    arrs = headers_text.split('\r\n')
    for i in range(0,arrs.__len__()):
        one_http_header = arrs[i].split(': ')
        header_name = one_http_header[0]
        header_body = one_http_header[1]
        if(', ' in header_body):
            splitor = ' ,'
        elif(',' in header_body):
            splitor = ','
        elif(' ;' in header_body):
            splitor = '; '
        else:
            splitor = '; '
        if(ordered):
            rslt[i] = decode_one_http_head(header_name,splitor,header_body,ordered)
        else:
            rslt[header_name] = decode_one_http_head(header_name,splitor,header_body,ordered)
    return(rslt)

def encode_http_headers(headers_dict):
    rslt = ''
    for i in range(0,headers_dict.__len__() - 1):
        splitor = http_get_splitor_via_headname(headers_dict[i]['name'])
        text = encode_one_http_head(headers_dict[i],headers_dict[i]['name'],splitor,include_head=1)
        rslt = ''.join((rslt,text,'\r\n'))
    i = headers_dict.__len__() - 1
    splitor = http_get_splitor_via_headname(headers_dict[i]['name'])
    text = encode_one_http_head(headers_dict[i],headers_dict[i]['name'],splitor,include_head=1)
    rslt = ''.join((rslt,text))
    return(rslt)

def http_get_splitor_via_headname(head_name):
    const_http_header_splitor_dict = {
        'Accept':", ",
        'Accept-Encoding':", ",
        'Content-Disposition':"; ",
        'Content-Type':"; ",
        'Cookie':"; ",
        'X-UA-Compatible':','
    }
    if(head_name in const_http_header_splitor_dict):
        return(const_http_header_splitor_dict[head_name])
    else:
        return('; ')

def http_remove_first_head(disp_text):
    rslt =''
    arrs = http_all.split('\r\n')
    for i in range(1,arrs.__len__()):
        rslt = ''.join((rslt,'\r\n',arrs[i]))
    return(rslt.lstrip('\r').lstrip('\n'))

###################################3
def build_headers_dict_from_str(head_str,SP='\r\n'):
    '''
    head_str = 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\nUser-Agent: Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36\nAccept-Encoding: gzip,deflate,sdch\nAccept-Language: en;q=1.0, zh-CN;q=0.8'
    '''
    headers = {}
    regex_H = re.compile('(.*): (.*)')
    sp_HS = head_str.split(SP)
    for i in range(0,sp_HS.__len__()):
        m = regex_H.search(sp_HS[i])
        HN = m.group(1)
        HV = m.group(2)
        headers[HN] = HV
    return(headers)

def build_headers_tuple_list_from_str(head_str,SP='\r\n'):
    '''
    head_str = 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\nUser-Agent: Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36\nAccept-Encoding: gzip,deflate,sdch\nAccept-Language: en;q=1.0, zh-CN;q=0.8'
    '''
    headers = []
    regex_H = re.compile('(.*): (.*)')
    sp_HS = head_str.split(SP)
    for i in range(0,sp_HS.__len__()):
        m = regex_H.search(sp_HS[i])
        HN = m.group(1)
        HV = m.group(2)
        headers.append((HN,HV))
    return(headers)

def build_headers_str_from_dict(head_dict):
    head_str =''
    for key in head_dict:
        head_str = ''.join((head_str,key,': ',head_dict[key],'\r\n'))
    head_str.rstrip('\n')
    head_str.rstrip('\r')
    return(head_str)

def build_headers_str_from_tuple_list(head_tuple_list):
    head_str =''
    for i in range(0,head_tuple_list.__len__()):
        temp = head_tuple_list[i]
        key = temp[0]
        value = temp[1]
        head_str = ''.join((head_str,key,': ',value,'\r\n'))
    head_str.rstrip('\n')
    head_str.rstrip('\r')
    return(head_str)



def http_remove_head_from_head_str(head_name,head_str,keep_order=0):
    if(keep_order):
        head_tuple_list = build_headers_tuple_list_from_str(head_str)
        head_str =''
        for i in range(0,head_tuple_list.__len__()):
            temp = head_tuple_list[i]
            key = temp[0]
            value = temp[1]
            if(key == head_name):
                pass
            else:
                head_str = ''.join((head_str,key,': ',value,'\r\n'))
        head_str.rstrip('\n')
        head_str.rstrip('\r')
    else:
        head_dict = build_headers_dict_from_str(head_str)
        del head_dict[head_name]
        head_str = build_headers_str_from_dict(head_dict)
    return(head_str)



def expand_headers_dict_via_head_string_list(Cheaders,ex_String_List):
    new_Cheaders = {}
    for each in Cheaders:
        new_Cheaders[each] = Cheaders[each]
    regex_H = re.compile('(.*): (.*)')
    for each in ex_String_List:
        m = regex_H = re.compile('(.*): (.*)')
        new_Cheaders[m.group(1)] = m.group(2)
    return(new_Cheaders)

    
    

#############
def with_quality_head_str_to_tuple_list(Accept_text,name,sp=','):
    '''
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Accept
        Accept: <MIME_type>/<MIME_subtype>
        Accept: <MIME_type>/*
        Accept: */*
        Accept: text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8
        Accept_text = 'Accept: text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8'
        accept_head_str_to_dict(Accept_text)
        
        apply to name :  Accept ,Accept-Charset,Accept-Encoding,Accept-Language,Accept-Ranges,Keep-Alive
    '''
    s_rep = ''.join((sp,' '))
    Accept_text = Accept_text.replace(s_rep,sp)
    Accept_dict = decode_one_http_head(name,sp,Accept_text,ordered=1)
    name_list = []
    qualisty_list = []
    seq = 0
    for i in range(0,Accept_dict.__len__()-1):
        kv = Accept_dict[i]
        k = Accept_dict[i][0]
        v = Accept_dict[i][1]
        if(k == ''):
            name_list.append(v)
            qualisty_list.append(1.0)
        else:
            key = k.rstrip('q').rstrip(';')
            name_list.append(key)
            qualisty_list.append(float(v))
    pn_list = {}
    for i in range(0,qualisty_list.__len__()):
        pn_list[name_list[i]] = qualisty_list[i]
    new_pn_list = sorted(pn_list.items(), key=operator.itemgetter(1),reverse=True)
    return(new_pn_list)


def with_quality_head_tuple_list_to_str(head_tuple_list,name,sp=',',explicit=0):
    head = ''.join((name,': '))
    for i in range(0,head_tuple_list.__len__()):
        t = head_tuple_list[i][0]
        q = head_tuple_list[i][1]
        if((explicit==0) & (q==1.0)):
            tq = ''.join((t,sp,' '))
        else:
            tq = ''.join((t,';','q=',str(q),sp,' '))
        head = ''.join((head,tq))
    head = head.rstrip(' ')
    head = head.rstrip(sp)
    return(head)


def access_control_head_str_to_tuple_list(Accept_text,name):
    '''
        Access-Control-Allow-Credentials
        Access-Control-Allow-Headers
        Access-Control-Allow-Methods
        Access-Control-Allow-Origin
        Access-Control-Expose-Headers
        Access-Control-Max-Age
        Access-Control-Request-Headers
        Access-Control-Request-Method
    '''
    Accept_text = Accept_text.replace(', ',',')
    Accept_dict = decode_one_http_head(name,',',Accept_text,ordered=1)
    name_list = []
    qualisty_list = []
    seq = 0
    for i in range(0,Accept_dict.__len__()-1):
        kv = Accept_dict[i]
        k = Accept_dict[i][0]
        v = Accept_dict[i][1]
        if(k == ''):
            name_list.append(v)
            qualisty_list.append(1.0)
        else:
            key = k.rstrip('q').rstrip(';')
            name_list.append(key)
            qualisty_list.append(float(v))
    pn_list = {}
    for i in range(0,qualisty_list.__len__()):
        pn_list[name_list[i]] = qualisty_list[i]
    new_pn_list = sorted(pn_list.items(), key=operator.itemgetter(1),reverse=True)
    return(new_pn_list)


def access_control_head_tuple_list_to_str(head_tuple_list,name,explicit=0):
    head = ''.join((name,': '))
    for i in range(0,head_tuple_list.__len__()):
        t = head_tuple_list[i][0]
        q = head_tuple_list[i][1]
        if((explicit==0) & (q==1.0)):
            tq = ''.join((t,', '))
        else:
            tq = ''.join((t,';','q=',str(q),', '))
        head = ''.join((head,tq))
    head = head.rstrip(' ')
    head = head.rstrip(',')
    return(head)




def name_value_exist_in_headers(rheaders,header,HV):
    len = rheaders.__len__()
    for i in range(0,len):
        if(rheaders[i][0]==header):
            if(rheaders[i][1]==HV):
                return(1)
            else:
                return(-1)
    return(0)


def select_headers_via_key_from_tuple_list(headers_turple_array,key,**kwargs):
    if('mode' in kwargs):
        mode = kwargs['mode']
    else:
        mode = 'loose'
    # 返回的是符合条件的tuple_list
    arr = headers_turple_array
    arr_len = arr.__len__()
    rslt = []
    for i in range(0,arr_len):
        k = arr[i][0]
        v = arr[i][1]
        if(mode == 'strict'):
            cond = (k == key)
        else:
            cond = (k.upper() == key.upper())
        if(cond):
            temp = (k,v)
            rslt.append(temp)
    return(rslt)
    


def get_resp_headers_vl_dict_from_resp(resp):
    Rheaders_Dict = {}
    keys = resp.info().keys()
    values = resp.info().values()
    for i in range(0,keys.__len__()):
        if(keys[i] in Rheaders_Dict):
            Rheaders_Dict[keys[i]].append(values[i])
        else:
            Rheaders_Dict[keys[i]] = [values[i]]
    return(Rheaders_Dict)

    
def is_mobile_user_agent(Cheaders):
    CUA = Cheaders['User-Agent']
    regex_Mobile_UA = re.compile('applewebkit.*mobile.*|windows.*phone.*mobile.*|msie.*touch.*wpdesktop|android.*mobile.*|android.*applewebkit.*',re.I)
    if(regex_Mobile_UA.search(CUA)):
        return(True)
    else:
        return(False)

def creat_B2I_url(Cheaders,Rerirecto_Url):
    regex_B2I = re.compile('bootstrap')
    if(is_mobile_user_agent(Cheaders)):
        url = regex_B2I.sub('mobile_index',Rerirecto_Url,0)
    else:
        url = regex_B2I.sub('index',Rerirecto_Url,0)
    return(url)
    

def get_date_from_resp(resp):
    resp_head_dict = get_resp_headers_vl_dict_from_resp(resp)
    if('Date' in resp_head_dict):
        date = resp_head_dict['Date']
        time_format = time_utils.detect_time_format(date)  
        return({'orig':date,'format':time_format})
    else:
        return(None)



def get_content_type_from_resp(resp):
    resp_head_dict = get_resp_headers_vl_dict_from_resp(resp)
    #ct = resp.getheader('Content-Type')
    if('Content-Type' in resp_head_dict):
    #if(ct):
        charset = 'utf-8'
        ct = resp_head_dict['Content-Type']
        for i in range(0,ct.__len__()):
            temp = ct[i].split('; ')
            for j in range(0,temp.__len__()):
                if('/' in temp[j]):
                    data_type = temp[j]
                elif('charset' in temp[j]):
                    t = temp[j].split('=')
                    charset = t[1]
        return({'data_type':data_type,'charset':charset})
    else:
        return(None)


def get_redirect_url_from_resp(resp,**kwargs):
    #301,302,303,307
    #301 永久重定向,告诉客户端以后应从新地址访问.
    #302 作为HTTP1.0的标准,以前叫做Moved Temporarily ,现在叫Found. 现在使用只是为了兼容性的处理,包括PHP的默认Location重定向用的也是302.
    #但是HTTP 1.1 有303 和307作为详细的补充,其实是对302的细化
    #303：对于POST请求，它表示请求已经被处理，客户端可以接着使用GET方法去请求Location里的URI。
    #307：对于POST请求，表示请求还没有被处理，客户端应该向Location里的URI重新发起POST请求。
    resp_headers = resp.getheaders()
    locs =  select_headers_via_key_from_tuple_list(resp_headers,'Location')
    length = locs.__len__()
    if(length == 0):
        return(None)            
    else:
        loc = locs[0]
        return(loc[1])



def get_abs_redirect_url_from_resp(resp,url):
    #@@@@
    loc = get_redirect_url_from_resp(resp)
    if(loc==None):
        return(None)
    else:
        abs_url = url_tool.get_abs_url(loc,base=url)
    return(abs_url)  

def get_redirect_url(ic,**kwargs):
    '''
    '''
    if('mode' in kwargs):
        mode = kwargs['mode']
    else:
        mode = 'abs'
    if('url' in kwargs):
        url = kwargs['url']
    else:
        pass
    t = str(type(ic))
    if( "http.client.HTTPResponse" in t):
        #resp
        if(mode == 'abs'):
            return(get_abs_redirect_url_from_resp(ic,url))
        else:
            return(get_redirect_url_from_resp(ic))
    elif('dict' in t):
        #info_container
        if(mode == 'abs'):
            return(get_abs_redirect_url_from_resp(ic['resp'],ic['url']))
        else:
            return(get_redirect_url_from_resp(ic['resp']))
    else:
        #resp_head
        rel = select_headers_via_key_from_tuple_list(ic,'Location')[0]
        if(mode == 'abs'):
            origin = url_tool.get_origin(url)
            if(rel[0] == '/'):
                abs_url = origin + rel
            else:
                abs_url = rel
            return(abs_url)
        else:
            return(rel)
#@@@


#-----------------------------------implement cache
def get_cache_control_dict():
    ccd = {}
    ccd['request'] = ['max-age','max-stale','min-fresh','no-cache','no-store','no-transform','only-if-cached']
    ccd['response'] = ['must-revalidate', 'no-cache', 'no-store', 'no-transform', 'public', 'private', 'proxy-revalidate', 'max-age', 's-maxage']
    ccd['extension'] = ['immutable','stale-while-revalidate','stale-if-error']
    return(ccd)

def creat_cache_dir():
    '''
        public
        private-user1
               -user2
               -user3
        
    '''

def handle_cache_control(cache_control_text):
    cache_control_text = cache_control_text.replace(', ',',')
    cache_control_dict = decode_one_http_head('Cache-control',',',cache_control_text,ordered=1)
    for i in range(0,Accept_dict.__len__()-1):
        v = cache_control_dict[i][1]
        if('public' in v):
            print('the response may be cached by any cache')
        elif('private' in v):
            print('A private cache may store the response')
        elif('no-cache' in v):
            print('submit the request to the origin server for validation before releasing a cached copy.')
        elif('only-if-cached' in v):
            print('only wishes to obtain a cached response, and should not contact the origin-server to see if a newer copy exists')
           


######

#referer:
#referer存在于所有请求，而origin只存在于post请求
#referer显示来源页面的完整地址，而origin显示来源页面的origin: protocal+host
#Location 等导致的redirect 不在referer/origin 链中
#这个功能放到records中实现

# referer 的 metedata 参数可以设置为以下几种类型的值：

# never
# always
# origin
# default

# 如果在文档中插入 meta 标签，并且 name 属性的值为 referer，浏览器客户端将按照如下步骤处理这个标签：

# 1.如果 meta 标签中没有 content 属性，则终止下面所有操作
# 2.将 content 的值复制给 referrer-policy ，并转换为小写
# 3.检查 content 的值是否为上面 list 中的一个，如果不是，则将值置为 default

# 上述步骤之后，浏览器后续发起 http 请求的时候，会按照 content 的值，做出如下反应(下面 referer-policy 的值即 meta 标签中 content 的值)：

# 1.如果 referer-policy 的值为never：删除 http head 中的 referer；
# 2.如果 referer-policy 的值为default：如果当前页面使用的是 https 协议，而正要加载的资源使用的是普通的 http 协议，则将 http header 中的 referer 置为空；
# 3.如果 referer-policy 的值为 origin：只发送 origin 部分；
# 4.如果 referer-policy 的值为 always：不改变http header 中的 referer 的值，注意：这种情况下，如果当前页面使用了 https 协议，而要加载的资源使用的是 http 协议，加载资源的请求头中也会携带 referer。

#https://w3c.github.io/webappsec-referrer-policy/
#https://tools.ietf.org/html/rfc7231#section-5.5.2



#

import tlist.tlist as tltl


def get_header(ic,head_name,**kwargs):
    if(tltl.is_tlist(ic)):
        resp_head = ic
    else:
        resp_head = ic['resp_head'] 
    l = tltl.get_value(resp_head,head_name)
    if(l.__len__() == 1):
        return(l[0])
    else:
        return(l)



def get_etag(ic,**kwargs):
    return(get_header(ic,'ETag',**kwargs))


def get_last_modified(ic,**kwargs):
    return(get_header(ic,'Last-Modified',**kwargs))


def get_expires(ic,**kwargs):
    return(get_header(ic,'Expires',**kwargs))

def get_date(ic,**kwargs):
    return(get_header(ic,'Date',**kwargs))

def get_cahce_control(ic,**kwargs):
    return(get_header(ic,'Cache-Control',**kwargs))

def get_server(ic,**kwargs):
    return(get_header(ic,'Server',**kwargs))

def get_set_cookie(ic,**kwargs):
    return(get_header(ic,'Set-Cookie',**kwargs))

def get_x_powered_by(ic,**kwargs):
    return(get_header(ic,'X-Powered-By',**kwargs))

def get_connection(ic,**kwargs):
    return(get_header(ic,'Connection',**kwargs))










# Navegador web

import http.client
import urllib.parse
import time
import datetime
import operator
from navegador5 import url_tool
from navegador5 import shell_cmd
from navegador5 import head
from navegador5 import body
from navegador5.cookie import cookie
from navegador5 import time_utils
from navegador5 import status_code
import platform
import socket

from pyquery import PyQuery as pq

###########################
 #requests
 # '_content',
 # '_content_consumed',
 # '_next',
 # 'apparent_encoding',
 # 'close',
 # 'connection',
 # 'content',
 # 'cookies',
 # 'elapsed',
 # 'encoding',
 # 'headers',
 # 'history',
 # 'is_permanent_redirect',
 # 'is_redirect',
 # 'iter_content',
 # 'iter_lines',
 # 'json',
 # 'links',
 # 'next',
 # 'ok',
 # 'raise_for_status',
 # 'raw',
 # 'reason',
 # 'request',
 # 'status_code',
 # 'text',
 # 'url'
#######################


##############
# 数据结构设计
# conn        keepalive 模式下有用
# method
# url
# origin      域
# referer     上一条访问的url
# req_head    req.head
# req_body    req.body
# resp_head   res.head
# resp_body   res.body
# resp_code   res.code
########################
# auto_keepalive     
#     --------根据返回的Connection 头部自动处理
# auto_redirect      
#     --------Location 头部    
# auto_update_cookie
#     --------Cookie 的三个来源
#####################



#############
def shutdown(info_container,how=socket.SHUT_WR):
    '''close()releases the resource associated with a connection but does not 
       necessarily close the connection immediately. 
       If you want to close the connection in a timely fashion, callshutdown() beforeclose().
       socket.SHUT_RD 0 
       socket.SHUT_WR 1
       socket.SHUT_RDWR 2
       使用shutdown来关闭socket的功能
       SHUT_RDWR：关闭读写，即不能使用send/write/recv/read等
       SHUT_RD：关闭读，即不能使用read/recv等
       SHUT_WR:关闭写功能，即不能使用send/write等
       除此之外，还将缓冲区中的内容清空
    '''
    try:
        info_container['conn'].sock.shutdown(how)
        info_container['conn'].sock.close()
    except:
        pass
    else:
        pass
    info_container['shutdown'] = 1
    return(info_container)


def is_shutted(info_container):
    try:
        info_container['conn'].sock.send(b"\x00")
    except:
        return(0)
    else:
        return(1)


def links_pool(num,base_url):
    pool = {'links':[],'domain':base_url}
    for i in range(0,num):
        link = keepalive_init(base_url)
        pool['links'].append(link)
    return(pool)

def select_from_link_pool(pool):
    for seq in range(0,pool['links'].__len__()):
        info_container,records_container = each
        if(info_container['inuse']==0):
            info_container['inuse']=1
            return((info_container,records_container,seq))
        else:
            pass
    return(None)

def return_to_link_pool(pool,seq):
    '''you can do shutdown before return to make sure not exceed th max links'''
    base_url = pool['domain']
    pool['links'][seq] = keepalive_init(base_url)
    return(pool)

##############


def check_body(info_container,**kwargs):
    if('codec' in kwargs):
        codec = kwargs['codec']
    else:        
        codec = head.get_content_type_from_resp(info_container['resp'])['charset'].lower()
        if(codec):
            pass
        else:
            codec = 'utf-8'
    print(info_container['resp_body_bytes'].decode(codec))


def new_info_container():
    info_template = {
        'resp':None,
        'resp_head': [], 
        'resp_body_bytes': None,
        'resp_body_text':None,
        'resp_body_query':None,
        'resp_body_codec':None, 
        'req_head': None, 
        'req_body': None, 
        'method':None,
        'url': None, 
        'from_url':None,
        'referer':None,
        'origin':None,
        'step': 0, 
        'conn': None,
        'auto_update_cookie':0,
        'auto_redirected':0,
        'shutdown':0,
        'inuse':0,
        'reopened':0,
        'reopen_reason':'',
        'reason':None,
        'code':None
    }
    return(info_template)

def new_records_container():
    records_template = {
        'urls':{},
        'referers':{},
        'steps':{}
    }
    return(records_template)


def keepalive_init(base_url,**kwargs):
    info_container = new_info_container()
    info_container['base_url'] = base_url
    info_container['method'] = 'GET'
    if('UAnum' in kwargs):
        req_head_str = head.HEAD_POOL[kwargs['UAnum']]
    else:
        req_head_str = '''User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2\r\nAccept-Encoding: gzip, deflate, br'''
    info_container['req_head'] = head.build_headers_dict_from_str(req_head_str,'\r\n')
    info_container['req_head']['Connection'] = 'keep-alive'
    for key in kwargs:
        info_container['req_head'][key] = kwargs[key]
    #### init records_container
    records_container = new_records_container()
    return((info_container,records_container))


####
def dup_req(ic,**kwargs):
    info_container = new_info_container()
    info_container['auto_update_cookie'] = ic['auto_update_cookie']
    info_container['req_body'] = ic['req_body']
    info_container['base_url'] = ic['base_url'] 
    info_container['from_url'] = ic['from_url']   
    info_container['method'] = ic['method']
    info_container['auto_redirected'] = ic['auto_redirected']
    info_container['url'] = ic['url']
    info_container['req_head'] = ic['req_head']
    info_container['referer'] = ic['referer']
    info_container['origin'] = ic['origin']
    return(info_container)












####


def nonkeepalive_init(base_url,**kwargs):
    info_container = new_info_container()
    info_container['base_url'] = base_url
    info_container['method'] = 'GET'
    if('UAnum' in kwargs):
        req_head_str = head.HEAD_POOL[kwargs['UAnum']]
    else:
        req_head_str = '''User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2\r\nAccept-Encoding: gzip, deflate, br'''
    info_container['req_head'] = head.build_headers_dict_from_str(req_head_str,'\r\n')
    info_container['req_head']['Connection'] = 'close'
    for key in kwargs:
        info_container['req_head'][key] = kwargs[key]
    #### init records_container
    records_container = new_records_container()
    return((info_container,records_container))


def connection(url_scheme,url_Netloc,**kwargs):
    if('port' in kwargs):
        port = kwargs['port']
    else:
        port =None
    if('timeout' in kwargs):
        timeout = kwargs['timeout']
    else:
        timeout = 60
    if(url_scheme == 'http'):
        if(port==None):
            port = 80 
        else:
            pass
        conn = http.client.HTTPConnection(url_Netloc,port,timeout)
    else:
        if(port==None):
            port = 443 
        else:
            pass
        conn = http.client.HTTPSConnection(url_Netloc,port,None,None,timeout)
    return(conn)

def stepping_req(conn,method,url_path,**kwargs):
    '''
        refer to https://docs.python.org/3/library/http.client.html
        If headers contains neither Content-Length nor Transfer-Encoding, but there is a request body, 
        one of those header fields will be added automatically. If body is None, 
        the Content-Length header is set to 0 for methods that expect a body (PUT, POST, and PATCH). 
        If body is a string or a bytes-like object that is not also a file, the Content-Length header is set to its length. 
        Any other type of body (files and iterables in general) will be chunk-encoded, 
        and the Transfer-Encoding header will automatically be set instead of Content-Length.
        The encode_chunked argument is only relevant if Transfer-Encoding is specified in headers. 
        If encode_chunked is False, the HTTPConnection object assumes that all encoding is handled by the calling code. 
        If it is True, the body will be chunk-encoded.
        Changed in version 3.6: If neither Content-Length nor Transfer-Encoding are set in headers, 
        file and iterable body objects are now chunk-encoded. The encode_chunked argument was added. 
        No attempt is made to determine the Content-Length for file objects.
    '''
    #encode_chunked only supportted in python3.6
    if('encode_chunked' in kwargs):
        encode_chunked = kwargs['encode_chunked']
    else:
        encode_chunked = False
    if('req_head' in kwargs):
        req_head = kwargs['req_head']
    else:
        req_head = None
    if(type({}) == type(req_head)):
        req_head_dict = req_head
    else:
        req_head_dict = None
    if(type('') == type(req_head)):
        req_head_str = req_head
    else:
        req_head_str = None
    if(req_head_str==None):
        if(req_head_dict==None):
            req_head_dict = {}
        else:
            req_head_dict = req_head_dict
    else:
        req_head_dict = head.build_headers_dict_from_str(req_head_str,'\n')
    #body is string or bytes
    if('req_body' in kwargs):
        req_body = kwargs['req_body']
    else:
        req_body = None
    if(method == "GET"):
        #GET 请求中应该处理一些通用动作，比如删除Content-Type
        if('Content-Type' in req_head_dict):
            del req_head_dict['Content-Type']
        else:
            pass
        if(type(req_body)==type({})):
            req_body = url_tool.urlencode(req_body)
            url_path = ''.join((url_path,"?",req_body))
    if(method == "POST"):
        if(type(req_body)==type({})):
            req_body = url_tool.urlencode(req_body)
    try:
        conn.request(method,url_path,headers=req_head_dict,body=req_body)
    except Exception as e:
        #to avoid socket.gaierror: [Errno -2] Name or service not known
        print(e)
    else:
        pass
    return(conn)



#this will error when the remote RST
#>>> conn.sock
#<ssl.SSLSocket fd=3, family=AddressFamily.AF_INET, type=2049, proto=6, laddr=('192.168.75.128', 41597)>
#>>>
#>>> conn.sock.getsockname()
#('192.168.75.128', 41597)
#>>> conn.sock.getpeername()
#Traceback (most recent call last):
#  File "<stdin>", line 1, in <module>
#OSError: [Errno 107] Transport endpoint is not connected
#>>>
#this happend when the remote send RST
#<REMOTE IP_ADD> 192.168.75.128	TCP	54	https > 41597 [RST, ACK] Seq=3517 Ack=1109 Win=64240 Len=0

def linux_check_tcp_state_via_conn(conn):
    '''#this will error when the remote RST
       #>>> conn.sock
       #<ssl.SSLSocket fd=3, family=AddressFamily.AF_INET, type=2049, proto=6, laddr=('192.168.75.128', 41597)>
       #>>>
       #>>> conn.sock.getsockname()
       #('192.168.75.128', 41597)
       #>>> conn.sock.getpeername()
       #Traceback (most recent call last):
       #  File "<stdin>", line 1, in <module>
       #OSError: [Errno 107] Transport endpoint is not connected
       #>>>
       #this happend when the remote send RST
       #<REMOTE IP_ADD> 192.168.75.128 TCP    54    https > 41597 [RST, ACK] Seq=3517 Ack=1109 Win=64240 Len=0
    '''
    if(conn==None):
        return("_CONN_NONE")
    elif(conn.sock == None):
        return("_SOCK_NONE")
    else:
        pass
    LA = None
    FA = None
    try:
        LA  = ''.join((conn.sock.getsockname()[0],':',str(conn.sock.getsockname()[1])))
    except:
        return("_LOCAL_NONE")
    else:
        pass
    try:
        FA = ''.join((conn.sock.getpeername()[0],':',str(conn.sock.getpeername()[1])))
    except:
        return("_REMOTE_NONE")
    else:
        pass
    egrep_RE_string = ''.join((LA,'[ ]+',FA))
    shell_CMDs = {}
    shell_CMDs[1] = 'netstat -n'
    shell_CMDs[2] = ''.join(('egrep ','"',egrep_RE_string,'"'))
    shell_CMDs[3] = "awk {'print $6'}"
    state = shell_cmd.pipe_shell_cmds(shell_CMDs)[0].decode().strip('\n').strip(' ')
    return(state)

def getipport_from_conn(conn):
    src_ip,src_port,dst_ip,dst_port = (None,None,None,None)
    try:
        src_ip =conn.sock.getsockname()[0]
        src_port = conn.sock.getsockname()[1]
    except:
        pass
    else:
        pass
    try:
        dst_ip = conn.sock.getpeername()[0]
        dst_port = conn.sock.getpeername()[1]
    except:
        pass
    else:
        pass
    return((src_ip,src_port,dst_ip,dst_port))

def linux_check_tcp_state_via_ipport(src_ip,src_port,dst_ip,dst_port):
    LA  = ''.join((str(src_ip),':',str(src_port)))
    FA = ''.join((str(dst_ip),':',str(dst_port)))
    egrep_RE_string = ''.join((LA,'[ ]+',FA))
    shell_CMDs = {}
    shell_CMDs[1] = 'netstat -n'
    shell_CMDs[2] = ''.join(('egrep ','"',egrep_RE_string,'"'))
    shell_CMDs[3] = "awk {'print $6'}"
    state = shell_cmd.pipe_shell_cmds(shell_CMDs)[0].decode().strip('\n').strip(' ')
    return(state)

def linux_record_state_change_via_conn(conn,check_interval=1,count=500):
    records = [("",0)]
    prev_rslt = ""
    prev_t = time.time()
    init_t = prev_t    
    meeted = 0
    while(1):
        try:
            rslt = linux_check_tcp_state_via_conn(conn)
            if(rslt == prev_rslt):
                print(rslt)                
            else:
                t = time.time()
                diff_t = t - prev_t
                print("from {0} to {1} afte {2} secs".format(prev_rslt,rslt,diff_t))
                records.append((rslt,diff_t))
                prev_rslt = rslt
                prev_t = t
        except:
            rslt = ""
            t =time.time()
            diff_t = t - prev_t
            records.append((rslt,diff_t))
            if(meeted==1):
                total_t = t - init_t
                print("{0}seconds elapsed finally".format(total_t))
                break
            else:
                pass
        else:
            meeted = 1
        time.sleep(check_interval)
    return(records) 
    




def linux_record_state_change_via_ipport(src_ip,src_port,dst_ip,dst_port,check_interval=1,count=500):
    records = [("",0)]
    prev_rslt = ""
    prev_t = time.time()
    init_t = prev_t
    meeted = 0
    while(1):
        rslt = linux_check_tcp_state_via_ipport(src_ip,src_port,dst_ip,dst_port)
        if(rslt == ""):
            pass
        else:
            meeted = 1
        if(rslt == prev_rslt):
            print(rslt)
        else:
            t = time.time()
            diff_t = t - prev_t
            print("from {0} to {1} afte {2} secs".format(prev_rslt,rslt,diff_t))
            records.append((rslt,diff_t))
            prev_rslt = rslt
            prev_t = t
        if((meeted==1)&(rslt =="")):
            t =time.time()
            diff_t = t - prev_t
            records.append((rslt,diff_t))
            total_t = t - init_t
            print("{0}seconds elapsed finally".format(total_t))
            break
        else:
            pass
        time.sleep(check_interval)
    return(records)


def linux_manual_close_conn(conn,keepalive_timeout=0,how=socket.SHUT_WR):
    time.sleep(keepalive_timeout)
    r_TCP_state = self.linux_check_tcp_state(conn)
    print(r_TCP_state)
    if(r_TCP_state=='ESTABLISHED'):
        pass
    else:
        print('TCP STATE {0} ,IMPLICIT CONN RESP MODE, CLOSE CONN'.format(r_TCP_state))
        conn.sock.shutdown(how)
        conn.sock.close()



####
class RespError(Exception):
    pass

class RespHeadError(Exception):
    pass

class RespBodyError(Exception):
    pass
####

def stepping_resp(conn,client_close_when_recv_Connection_close=0):
    try:
        resp = conn.getresponse()
    except Exception as e:
        print("----resp Exception-----")
        print("Exception: ")
        print(e)
        print("----resp Exception-----")
        #return((conn,[],None,None))
        raise RespError()
    else:
        pass
    try:
        resp_head = resp.getheaders()
    except Exception as e:
        print("----resp_head Exception-----")
        print("Exception: ")
        print(e)
        print("----resp_head Exception-----")
        #return((conn,[],None,None))
        raise RespHeadError()
    else:
        pass
    try:
        resp_body_bytes = resp.read()
    except Exception as e:
        print("----resp_body Exception-----")
        print("Exception: ")
        print(e)
        print("resp_head: ")
        print(resp_head)
        #resp_body_bytes = None
        print("----resp_body Exception-----")
        raise RespBodyError()
    else:
        pass
    #
    #secarino_1 = head.name_value_exist_in_headers(resp_head,'Connection','Keep-Alive')
    #secarino_2 = head.name_value_exist_in_headers(resp_head,'Connection','keep-alive')
    #
    tmp = head.select_headers_via_key_from_tuple_list(resp_head,'connection')
    if(tmp.__len__()==0):
        pass
    else:
        v = tmp[0][1].lower()
        if(v == "keep-alive"):
            print("recv ex keepalive")
            pass
        elif(v == "close"):
            print("recv ex close")
            if(client_close_when_recv_Connection_close):
                print("        :client do close")
                conn.close()
            else:
                print("        :wait for server for ex close")
                pass
        else:
            print("recv im keepalive")
            pass
    return((conn,resp_head,resp_body_bytes,resp))


def obseleted_walkon(info_container,**kwargs):
    '''by default auto_update_cookie enabled'''
    step = info_container['step']
    ####
    #from_url = info_container['from_url']
    ####
    url = info_container['url']
    method = info_container['method']
    conn = info_container['conn']
    req_head = info_container['req_head']
    #body is string or bytes
    req_body = info_container['req_body']
    if(info_container['method'] == 'GET'):
        try:
            del info_container['req_head']['Content-Type']
            del info_container['req_head']['Content-Length']
        except:
            pass
        else:
            pass
        info_container['req_body'] = None
    else:
        pass
    if('save_scripts' in kwargs):
        save_scripts = kwargs['save_scripts']
    else:
        save_scripts = 0
    if('client_close_when_recv_Connection_close' in kwargs):
        client_close_when_recv_Connection_close = kwargs['client_close_when_recv_Connection_close']
    else:
        client_close_when_recv_Connection_close = 0
    url_scheme = urllib.parse.urlparse(url).scheme
    url_Netloc = urllib.parse.urlparse(url).netloc
    if('default_port' in kwargs):
        default_port = kwargs['default_port']
    else:
        if('https' in url_scheme):
            default_port = 443
        elif('http' in url_scheme):
            default_port = 80
        else:
            default_port = None
    url_NL_HP = url_tool.parse_url_netloc(url_Netloc,default_port)
    url_host = url_NL_HP[0]
    url_port = url_NL_HP[1]
    url_path = urllib.parse.urlparse(url).path
    url_Params = urllib.parse.urlparse(url).params
    url_Query = urllib.parse.urlparse(url).query
    url_Fragment = urllib.parse.urlparse(url).fragment
    if('upgrade_records' in kwargs):
        upgrade_records = kwargs['upgrade_records']
    else:
        upgrade_records = 1
    if(upgrade_records):
        if('records_container' in kwargs):
            records_container = kwargs['records_container']
        else:
            records_container = new_records_container()
        records_container['steps'][step] = step
        records_container['urls'][step] = url
        if('Referer' in info_container['req_head']):
            records_container['referers'][step] = info_container['req_head']['Referer']
    else:
        pass
    if('port' in kwargs):
        port = kwargs['port']
    else:
        port = None
    if('timeout' in kwargs):
        timeout = kwargs['timeout']
    else:
        timeout = 60
    if(step == 0):
        conn = connection(url_scheme,url_Netloc,port=port,timeout=timeout)
    else:
        if(conn.sock == None):
            conn.close()
            conn = connection(url_scheme,url_Netloc,port=port,timeout=timeout)
        else:
            if(conn==None):
                conn = connection(url_scheme,url_Netloc,port=port,timeout=timeout)
            else:
                conn = conn
    #encode_chunked only supportted in python3.6
    if('encode_chunked' in kwargs):
        encode_chunked = kwargs['encode_chunked']
    else:
        encode_chunked = False
    if(url_Query == ''):
        conn = stepping_req(conn,method,url_path,req_head=req_head,req_body=req_body)
    else:
        conn = stepping_req(conn,method,url_path+'?'+url_Query,req_head=req_head,req_body=req_body)
    conn,resp_head,resp_body_bytes,resp = stepping_resp(conn,client_close_when_recv_Connection_close=client_close_when_recv_Connection_close)
    resp_body_bytes = body.decompress_resp_body(resp_body_bytes,resp)
    if(save_scripts):
        body.findall_jscript_from_resp_body(resp_body_bytes,'s{0}'.format(step))
    else:
        pass
    step = step + 1
    info_container['step'] = step
    info_container['conn'] = conn
    info_container['resp_head'] = resp_head
    info_container['resp_body_bytes'] = resp_body_bytes
    info_container['resp'] = resp
    #--------------------------------加入cookie处理-------
    if('auto_update_cookie' in kwargs):
        auto_update_cookie = kwargs['auto_update_cookie']
    else:
        auto_update_cookie = 1
    if(auto_update_cookie):
        #from_url = url
        if('to_url' in kwargs):
            to_url = kwargs['to_url']
        else:
            to_url = from_url
        ##
        ##print("---------")
        ##print(req_head)
        ##print("---------")
        ##print(resp_head)
        ##print("---------")
        ##print(from_url)
        ##print("---------")
        ##print(to_url)
        ##print("---------")
        ##
        next_req_cookie_dict = cookie.select_valid_cookies_from_resp(req_head,resp_head,from_url,to_url)
        next_req_cookie_str = cookie.cookie_dict_to_str(next_req_cookie_dict,with_head=0)
        ####
        ##print(next_req_cookie_dict)
        ##print("---------")
        ##print(next_req_cookie_str)
        ####
        if(next_req_cookie_str ==""):
            pass
        else:
            ##print("---req_head---")
            ##print(req_head)
            ##print("---req_head_type---")
            ##print(type(req_head))
            if(type(req_head) == type({})):
                req_head['Cookie'] = next_req_cookie_str
            elif(type(req_head) == type('')):
                req_head_dict = head.build_headers_dict_from_str(req_head)
                req_head_dict['Cookie'] = next_req_cookie_str
                req_head = head.build_headers_str_from_dict(req_head_dict)
            else:
                pass
        info_container['req_head'] = req_head
        info_container['auto_update_cookie'] = 1
    else:
        info_container['auto_update_cookie'] = 0
    #--------------------------------加入cookie处理-------
    return(info_container)



def check_and_reopen_ifneeded(info_container):
    #---------------for CLOSE_WAIT  bug---------------
    #---------------when using http1.1 long-persistant keep-alive feature------------
    #---------------if the server send FIN,PSH,ACK, and the client response ACK
    #---------------client will stuck in CLOSE_WAIT state, even if NO anything in recv buffer
    #121.29.8.170       192.168.75.128  TCP     54      http > 33815 [FIN, PSH, ACK] Seq=15816 Ack=364 Win=64240 Len=0
    #192.168.75.128     121.29.8.170    TCP     60      33815 > http [ACK] Seq=364 Ack=15817 Win=59860 Len=0

    # root@ubuntu:~# netstat | egrep "(https|http)"
    # tcp        1      0 192.168.75.128:33815    121.29.8.170:http       CLOSE_WAIT
    # root@ubuntu:~# netstat | egrep "(https|http)"
    # tcp        1      0 192.168.75.128:33815    121.29.8.170:http       CLOSE_WAIT
    # root@ubuntu:~# netstat | egrep "(https|http)"
    # tcp        1      0 192.168.75.128:33815    121.29.8.170:http       CLOSE_WAIT
    # root@ubuntu:~# netstat | egrep "(https|http)"
    # tcp        1      0 192.168.75.128:33815    121.29.8.170:http       CLOSE_WAIT
    if('linux' in platform.system().lower()):
        if(info_container['conn']):
            state = linux_check_tcp_state_via_conn(info_container['conn'])
            #
            if(state.upper() ==  'ESTABLISHED'):
                pass
            elif(state.upper() ==  'CLOSE_WAIT'):
                print("---reopen new reason: {0}----".format(state))
                shutdown(info_container)
                info_container['conn'] = None
                info_container['shutdown'] = 0
                info_container['reopened'] = 1
                info_container['reopen_reason']= state.upper()
            elif(''==state.upper()):
                print("---reopen new reason: _CANT_FIND----")
                shutdown(info_container)
                info_container['conn'] = None
                info_container['shutdown'] = 0
                info_container['reopened'] = 1
                info_container['reopen_reason']= state.upper()
            elif('_'==state.upper()[0]):
                #Some me defined state such as 
                #_CONN_NONE
                #_SOCK_NONE
                #_LOCAL_NONE
                #_REMOTE_NONE
                print("---reopen new reason: {0}----".format(state))
                shutdown(info_container)
                info_container['conn'] = None
                info_container['shutdown'] = 0
                info_container['reopened'] = 1
                info_container['reopen_reason']= state.upper()
            else:
                #for other TCP state need to add some code
                pass
        else:
            #for windows need add some code
            pass
    else:
        #this is the init request
        pass
    return(info_container)




def walkon(info_container,**kwargs):
    '''by default auto_update_cookie enabled'''
    #try:
    #    print(info_container['req_head']['Cookie'])
    #except:
    #    pass
    #else:
    #    pass
    #print("--------------------------------------")
    info_container['inuse'] = 1
    step = info_container['step']
    from_url = info_container['from_url']
    url = info_container['url']
    #for the first request
    if(from_url == None):
        from_url = url
    else:
        pass
    to_url = url
    method = info_container['method']
    conn = info_container['conn']
    req_head = info_container['req_head']
    resp_head = info_container['resp_head']
    #--------------------------------加入cookie处理-------
    if('auto_update_cookie' in kwargs):
        auto_update_cookie = kwargs['auto_update_cookie']
    else:
        auto_update_cookie = 1
    if(auto_update_cookie):
        next_req_cookie_dict = cookie.select_valid_cookies_from_resp(req_head,resp_head,from_url,to_url)
        next_req_cookie_str = cookie.cookie_dict_to_str(next_req_cookie_dict,with_head=0)
        if(next_req_cookie_str ==""):
            pass
        else:
            if(type(req_head) == type({})):
                req_head['Cookie'] = next_req_cookie_str
            elif(type(req_head) == type('')):
                req_head_dict = head.build_headers_dict_from_str(req_head)
                req_head_dict['Cookie'] = next_req_cookie_str
                req_head = head.build_headers_str_from_dict(req_head_dict)
            else:
                pass
        info_container['req_head'] = req_head
        info_container['auto_update_cookie'] = 1
    else:
        info_container['auto_update_cookie'] = 0
    #--------------------------------加入cookie处理-------
    #try:
    #    print(info_container['req_head']['Cookie'])
    #except:
    #    pass
    #else:
    #    pass
    #
    #body is string or bytes
    ######################################
    #---------------for CLOSE_WAIT  bug---------------
    #---------------when using http1.1 long-persistant keep-alive feature------------
    #---------------if the server send FIN,PSH,ACK, and the client response ACK
    #---------------client will stuck in CLOSE_WAIT state, even if NO anything in recv buffer
    #121.29.8.170	192.168.75.128	TCP	54	http > 33815 [FIN, PSH, ACK] Seq=15816 Ack=364 Win=64240 Len=0
    #192.168.75.128	121.29.8.170	TCP	60	33815 > http [ACK] Seq=364 Ack=15817 Win=59860 Len=0

    # root@ubuntu:~# netstat | egrep "(https|http)"
    # tcp        1      0 192.168.75.128:33815    121.29.8.170:http       CLOSE_WAIT
    # root@ubuntu:~# netstat | egrep "(https|http)"
    # tcp        1      0 192.168.75.128:33815    121.29.8.170:http       CLOSE_WAIT
    # root@ubuntu:~# netstat | egrep "(https|http)"
    # tcp        1      0 192.168.75.128:33815    121.29.8.170:http       CLOSE_WAIT
    # root@ubuntu:~# netstat | egrep "(https|http)"
    # tcp        1      0 192.168.75.128:33815    121.29.8.170:http       CLOSE_WAIT
    if(step == 0):
        pass
    else:
        info_container = check_and_reopen_ifneeded(info_container)
        conn = info_container['conn']
    #---------------for CLOSE_WAIT  bug--------------
    #####################################
    req_body = info_container['req_body']
    if(info_container['method'] == 'GET'):
        try:
            del info_container['req_head']['Content-Type']
            del info_container['req_head']['Content-Length']
        except:
            pass
        else:
            pass
        info_container['req_body'] = None
    else:
        pass
    if('save_scripts' in kwargs):
        save_scripts = kwargs['save_scripts']
    else:
        save_scripts = 0
    if('client_close_when_recv_Connection_close' in kwargs):
        client_close_when_recv_Connection_close = kwargs['client_close_when_recv_Connection_close']
    else:
        client_close_when_recv_Connection_close = 0
    url_scheme = urllib.parse.urlparse(url).scheme
    url_Netloc = urllib.parse.urlparse(url).netloc
    if('default_port' in kwargs):
        default_port = kwargs['default_port']
    else:
        if('https' in url_scheme):
            default_port = 443
        elif('http' in url_scheme):
            default_port = 80
        else:
            default_port = None
    url_NL_HP = url_tool.parse_url_netloc(url_Netloc,default_port)
    url_host = url_NL_HP[0]
    url_port = url_NL_HP[1]
    url_path = urllib.parse.urlparse(url).path
    url_Params = urllib.parse.urlparse(url).params
    url_Query = urllib.parse.urlparse(url).query
    url_Fragment = urllib.parse.urlparse(url).fragment
    if('upgrade_records' in kwargs):
        upgrade_records = kwargs['upgrade_records']
    else:
        upgrade_records = 1
    if(upgrade_records):
        if('records_container' in kwargs):
            records_container = kwargs['records_container']
        else:
            records_container = new_records_container()
        records_container['steps'][step] = step
        records_container['urls'][step] = url
        if('Referer' in info_container['req_head']):
            records_container['referers'][step] = info_container['req_head']['Referer']
    else:
        pass
    if('port' in kwargs):
        port = kwargs['port']
    else:
        port = None
    if('timeout' in kwargs):
        timeout = kwargs['timeout']
    else:
        timeout = 60
    if(step == 0):
        conn = connection(url_scheme,url_Netloc,port=port,timeout=timeout)
    else:
        if(conn==None):
             conn = connection(url_scheme,url_Netloc,port=port,timeout=timeout)
        else:
            if(conn.sock == None):
                ####@@@@@
                #print("step:{0}".format(step))
                #print(conn)
                #release resource
                conn.close()
                ######
                #@@@@@
                conn = connection(url_scheme,url_Netloc,port=port,timeout=timeout)
            else:
                #if(conn==None):
                #    conn = connection(url_scheme,url_Netloc,port=port,timeout=timeout)
                #else:
                conn = conn
    #encode_chunked only supportted in python3.6
    if('encode_chunked' in kwargs):
        encode_chunked = kwargs['encode_chunked']
    else:
        encode_chunked = False
    if(url_Query == ''):
        conn = stepping_req(conn,method,url_path,req_head=req_head,req_body=req_body)
    else:
        conn = stepping_req(conn,method,url_path+'?'+url_Query,req_head=req_head,req_body=req_body)
    conn,resp_head,resp_body_bytes,resp = stepping_resp(conn,client_close_when_recv_Connection_close=client_close_when_recv_Connection_close)
    resp_body_bytes = body.decompress_resp_body(resp_body_bytes,resp)
    if(save_scripts):
        body.findall_jscript_from_resp_body(resp_body_bytes,'s{0}'.format(step))
    else:
        pass
    step = step + 1
    info_container['step'] = step
    info_container['conn'] = conn
    info_container['resp_head'] = resp_head
    info_container['resp_body_bytes'] = resp_body_bytes
    ###########################################################################################
    #print(info_container['resp_body_codec'])
    ####
    if(info_container['resp_body_codec']!=None):
        pass
    else:
        try:
            info_container['resp_body_codec'] = head.get_content_type_from_resp(resp)['charset']
        except:
            print("no charset in resp_head")
        ####add code to get charset from http-equiv
            info_container['resp_body_codec'] = "utf-8"
        else:
            if(info_container['resp_body_codec']):
                pass
            else:
                info_container['resp_body_codec'] = "utf-8" 
    ####
    #print(info_container['resp_body_codec'])
    ############################################################################################
    info_container['resp_body_text'] = resp_body_bytes.decode(info_container['resp_body_codec'])
    try:
        info_container['resp_body_query'] = pq(info_container['resp_body_text']) 
    except Exception as e:
        print(e)
    else:
        pass
    info_container['resp'] = resp
    info_container['from_url'] = url
    ###################
    info_container['referer'] = url
    info_container['origin'] = url_tool.get_origin(url)
    ###################
    info_container['code'] = resp.code
    info_container['reason'] = status_code.REASONS[resp.code]
    ####################
    if(step<2):
        pass
    else:
        info_container = check_and_reopen_ifneeded(info_container)
    ###################
    return(info_container)


















#-----------dont put this func in walkon, coz recursive
def auto_redireced(info_container,records_container,max_redirects=10):
    #------------------auto redirect-----------------------
    count = 0
    while(count<max_redirects):
        redirect_url = head.get_abs_redirect_url_from_resp(info_container['resp'],info_container['url'])
        if(redirect_url):
            info_container['url'] = redirect_url
            info_container = walkon(info_container,records_container=records_container)
        else:
            break
        count = count + 1
    info_container['auto_redirected'] = 1
    return(info_container)
    


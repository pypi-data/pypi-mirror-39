import urllib.parse
import os
import re
from xdict import utils
import elist.elist as elel


def get_origin(url):
    rslt = urllib.parse.urlparse(url)
    origin = rslt.scheme +'://'+rslt.netloc
    return(origin)
    

def get_base_url(url):
    temp = urllib.parse.urlparse(url)
    netloc = temp.netloc
    scheme = temp.scheme
    base_url = ''.join((scheme,'://',netloc))
    return(base_url)


def trim_after_netloc(url):
    temp = urllib.parse.urlparse(url)
    netloc = temp.netloc
    scheme = temp.scheme
    base_url = ''.join((scheme,'://',netloc))
    return(base_url)

def get_path_arr(url):
    '''
        url = "http://baidu.com/a/b/c/d.html;p1;p2?q=a#frag"
        >>> url = "http://baidu.com/a/b/c/d.html;p1;p2?q=a#frag"
        >>>
        >>> parr = get_path_arr(url)
        >>> pobj(parr)
        [
         'http://baidu.com/a',
         'http://baidu.com/a/b',
         'http://baidu.com/a/b/c',
         'http://baidu.com/a/b/c/d.html'
        ]

    '''
    temp = urllib.parse.urlparse(url)
    netloc = temp.netloc
    scheme = temp.scheme
    path = temp.path
    parent = ''.join((scheme,'://',netloc))
    path = utils.str_lstrip(path,'/',1)
    paths = path.split('/')
    rslt = []
    length = paths.__len__()
    for i in range(0,length):
        fp = parent + '/' + paths[i]
        rslt.append(fp)
        parent = fp
    return(rslt)
    
    

def trim_after_parent(url):
    '''
          url = "http://baidu.com/a/b/c/d.html;p1;p2?q=a#frag"
    '''
    rslt = get_path_arr(url)[-2]
    return(rslt)


def trim_after_ancestor(url,which):
    rslt = get_path_arr(url)[which]
    return(rslt)



def trim_after_path(url):
    temp = urllib.parse.urlparse(url)
    netloc = temp.netloc
    scheme = temp.scheme
    path = temp.path
    path_url = ''.join((scheme,'://',netloc,path))
    return(path_url)

def trim_after_params(url):
    temp = urllib.parse.urlparse(url)
    netloc = temp.netloc
    scheme = temp.scheme
    path = temp.path
    params = temp.params
    params_url = ''.join((scheme,'://',netloc,path,';',params))
    return(params_url)

def trim_after_query(url):
    temp = urllib.parse.urlparse(url)
    netloc = temp.netloc
    scheme = temp.scheme
    path = temp.path
    params = temp.params
    query = temp.query
    query_url = ''.join((scheme,'://',netloc,path,';',params,'?',query))
    return(query_url)





def url_to_dirpath(url):
    netloc = urllib.parse.urlparse(url).netloc
    path = urllib.parse.urlparse(url).path
    dirpath = ''.join((netloc,path))
    if(os.path.exists(dirpath)):
        pass
    else:
        os.makedirs(dirpath)
    return(dirpath)
    

def url_to_fn(url):
    netloc = urllib.parse.urlparse(url).netloc
    path = urllib.parse.urlparse(url).path
    path = path.replace("/","_")
    fn = ''.join((netloc,"__",path,".","html"))
    return(fn)

def parse_url_netloc(url_Netloc,default_Port):
    regex_Netloc = re.compile('(.*):(.*)')
    m = regex_Netloc.search(url_Netloc)
    if(m == None):
        url_Netloc_Host = url_Netloc
        url_Netloc_Port = default_Port
    else:
        url_Netloc_Host = m.group(1)
        url_Netloc_Port = m.group(2)
    return((url_Netloc_Host,url_Netloc_Port))

def url_to_tuple(url):
    url_Scheme = urllib.parse.urlparse(url).scheme
    url_Netloc = urllib.parse.urlparse(url).netloc
    url_Path = urllib.parse.urlparse(url).path
    url_Params = urllib.parse.urlparse(url).params
    url_Query = urllib.parse.urlparse(url).query
    url_Fragment = urllib.parse.urlparse(url).fragment
    return((url_Scheme,url_Netloc,url_Path,url_Params,url_Query,url_Fragment))


def url_to_dict(url,**kwargs):
    '''
        url = "foo://example.com:8042/over/there?name=ferret#nose"
        url = "http://www.blah.com/some;param1=foo/crazy;param2=bar/path.html"
        url =  "http://www.blah.com/some/crazy/path.html;param1=foo;param2=bar"
    '''
    if("http_default_port" in kwargs):
        http_default_port = kwargs['http_default_port']
    else:
        http_default_port = 80
    if("https_default_port" in kwargs):
        https_default_port = kwargs['https_default_port']
    else:
        https_default_port = 443
    url_Scheme = urllib.parse.urlparse(url).scheme
    if(url_Scheme == 'http'):
        default_Port = http_default_port
    else:
        default_Port = https_default_port
    url_Netloc = urllib.parse.urlparse(url).netloc
    url_NL_HP = parse_url_netloc(url_Netloc,default_Port)
    url_Netloc_Host = url_NL_HP[0]
    url_Netloc_Port = url_NL_HP[1]
    url_Path = urllib.parse.urlparse(url).path
    url_Params = urllib.parse.urlparse(url).params
    url_Query = urllib.parse.urlparse(url).query
    url_Fragment = urllib.parse.urlparse(url).fragment
    rslt = {}
    rslt['scheme'] = url_Scheme
    rslt['netloc'] = url_Netloc
    rslt['host'] = url_Netloc_Host
    rslt['port'] = url_Netloc_Port    
    rslt['path'] = url_Path    
    rslt['params'] = url_Params    
    rslt['query'] = url_Query    
    rslt['fragment'] = url_Fragment    
    return(rslt)

def dict_to_url(url_dict):
    '''scheme://host:port/path?query#fragment
     url = "https://servicegate.suunto.com/UserAuthorityService/?callback=jQuery18108122223665320987_1485771086287&service=Movescount&emailAddress=xxxxxxxx%40163.com&password=xxxxxx&_=1485771109116#a=b&c=d&e=f"
     urllib.parse.urlparse(url)
     <scheme>://<username>:<password>@<host>:<port>/<path>;<parameters>?<query>#<fragment>
     url2 = "http://www.blah.com/some;param1=foo/crazy;param2=bar/path.html"
     >>> urllib.parse.urlparse(url2)
     ParseResult(scheme='http', netloc='www.blah.com', path='/some;param1=foo/crazy;param2=bar/path.html', params='', query='', fragment='')
     urllib.parse.urlparse(url2)
     url3 = "http://www.blah.com/some/crazy/path.html;param1=foo;param2=bar"
    >>> urllib.parse.urlparse(url3)
     ParseResult(scheme='http', netloc='www.blah.com', path='/some/crazy/path.html', params='param1=foo;param2=bar', query='', fragment='')
     params_dict = {'param1': 'foo', 'param2': 'bar'}
     
     servicegate_url_dict = {
        'scheme':"https",
        'netloc':"servicegate.suunto.com",
        'path':"UserAuthorityService",
        'query_dict':{
            'callback': jQuery_get_random_jsonpCallback_name(),
            'emailAddress':"terryinzaghi@163.com",
            'password':"shu6LA",
            '_':jQuery_unix_now(),
            'service':"Movescount"
        }
    }
     '''
    url_dict_template = {
        'scheme':"",
        'sp_scheme_host':"://",
        'host':"",
        'sp_host_port':":",
        'port':{
            'explicit':"",
            'implicit':""
        },
        'netloc':"",
        'sp_netloc_path':"/",
        'path':"",
        'sp_path_params':";",
        'params':"",
        'params_dict':{},
        'sp_params_query':"?",
        'query':"",
        'query_dict':{},
        'sp_query_fragment':"#",
        'fragment':"",
        'fragment_dict':{},
        'hash':"",
        'hash_dict':{}
    }
    url_dict_template['scheme'] = url_dict['scheme']
    if('sp_scheme_host' in url_dict):
        url_dict_template['sp_scheme_host'] = url_dict['sp_scheme_host']
    if('sp_host_port' in url_dict):
        url_dict_template['sp_host_port'] = url_dict['sp_host_port']
    if('sp_netloc_path' in url_dict):
        url_dict_template['sp_netloc_path'] = url_dict['sp_netloc_path']
    if('sp_path_params' in url_dict):
        url_dict_template['sp_path_params'] = url_dict['sp_path_params']
    if('sp_params_query' in url_dict):
        url_dict_template['sp_params_query'] = url_dict['sp_params_query']
    if('sp_query_fragment' in url_dict):
        url_dict_template['sp_query_fragment'] = url_dict['sp_query_fragment']
    if('netloc' in url_dict):
        url_dict_template['netloc'] = url_dict['netloc']
    elif('host' in url_dict):
        if('port' in url_dict):
            url_dict_template['netloc'] = ''.join((url_dict['host'],url_dict['sp_host_port'],url_dict['port']['explicit']))
        else:
            url_dict_template['netloc'] = url_dict['port']['explicit']
            if(url_dict_template['scheme'] == 'https'):
                url_dict_template['port']['implicit'] = "443"
            elif(url_dict_template['scheme'] == 'http'):
                url_dict_template['port']['implicit'] = "80"
            else:
                pass
    else:
        pass
    if('path' in url_dict):
        url_dict_template['path'] = url_dict['path']
        sec_1 = ''.join((url_dict_template['scheme'],url_dict_template['sp_scheme_host'],url_dict_template['netloc'],url_dict_template['sp_netloc_path'],url_dict['path']))
    else:
        return(''.join((url_dict_template['scheme'],url_dict_template['sp_scheme_host'],url_dict_template['netloc'])))
    if('params' in url_dict):
        url_dict_template['params'] = url_dict['params'];
    elif('params_dict' in url_dict):
        url_dict_template['params_dict'] = url_dict['params_dict'];
        url_dict_template['params'] = params_dict_urlencode(url_dict['params_dict']);
    else:
        pass
    if(url_dict_template['params']==""):
        sec_2 = sec_1;
    else:
        sec_2 = ''.join((url_dict_template['sp_path_params'],sec_1))
    if('query' in url_dict):
        url_dict_template['query'] = url_dict['query']
        sec_3 = ''.join((sec_2,url_dict_template['sp_params_query'],url_dict_template['query']))
    elif('query_dict' in url_dict):
        url_dict_template['query_dict'] = url_dict['query_dict']
        url_dict_template['query'] = params_dict_urlencode(url_dict['query_dict'],sp="&")
        sec_3 = ''.join((sec_2,url_dict_template['sp_params_query'],url_dict_template['query']))
    else:
        return(sec_2)
    if('fragment' in url_dict):
        url_dict_template['fragment'] = url_dict['fragment']
        sec_4 = ''.join((sec_3,url_dict_template['sp_query_fragment'],url_dict_template['fragment']))
        return(sec_4)
    elif('fragment_dict' in url_dict):
        url_dict_template['fragment_dict'] = url_dict['fragment_dict']
        url_dict_template['fragment'] = params_dict_urlencode(url_dict['fragment_dict'],sp="&")
        sec_4 = ''.join((sec_3,url_dict_template['sp_query_fragment'],url_dict_template['fragment']))
        return(sec_4)
    else:
        if('hash' in url_dict):
            url_dict_template['hash'] = url_dict['hash']
            sec_4 = ''.join((sec_3,url_dict_template['sp_query_fragment'],url_dict_template['hash']))
            return(sec_4)
        elif('hash_dict' in url_dict):
            url_dict_template['hash_dict'] = url_dict['hash_dict']
            url_dict_template['fragment'] = params_dict_urlencode(url_dict['hash_dict'],sp="&")
            sec_4 = ''.join((sec_3,url_dict_template['sp_query_fragment'],url_dict_template['fragment']))
            return(sec_4)
        else:
            return(sec_3)


def params_to_params_dict(params_str):
    eles = params_str.split(";")
    eles_len = eles.__len__()
    r1 = {}
    for i in range(0,eles_len):
        kv = eles[i]
        if("=" in kv):
            kv_arr = kv.split("=")
            k=kv_arr[0]
            v=kv_arr[1]
            k=urllib.parse.unquote(k)
            v=urllib.parse.unquote(v)
            r1[k] = v
        else:
            k = kv
            v = {}
            k=urllib.parse.unquote(k)
            r1[k] = v
    return(r1)

def params_dict_urlencode(decoded_dict,sp=";"):
    eles = decoded_dict
    eles_len = eles.__len__()
    r1_dict = {}
    r2_str = ""
    for k in eles:
        if(type(eles[k]) == type({})):
            r2_str = ''.join((r2_str,sp,k))
        else:
            r1_dict[k] = eles[k]
    rslt_str = urllib.parse.urlencode(r1_dict)
    rslt_str = ''.join((rslt_str,r2_str))
    rslt_str = rslt_str.lstrip(sp)
    rslt_str = rslt_str.replace("&",sp)
    return(rslt_str)
    

def urldecode(encoded_str,**kwargs):
    if('quote_plus' in kwargs):
        quote_plus=kwargs['quote_plus']
    else:
        quote_plus=True
    if('sp' in kwargs):
        sp=kwargs['sp']
    else:
        sp="&"
    eles = encoded_str.split(sp)
    eles_len = eles.__len__()
    r1 = {}
    ####improvement for value such as 'SourceUrl=//xyz/query.aspx?ID=000001'
    regex = re.compile('(.*?)=(.*)')
    for i in range(0,eles_len):
        kv = eles[i]
        if("=" in kv):
            ####improvement for value such as 'SourceUrl=//xyz/query.aspx?ID=000001'
            m = regex.search(kv)
            #kv_arr = kv.split("=")
            #k=kv_arr[0]
            #v=kv_arr[1]
            k = m.group(1)
            v = m.group(2)
            ###################
            if(quote_plus):
                k=urllib.parse.unquote_plus(k)
                v=urllib.parse.unquote_plus(v)
            else:
                k=urllib.parse.unquote(k)
                v=urllib.parse.unquote(v)     
            r1[k] = v
        else:
            k = kv
            v = {}
            if(quote_plus):
                k=urllib.parse.unquote_plus(k)
            else:
                k=urllib.parse.unquote(k)
            r1[k] = v
    return(r1)


def urldecode_half_ordered(encoded_str,**kwargs):
    if('quote_plus' in kwargs):
        quote_plus=kwargs['quote_plus']
    else:
        quote_plus=True
    if('sp' in kwargs):
        sp=kwargs['sp']
    else:
        sp="&"
    eles = encoded_str.split(sp)
    eles_len = eles.__len__()
    r1 = []
    regex = re.compile('(.*?)=(.*)')
    for i in range(0,eles_len):
        kv = eles[i]
        if("=" in kv):
            #kv_arr = kv.split("=")
            #k=kv_arr[0]
            #v=kv_arr[1]
            ####improvement for value such as 'SourceUrl=//xyz/query.aspx?ID=000001'
            m = regex.search(kv)
            k = m.group(1)
            v = m.group(2)
            ###################
            if(quote_plus):
                k=urllib.parse.unquote_plus(k)
                v=urllib.parse.unquote_plus(v)
            else:
                k=urllib.parse.unquote(k)
                v=urllib.parse.unquote(v)
            r1.append({k:v})
        else:
            k = kv
            v = ""
            if(quote_plus):
                k=urllib.parse.unquote_plus(k)
            else:
                k=urllib.parse.unquote(k)
            r1.append({k:v})
    return(r1)




def urldecode_ordered(encoded_str,**kwargs):
    if('quote_plus' in kwargs):
        quote_plus=kwargs['quote_plus']
    else:
        quote_plus=True
    if('sp' in kwargs):
        sp=kwargs['sp']
    else:
        sp="&"
    eles = encoded_str.split(sp)
    eles_len = eles.__len__()
    r1 = []
    regex = re.compile('(.*?)=(.*)')
    for i in range(0,eles_len):
        kv = eles[i]
        if("=" in kv):
            ####improvement for value such as 'SourceUrl=//xyz/query.aspx?ID=000001'
            m = regex.search(kv)
            #kv_arr = kv.split("=")
            #k=kv_arr[0]
            #v=kv_arr[1]
            k = m.group(1)
            v = m.group(2)
            ###################
            if(quote_plus):
                k=urllib.parse.unquote_plus(k)
                v=urllib.parse.unquote_plus(v)
            else:
                k=urllib.parse.unquote(k)
                v=urllib.parse.unquote(v)
            r1.append((k,v))
        else:
            k = kv
            v = ""
            if(quote_plus):
                k=urllib.parse.unquote_plus(k)
            else:
                k=urllib.parse.unquote(k)
            r1.append((k,v))
    return(r1)




def urlencode(decoded_dict,**kwargs):
    if('quote_plus' in kwargs):
        quote_plus=kwargs['quote_plus']
    else:
        quote_plus=True
    if('sp' in kwargs):
        sp=kwargs['sp']
    else:
        sp="&"
    eles = decoded_dict
    eles_len = eles.__len__()
    r1_dict = {}
    r2_str = ""
    for k in eles:
        if(type(eles[k]) == type({})):
            r2_str = ''.join((r2_str,sp,k))
        else:
            r1_dict[k] = eles[k]
    rslt_str = urllib.parse.urlencode(r1_dict)
    rslt_str = ''.join((rslt_str,r2_str))
    rslt_str = rslt_str.lstrip(sp)
    rslt_str = rslt_str.replace("&",sp)
    if(quote_plus):
        pass
    else:
        rslt_str = rslt_str.replace("+","%20")
    return(rslt_str)
 


def urlencode_half_ordered(decoded_dict_list,**kwargs):
    if('quote_plus' in kwargs):
        quote_plus=kwargs['quote_plus']
    else:
        quote_plus=True
    if('sp' in kwargs):
        sp=kwargs['sp']
    else:
        sp="&"
    eles = decoded_dict_list
    eles_len = eles.__len__()
    rslt_str = ""
    for i in range(0,eles.__len__()):
        r1_dict = eles[i]
        k = list(r1_dict.keys())[0]
        v = list(r1_dict.values())[0]
        if(v == {}):
            rslt_str = ''.join((rslt_str,sp,k))
        else:
            tmp = urllib.parse.urlencode(r1_dict)
            rslt_str = rslt_str+sp+tmp
    rslt_str = rslt_str.lstrip(sp)
    rslt_str = rslt_str.replace("&",sp)
    if(quote_plus):
        pass
    else:
        rslt_str = rslt_str.replace("+","%20")
    return(rslt_str)


def urlencode_ordered(decoded_tuple_list,**kwargs):
    if('quote_plus' in kwargs):
        quote_plus=kwargs['quote_plus']
    else:
        quote_plus=True
    if('sp' in kwargs):
        sp=kwargs['sp']
    else:
        sp="&"
    eles = decoded_tuple_list
    eles_len = eles.__len__()
    rslt_str = ""
    for i in range(0,eles.__len__()):
        kv = eles[i]
        k = kv[0]
        v = kv[1]
        if(v == {}):
            rslt_str = ''.join((rslt_str,sp,k))
        else:
            tmp = urllib.parse.urlencode({k:v})
            rslt_str = rslt_str+sp+tmp
    rslt_str = rslt_str.lstrip(sp)
    rslt_str = rslt_str.replace("&",sp)
    if(quote_plus):
        pass
    else:
        rslt_str = rslt_str.replace("+","%20")
    return(rslt_str)

######
######六元组
######(scheme, netloc, path, params, query, fragment)
#####
def six_tn():
    return(['scheme', 'netloc', 'path', 'params', 'query', 'fragment'])

def six_md():
    md = {
        'path': 2,
        'netloc': 1,
        'fragment': 5,
        'params': 3,
        'scheme': 0,
        'query': 4,
        0:'scheme',
        1:'netloc',
        2:'path',
        3:'params',
        4:'query',
        5:'fragment'
    }
    return(md)



def six_u2d(url):
    '''
        url = 'http://www.baidu.com/index.php;params?username=query#frag'
        pobj(six_u2d(url))
    '''
    d = {}
    rslt = urllib.parse.urlparse(url)
    for k in rslt._fields:
        d[k] = rslt.__getattribute__(k)
    return(d)

def six_u2t(url):
    '''
        url = 'http://www.baidu.com/index.php;params?username=query#frag'
        pobj(six_u2t(url))
    '''
    rslt = urllib.parse.urlparse(url)
    t = (rslt.scheme,rslt.netloc,rslt.path,rslt.params,rslt.query,rslt.fragment)
    return(t)

def six_d2t(d):
    '''
        d = {
            'path': '/index.php',
            'netloc': 'www.baidu.com',
            'fragment': 'frag',
            'params': 'params',
            'scheme': 'http',
            'query': 'username=query'
        }
        t = six_d2t(d)
        pobj(t)
    '''
    t = (d['scheme'],d['netloc'],d['path'],d['params'],d['query'],d['fragment'])
    return(t)
    

def six_d2u(d):
    '''
        d = {
            'path': '/index.php',
            'netloc': 'www.baidu.com',
            'fragment': 'frag',
            'params': 'params',
            'scheme': 'http',
            'query': 'username=query'
        }
        url = six_d2u(d)
        url
    '''
    t = six_d2t(d)
    url = urllib.parse.urlunparse(t)
    return(url)

def six_t2d(t):
    '''
        t = ('http', 'www.baidu.com', '/index.php', 'params', 'username=query', 'frag')
        pobj(six_t2d(t))
    '''
    d = {}
    d['scheme'] = t[0]
    d['netloc'] = t[1]
    d['path'] = t[2]
    d['params'] = t[3]
    d['query'] = t[4]
    d['fragment'] = t[5]
    return(d)

def six_t2u(t):
    '''
    '''
    url = urllib.parse.urlunparse(t)
    return(url)

def six_set(url,**kwargs):
    '''
    '''
    tn = six_tn()
    d = six_u2d(url)
    for k in kwargs:
        rk = str.lower(k)
        cond = (rk in tn)
        if(cond):
            d[rk] = kwargs[k]
        else:
            pass
    url = six_d2u(d)
    return(url)
    



def get_abs_url(rel_url,**kwargs):
    '''
        purl =  "http://www.example.com/index.html"
        rel_url = "../zzz/checker.jsp" 
        base = "http://localhost:8080/mysite/xxx/login.jsp"
        
    '''
    #base = kwargs['base']
    #origin = get_origin(base)
    ####
    rel = urllib.parse.urlparse(rel_url)
    scheme = rel.scheme
    netloc = rel.netloc
    path = rel.path
    ####
    if(scheme == ''):
        base = kwargs['base']
        origin = get_origin(base)
        if(path == ''):
            abs_url = os.path.split(base)[0] + '/' + rel_url 
        elif(path[0] == '/'):
            abs_url = origin + rel_url
        elif(path[:2] == './'):
            rel_url = six_set(rel_url,path = path[2:])
            abs_url = os.path.split(base)[0] + '/' + rel_url
        elif(path[:3] == '../'):
            parent = os.path.split(base)[0]
            pp = os.path.split(parent)[0]
            rel_url = six_set(rel_url,path = path[3:])
            abs_url = pp + '/' + rel_url
        else:
            # 这种情况
            # 对于没以'/'结尾的情况
            cond = (base[-1] == '/')
            if(cond):
                abs_url = base  + rel_url
            else:
                abs_url = base + '/' + rel_url
        return(abs_url)
    else:
        return(rel_url) 




#https://onlineservices.immigration.govt.nz/PaymentGateway/OnLinePayment.aspx?ProductId=2&SourceUrl=%2f%2fonlineservices.immigration.govt.nz%2fWorkingHoliday%2fApplication%2fSubmitConfirmation.aspx%3fApplicationId%3d2057863&Token=LctQ9Y5g+5WanrJmA6S2WQ9VQMsvtIpCztSVdx4wiJkIiGx7DUL%2f2wipo5426qG0YTDq+nd8AwM%3d
# https://onlineservices.immigration.govt.nz/PaymentGateway/OnLinePayment.aspx?ProductId=2&SourceUrl=//onlineservices.immigration.govt.nz/WorkingHoliday/Application/SubmitConfirmation.aspx?ApplicationId=2057863&Token=LctQ9Y5g%205WanrJmA6S2WQ9VQMsvtIpCztSVdx4wiJkIiGx7DUL/2wipo5426qG0YTDq%20nd8AwM=
# 如果query里有url 先分离后quote
# uqurl = urllib.parse.unquote(url)
# head = nvurl.trim_after_path(uqurl)
# query = urllib.parse.urlparse(uqurl).query
# d = nvurl.urldecode(query)
# d['ProductId'] = urllib.parse.quote_plus(d['ProductId'])
# d['SourceUrl'] = urllib.parse.quote_plus(d['SourceUrl'])
# d['Token'] = urllib.parse.quote_plus(d['Token'])
# query_url = 'ProductId='+d['ProductId']+'&'+ 'SourceUrl=' + d['SourceUrl'] +'&' +'Token=' + d['Token']



def quote_plus_chinese_url(href):
    href = urllib.parse.quote_plus(href,":/?=;#")
    return(href)


def quote_chinese_url(href):
    href = urllib.parse.quote(href,":/?=;#")
    return(href)




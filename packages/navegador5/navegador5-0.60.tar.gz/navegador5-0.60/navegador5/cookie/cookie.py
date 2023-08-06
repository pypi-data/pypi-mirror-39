import re
import urllib.parse
from navegador5 import js_random
from navegador5 import html_tool
from navegador5 import head
from navegador5 import url_tool
import html
import http.cookiejar
import http.cookies


def get_cookie_for_next_req(info_container,next_url):
    req_head = info_container['req_head']
    resp_head = info_container['resp_head']
    from_url = info_container['url']
    to_url = next_url
    req_head = info_container['req_head']
    resp_head = info_container['resp_head']
    next_req_cookie_dict = select_valid_cookies_from_resp(req_head,resp_head,from_url,to_url)
    next_req_cookie_str = cookie_dict_to_str(next_req_cookie_dict,with_head=0)
    return(next_req_cookie_str)


def update_cookie_for_next_req(info_container,next_req_cookie_str):
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









def add_cookie_str_to_cookie_str(orig,new):
    return((orig+'; '+new).lstrip(';').strip(' '))

def add_cookie_dict_to_cookie_str(orig,ckd):
    new = cookie_dict_to_str(ckd,with_head=0)
    return((orig+'; '+new).lstrip(';').strip(' '))

def add_cookie_to_req_head(req_head,ck):
    if('Cookie' in req_head):
        pass
    else:
        req_head['Cookie'] = ""
    if(type(ck) == type("")):
        req_head['Cookie'] = add_cookie_str_to_cookie_str(req_head['Cookie'],ck)
    else:
        req_head['Cookie'] = add_cookie_dict_to_cookie_str(req_head['Cookie'],ck)
    return(req_head)


#
def replace_cookie_with_cookie_str(ck_str_1,ck_str_2):
    cktl1 = cookie_str_to_tuple_list(ck_str_1)
    cktl2 = cookie_str_to_tuple_list(ck_str_2)
    for i in  range(0,cktl1.__len__()):
        name = cktl[i][0]
        for j in  range(0,cktl2.__len__()):
            if(name == cktl2[j][0]):
                cktl[i][1] = cktl2[j][1]
            else:
                pass   
    return(cookie_tuple_list_to_str(cktl1,with_head=0))




def delete_cookie_via_name_from_cookie_str(ck_str,name,howmany=2**32):
    ntl = []
    cktl = cookie_str_to_tuple_list(ck_str)
    count = 0
    for i in  range(0,cktl.__len__()):
        if(name == cktl[i][0]):
            if(count<howmany):
                count = count + 1
            else:
                break
        else:
            ntl.append(cktl[i])
    for j in range(i+1,cktl.__len__()):
        ntl.append(cktl[j])
    return(cookie_tuple_list_to_str(ntl,with_head=0))


def delete_cookie_via_value_from_cookie_str(ck_str,value,howmany=2**32):
    ntl = []
    cktl = cookie_str_to_tuple_list(ck_str)
    count = 0
    for i in  range(0,cktl.__len__()):
        if(value == cktl[i][1]):
            if(count<howmany):
                count = count + 1
            else:
                break
        else:
            ntl.append(cktl[i])
    for j in range(i+1,cktl.__len__()):
        ntl.append(cktl[j])
    return(cookie_tuple_list_to_str(ntl,with_head=0))



def delete_cookie_via_nameandvalue_from_cookie_str(ck_str,name,value,howmany=2**32):
    ntl = []
    cktl = cookie_str_to_tuple_list(ck_str)
    count = 0
    for i in  range(0,cktl.__len__()):
        if((value == cktl[i][1])&(name == cktl[i][0])):
            if(count<howmany):
                count = count + 1
            else:
                break
        else:
            ntl.append(cktl[i])
    for j in range(i+1,cktl.__len__()):
        ntl.append(cktl[j])
    return(cookie_tuple_list_to_str(ntl,with_head=0))



def delete_cookie_via_nameorvalue_from_cookie_str(ck_str,name,value,howmany=2**32):
    ntl = []
    cktl = cookie_str_to_tuple_list(ck_str)
    count = 0
    for i in  range(0,cktl.__len__()):
        if((value == cktl[i][1])|(name == cktl[i][0])):
            if(count<howmany):
                count = count + 1
            else:
                break
        else:
            ntl.append(cktl[i])
    for j in range(i+1,cktl.__len__()):
        ntl.append(cktl[j])
    return(cookie_tuple_list_to_str(ntl,with_head=0))





def in_ignoreUpper(lora,key):
    for each in lora:
        if(key.lower() == each.lower()):
            return((True,each))
        else:
            pass
    return((False,None))
    

def get_cookie_eles_from_cookie_str(cookie_str):
    cookie_str = cookie_str.replace("Cookie: ","")
    eles = cookie_str.split('; ')
    return(eles)

def cookie_str_to_dict(cookie_str):
    cookie_dict = {}
    eles = cookie_str.split("; ")
    eles_len = eles.__len__()
    regex = re.compile("(.*?)=(.*)")
    for i in range(0,eles_len):
        m = regex.search(eles[i])
        if(m):
            k=m.group(1)
            v=m.group(2)
            cookie_dict[k] = v
    return(cookie_dict)
    

def cookie_dict_to_str(cookie_dict,with_head=1):
    if(with_head):
        cookie_str ='Cookie: '
    else:
        cookie_str =''
    for key in cookie_dict:
        cookie_str = ''.join((cookie_str,key,'=',cookie_dict[key],'; '))
    cookie_str = cookie_str.rstrip(' ')
    cookie_str = cookie_str.rstrip(';')
    return(cookie_str)



def cookie_str_to_tuple_list(cookie_str):
    cookie_tuple_list = []
    eles = cookie_str.split("; ")
    eles_len = eles.__len__()
    regex = re.compile("(.*?)=(.*)")
    for i in range(0,eles_len):
        m = regex.search(eles[i])
        if(m):
            k=m.group(1)
            v=m.group(2)
            cookie_tuple_list.append((k,v))
    return(cookie_tuple_list)


def cookie_tuple_list_to_str(cookie_tuple_list,with_head=1):
    if(with_head):
        cookie_str ='Cookie: '
    else:
        cookie_str =''
    for i in range(0,cookie_tuple_list.__len__()):
        kv = cookie_tuple_list[i]
        cookie_str = ''.join((cookie_str,kv[0],'=',kv[1],'; '))
    cookie_str = cookie_str.rstrip(' ')
    cookie_str = cookie_str.rstrip(';')
    return(cookie_str)


def cookie_to_further_dict(ck):
    if(type(ck) == type({})):
        cookie_dict = ck
    elif(type(ck) == type('')):
        cookie_dict = head.decode_one_http_head('Cookie',';',ck,ordered=0)
    else:
        pass
    further = {}
    for key in cookie_dict:
        if(key == ' '):
            pass
        else:
            value = url_tool.urldecode(cookie_dict[key])
            further[key] = value
    return(further)

#
def further_cookie_dict_to_str(further_cookie_dict,with_head=1):
    if(with_head):
        cookie_str ='Cookie: '
    else:
        cookie_str =''
    for key in cookie_dict:
        value = cookie_dict[key]
        if(type(value) == type({})):
            temp = ''
            for k in value:
                v = url_tool.urlencode(value[k])
                temp = ''.join((temp,k,'=',v,'; '))
            temp = temp.rstrip(' ')
            temp = temp.rstrip(';')
            cookie_str = ''.join((cookie_str,key,'=',temp,'; '))
        else:
            cookie_str = ''.join((cookie_str,key,'=',value,'; '))
    cookie_str = cookie_str.rstrip(' ')
    cookie_str = cookie_str.rstrip(';')
    return(cookie_str)
#
    
    
def key_in_arr_cookies(key,arr_cookies):
    ptrn = ''.join((key,"="))
    arr_cookies_len = arr_cookies.__len__()
    for i in range(0,arr_cookies_len):
        if(ptrn in arr_cookies[i][1]):
            return(1)
    return(0)
    



    
    

def which_time_format(date_value):
    '''
        ####################HTTP-date###############
        # HTTP-date    = rfc1123-date | rfc850-date | asctime-date
               # rfc1123-date = wkday "," SP date1 SP time SP "GMT"
               # rfc850-date  = weekday "," SP date2 SP time SP "GMT"
               # asctime-date = wkday SP date3 SP time SP 4DIGIT
               # date1        = 2DIGIT SP month SP 4DIGIT
                              # ; day month year (e.g., 02 Jun 1982)
               # date2        = 2DIGIT "-" month "-" 2DIGIT
                              # ; day-month-year (e.g., 02-Jun-82)
               # date3        = month SP ( 2DIGIT | ( SP 1DIGIT ))
                              # ; month day (e.g., Jun  2)
               # time         = 2DIGIT ":" 2DIGIT ":" 2DIGIT
                              # ; 00:00:00 - 23:59:59
               # wkday        = "Mon" | "Tue" | "Wed"
                            # | "Thu" | "Fri" | "Sat" | "Sun"
               # weekday      = "Monday" | "Tuesday" | "Wednesday"
                            # | "Thursday" | "Friday" | "Saturday" | "Sunday"
    '''
    month = 'Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec'
    weekday = 'Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday'
    wkday = 'Mon|Tue|Wed|Thu|Fri|Sat|Sun'
    rfc1123 = ''.join(("(",wkday,")",", ","[0-9]{2} ","(",month,")"," [0-9]{4} ","[0-9]{2}:[0-9]{2}:[0-9]{2} ","GMT"))
    regex_rfc1123 = re.compile(rfc1123)
    rfc1123_hypen = ''.join(("(",wkday,")",", ","[0-9]{2}-","(",month,")","-[0-9]{4} ","[0-9]{2}:[0-9]{2}:[0-9]{2} ","GMT"))
    regex_rfc1123_hypen = re.compile(rfc1123_hypen)
    rfc850 = ''.join(("(",weekday,")",", ","[0-9]{2}-","(",month,")","-[0-9]{2} ","[0-9]{2}:[0-9]{2}:[0-9]{2} ","GMT"))
    regex_rfc850 = re.compile(rfc850)
    rfc850_a = ''.join(("(",wkday,")",", ","[0-9]{2}-","(",month,")","-[0-9]{2} ","[0-9]{2}:[0-9]{2}:[0-9]{2} ","GMT"))
    regex_rfc850_a = re.compile(rfc850_a)
    asctime = ''.join(("(",wkday,")"," ","(",month,")","(( [0-9]{2})|(  [0-9]{1}))"," ","[0-9]{2}:[0-9]{2}:[0-9]{2} ","[0-9]{4}"))
    regex_asctime = re.compile(asctime)
    if(regex_rfc1123.search(date_value)):
        return('rfc1123_date')
    elif(regex_rfc1123_hypen.search(date_value)):
        return('rfc1123_hypen_date')
    elif(regex_rfc850.search(date_value)):
        return('rfc850_date')
    elif(regex_rfc850_a.search(date_value)):
        return('rfc850_date_a')
    elif(regex_asctime.search(date_value)):
        return('asctime_date')
    else:
        return(None)


def set_rt_cookie(url):
    r=re.sub("#.*","",url)
    r=urllib.parse.quote(url)
    r=r.replace("/","%2F")
    n=js_random.js_clock_seconds(13)
    rslt = ''.join(("r=",str(r),"&","s=",str(n)))
    return(rslt)

def get_cookies_array(headers):
    #previous get_Cookie
    Cookies = []
    for each in headers:
        if(each[0]=='Set-Cookie'):
            Cookies.append(each[1])
    return(Cookies)




    
def extract_one_cookie_to_tuple(Set_Cookie,head ='Set-Cookie: '):
    if(head in Set_Cookie):
        regex = re.compile(''.join((head,'(.*)')))
        m = regex.search(Set_Cookie)
        Set_Cookie = m.group(1)
    else:
        Set_Cookie = Set_Cookie.strip(' ')
    CK = Set_Cookie.split(';')
    regex_CK_attr = re.compile('Max-Age|Expires|Domain|Path|Secure|HttpOnly',re.I)
    len = CK.__len__()
    regex_NV = re.compile('(.*?)=(.*)')
    for i in range(0,len):
        m = regex_NV.search(CK[i])
        if(m==None):
            N = CK[i]
            V = ''
        else:
            N = m.group(1)
            V = m.group(2)
        if(regex_CK_attr.search(N)):
            pass
        else:
            return((N,V))

def creat_cookie_from_cookie_nv_tuple_list(Set_Cookies):
    NV_list = []
    for each in Set_Cookies:
        NV_list.append(extract_one_cookie_to_tuple(each))
    CK_header = 'Cookie: '
    for each in NV_list:
        NV_str = '{0}={1}; '.format(each[0],each[1])
        CK_header = ''.join((CK_header,NV_str))
    return(CK_header.rstrip(' ').rstrip(';'))


def extract_one_cookie_to_tuple_enhanced(Set_Cookie,head ='Set-Cookie: '):
    if(head in Set_Cookie):
        regex = re.compile(''.join((head,'(.*)')))
        m = regex.search(Set_Cookie)
        Set_Cookie = m.group(1)
    else:
        Set_Cookie = Set_Cookie.strip(' ')
    Set_Cookie = html_tool.convert_token_in_quote(Set_Cookie,colons=['='])
    CK = Set_Cookie.split(';')
    regex_CK_attr = re.compile('Max-Age|Expires|Domain|Path|Secure|HttpOnly',re.I)
    len = CK.__len__()
    regex_NV = re.compile('(.*?)=(.*)')
    for i in range(0,len):
        m = regex_NV.search(CK[i])
        if(m==None):
            N = CK[i]
            V = ''
        else:
            N = m.group(1)
            V = m.group(2)
        if(regex_CK_attr.search(N)):
            pass
        else:
            return((html.unescape(N),html.unescape(V)))

def creat_cookie_from_cookie_nv_tuple_list_enhanced(Set_Cookies):
    NV_list = []
    for each in Set_Cookies:
        NV_list.append(extract_one_cookie_to_tuple_enhanced(each))
    CK_header = 'Cookie: '
    for each in NV_list:
        NV_str = '{0}={1}; '.format(each[0],each[1])
        CK_header = ''.join((CK_header,NV_str))
    return(CK_header.rstrip(' ').rstrip(';'))



def decode_resp_set_cookie(set_cookie_tuple):
    rslt = {}
    set_cookie_len = set_cookie_tuple.__len__()
    rslt['type'] =  set_cookie_tuple[0]
    content = set_cookie_tuple[1]
    #for bug such as:('Set-Cookie', 'AWSELB=6BA385EF167F548755DA9475B5E2E58BE6A3496C1BD0B6C4814ACBD32A4C1C7D2E3AF5509C04AF1EB435D54130EA28AA464A1B0116C7C86B6A784C164C2DF73816BE62FFED;PATH=/')
    content = content.replace('; ',';');
    content = content.replace(';','; ');
    attrs = content.split('; ')
    regex_ck_attr = re.compile('Max-Age|Expires|Domain|Path|Secure|HttpOnly|Version|Comment|Discard|CommentURL',re.I)
    regex_kv = re.compile('(.*)=(.*)')
    for i in range(0,attrs.__len__()):
        kv = attrs[i]
        m_ck_attr = regex_ck_attr.search(kv)
        m_kv = regex_kv.search(kv)
        if(m_ck_attr==None):
            rslt['Cookie'] = kv
        else:
            if(m_kv == None):
                key = kv
                value = ''
            else:
                key = m_kv.group(1)
                value = m_kv.group(2)
            rslt[key] = value
    return(rslt)

def http_cookie_expired(expire):
    #python if not implement tzinfo or use pytz module, the timezone info will not be calculated
    now = datetime.datetime.now()
    now = time.mktime(now.timetuple())
    utcnow = datetime.datetime.utcnow()
    utcnow = time.mktime(utcnow.timetuple())
    diff = utcnow - now
    wtf = which_time_format(expire)
    if(wtf == "rfc1123_date"):
        expire =  time.strptime(expire, '%a, %d %b %Y %H:%M:%S %Z')
    elif(wtf == "rfc1123_hypen_date"):
        expire =  time.strptime(expire, '%a, %d-%b-%Y %H:%M:%S %Z')
    elif(wtf == "rfc850_date"):
        expire =  time.strptime(expire, '%A, %d-%b-%y %H:%M:%S %Z')
    elif(wtf == "rfc850_date_a"):
        expire =  time.strptime(expire, '%a, %d-%b-%y %H:%M:%S %Z')
    expire =  time.mktime(expire)
    expire = expire + diff
    if(utcnow > expire):
        return(1)
    else:
        return(0)


def http_cookie_overdue(cookie_dict):
#4.1.2.2.  The Max-Age Attribute
#   The Max-Age attribute indicates the maximum lifetime of the cookie,   represented as the number of seconds until the cookie expires.  The   user agent is not required to retain the cookie for the specified   duration.  In fact, user agents often evict cookies due to memory   pressure or privacy concerns.

# If a cookie has both the Max-Age and the Expires attribute, the Max-
# Age attribute has precedence and controls the expiration date of the
# cookie.  If a cookie has neither the Max-Age nor the Expires
# attribute, the user agent will retain the cookie until "the current
# session is over" (as defined by the user agent).
    rslt = {}
    rslt['errors'] = []
    cond,key = in_ignoreUpper(cookie_dict,'Max-Age')
    if(cond):
        #not supported full feature
        if(int(cookie_dict[key]) <= 0):
            rslt['errors'].append(key)
    else:
        cond,key = in_ignoreUpper(cookie_dict,'Expires')
        if(cond):
            if(http_cookie_expired(cookie_dict[key])):
                rslt['errors'].append(key)
    if(rslt['errors'].__len__() == 0):
        rslt['valid'] = 1
    else:
        rslt['valid'] = 0
    return(rslt)
    
        
def http_cookie_outof_domain(cookie_dict,**kwargs):
# 4.1.2.3.  The Domain Attribute
    # The Domain attribute specifies those hosts to which the cookie will
    # be sent.  For example, if the value of the Domain attribute is
    # "example.com", the user agent will include the cookie in the Cookie
    # header when making HTTP requests to example.com, www.example.com, and
    # www.corp.example.com.  (Note that a leading %x2E ("."), if present,
    # is ignored even though that character is not permitted, but a
    # trailing %x2E ("."), if present, will cause the user agent to ignore
    # the attribute.)  If the server omits the Domain attribute, the user
    # agent will return the cookie only to the origin server.
    # WARNING: Some existing user agents treat an absent Domain
    # attribute as if the Domain attribute were present and contained
    # the current host name.  For example, if example.com returns a Set-
    # Cookie header without a Domain attribute, these user agents will
    # erroneously send the cookie to www.example.com as well.
    # The user agent will reject cookies unless the Domain attribute
    # specifies a scope for the cookie that would include the origin
    # server.  For example, the user agent will accept a cookie with a
    # Domain attribute of "example.com" or of "foo.example.com" from
    # foo.example.com, but the user agent will not accept a cookie with a
    # Domain attribute of "bar.example.com" or of "baz.foo.example.com".
    # NOTE: For security reasons, many user agents are configured to reject
    # Domain attributes that correspond to "public suffixes".  For example,
    # some user agents will reject Domain attributes of "com" or "co.uk".
    ###
    ### domain must include the netloc of to_url 
    ### in other words, the str of <the netloc of to_url> must include <the str of domain>
    from_url = kwargs['from_url']
    to_url = kwargs['to_url']
    origin_server = urllib.parse.urlparse(from_url).netloc
    to_domain = urllib.parse.urlparse(to_url).netloc
    cond,key = in_ignoreUpper(cookie_dict,'Domain')
    if(cond):
        domain = cookie_dict[key].lstrip('.')
        regex_str = ''.join((domain,'$'))
        regex_domain = re.compile(regex_str)
        if(regex_domain.search(to_domain) == None):
            return(1)
        else:
            return(0)
    else:
        if(origin_server == to_domain):
            return(0)
        else:
            return(1)

            
def http_cookie_outof_path(cookie_dict,**kwargs):
# 4.1.2.4.  The Path Attribute
   # The scope of each cookie is limited to a set of paths, controlled by
   # the Path attribute.  If the server omits the Path attribute, the user
   # agent will use the "directory" of the request-uri’s path component as
   # the default value.  (See Section 5.1.4 for more details.)
   # The user agent will include the cookie in an HTTP request only if the
   # path portion of the request-uri matches (or is a subdirectory of) the
   # cookie’s Path attribute, where the %x2F ("/") character is
   # interpreted as a directory separator.
   # Although seemingly useful for isolating cookies between different
   # paths within a given host, the Path attribute cannot be relied upon
   # for security (see Section 8).
    from_url = kwargs['from_url']
    to_url = kwargs['to_url']
    from_attribs = urllib.parse.urlparse(from_url)
    to_attribs = urllib.parse.urlparse(to_url)
    ####
    #from_scheme = from_attribs.scheme
    #to_scheme = to_attribs.scheme
    #if(from_scheme == to_scheme):
    #    pass
    #else:
    #    return(0)
####
#6.   If the domain-attribute is non-empty:
#           If the canonicalized request-host does not domain-match the           domain-attribute:
#              Ignore the cookie entirely and abort these steps.
#           Otherwise:
#              Set the cookie’s host-only-flag to false.
#              Set the cookie’s domain to the domain-attribute.
#        Otherwise:
#           Set the cookie’s host-only-flag to true.
#           Set the cookie’s domain to the canonicalized request-host.
####
    from_netloc = from_attribs.netloc
    to_netloc = to_attribs.netloc
    cond,key = in_ignoreUpper(cookie_dict,'Domain')
    if(cond):
        domain = cookie_dict[key].replace(' ',"")
        if(domain == ''):
            domain = None
        else:
            pass
    else:
        domain = None
    if(domain):
        regex_str = domain
        regex_str.replace('\\',"\\\\")
        regex_set = {'.','^','$','*','+','?','{','}','[',']','(',')','|'}
        for each in regex_set:
            regex_str = regex_str.replace(each,"\\"+each)
        regex_dom = re.compile(regex_str+'$')
        m = regex_dom.search(to_netloc)
        if(m):
            pass
        else:
            return(0)
    else:
        #host-only-flag
        if(from_netloc == to_netloc):
            pass
        else:
            return(0)
    ####
    from_path = from_attribs.path
    to_path = to_attribs.path
    if(from_path == ''):
        from_path = '/'
    else:
        pass
    if(to_path == ''):
        to_path = '/'
    else:
        pass
    cond,key = in_ignoreUpper(cookie_dict,'Path')
    if(cond):
        path = cookie_dict[key]
    else:
        path = from_path
    if(path == ''):
        path = '/'
    else:
        pass
    regex_str = path
    regex_str = regex_str.replace('\\',"\\\\")
    regex_set = {'.','^','$','*','+','?','{','}','[',']','(',')','|'}
    for each in regex_set:
        regex_str = regex_str.replace(each,"\\"+each)
    regex_str = '^'+regex_str
    regex_path = re.compile(regex_str)
    if(regex_path.search(to_path) == None):
        return(1)
    else:
        return(0)


def split_cookies_via_secure(cookie_dict_arr):
    https_cks = []
    http_cks = []
    for cookie in cookie_dict_arr:
        cond = http_cookie_only_for_https(cookie)
        if(cond):
            https_cks.append(cookie)
        else:
            http_cks.append(cookie)
    return({'http':http_cks,'https':https_cks}) 
 
 

def http_cookie_only_for_https(cookie_dict,**kwargs):
#4.1.2.5.  The Secure Attribute
#   The Secure attribute limits the scope of the cookie to "secure"   channels (where "secure" is defined by the user agent).  When a   cookie has the Secure attribute, the user agent will include the   cookie in an HTTP request only if the request is transmitted over a   secure channel (typically HTTP over Transport Layer Security (TLS)   [RFC2818]).
#   Although seemingly useful for protecting cookies from active network   attackers, the Secure attribute protects only the cookie’s   confidentiality.  An active network attacker can overwrite Secure   cookies from an insecure channel, disrupting their integrity (see   Section 8.6 for more details).
    regex_secure = re.compile("Secure",re.I)
    secure_inside = 0
    for key in cookie_dict:
        if(regex_secure.search(key) == None):
            pass
        else:
            secure_inside = 1
            break
    return(secure_inside)

def http_cookie_not_for_apps(cookie_dict,**kwargs):
    regex_http_only = re.compile("HttpOnly",re.I)
    for key in cookie_dict:
        if(regex_http_only.search(key) == None):
            pass
        else:
            return 1
    return 0
    
    
def is_cookie_valid_for_send(set_cookie_tuple,from_url,to_url):
    cookie_dict = decode_resp_set_cookie(set_cookie_tuple)
    not_overdue = http_cookie_overdue(cookie_dict)['valid']
    in_domain = not(http_cookie_outof_domain(cookie_dict,from_url=from_url,to_url=to_url))
    in_path = not(http_cookie_outof_path(cookie_dict,from_url=from_url,to_url=to_url))
    secure_only = http_cookie_only_for_https(cookie_dict,to_url=to_url)
    url_scheme = urllib.parse.urlparse(to_url).scheme
    if(secure_only):
        if(url_scheme == "https"):
            ok_scheme = 1
        else:
            ok_scheme = 0
    else:
        ok_scheme = 1
    if(not_overdue & in_domain & in_path & ok_scheme):
        return(1)
    else:
        return(0)

def get_cookies_from_resp_head(resp_head,type='Set-Cookie'):
    return(head.select_headers_via_key_from_tuple_list(resp_head,type))


def cookies_tuple_list_to_cookies_dict_list(arr_cookies):
    cks_dl =[]
    arr_cookies_len = arr_cookies.__len__()
    for i in range(0,arr_cookies_len):
        full_cookie_dict = decode_resp_set_cookie(arr_cookies[i])
        cks_dl.append(full_cookie_dict)
    return(cks_dl)




def select_valid_cookies_from_resp(req_head,resp_head,from_url,to_url,return_dict=1):
    if(type(resp_head)==type([])):
        arr = resp_head
    else:
        arr = resp_head
    arr_cookies = head.select_headers_via_key_from_tuple_list(arr,'Set-Cookie')
    arr_cookies_len = arr_cookies.__len__()
    
    if(type(req_head)==type({})):
        if('Cookie' in req_head):
            req_head_ck_str = req_head['Cookie']
            req_head_ck_dict = cookie_str_to_dict(req_head_ck_str)
        else:
            req_head_ck_dict = {}
    else:
        req_head_dict = head.build_headers_dict_from_str(req_head)
        req_head_ck_dict = cookie_str_to_dict(req_head_dict['Cookie'])
    #
    new_ck_dict = {}
    for k in req_head_ck_dict:
        if(key_in_arr_cookies(k,arr_cookies)):
            pass
        else:
            new_ck_dict[k] = req_head_ck_dict[k]
    for i in range(0,arr_cookies_len):
        if(is_cookie_valid_for_send(arr_cookies[i],from_url,to_url)):
            full_cookie_dict = decode_resp_set_cookie(arr_cookies[i])
            cookie_str = full_cookie_dict['Cookie']
            cookie_dict = head.decode_one_http_head('Cookie',';',cookie_str,ordered=0)
            del cookie_dict[' ']
            new_ck_dict.update(cookie_dict)
################################################################
    new_ck_str = cookie_dict_to_str(new_ck_dict)
    if('return_dict'):
        return(new_ck_dict)
    else:
        return(new_ck_str)
    #-----------return str or dict ----------------



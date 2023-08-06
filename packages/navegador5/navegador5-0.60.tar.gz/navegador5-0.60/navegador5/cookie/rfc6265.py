import re
import xdict.time_utils  as xtime
import xdict.fsm as fsm
import xdict.utils as xutils
import urllib.parse
import xdict.dict_list as xdl
import xdict.tuple_list as xtl

#两个正则表达式工具
def _real_dollar(s,m):
    '''$ Matches the end of the string or just before the newline at the end of the string'''
    if(m):
        length_1 = s.__len__()
        length_2 = m.group(0).__len__()
        if(length_1 == length_2):
            return(True)
        else:
            return(False)
    else:
        return(False)

def _creat_regex(unescaped_regex_str,**kwargs):
    '''something like re.escape, with the unescape part prefix and suffix'''
    if("prefix" in kwargs):
        prefix = kwargs['prefix']
    else:
        prefix =""
    if("suffix" in kwargs):
        suffix = kwargs['suffix']
    else:
        suffix =""
    regex_str = re.escape(unescaped_regex_str)
    regex_str = prefix + regex_str + suffix
    regex = re.compile(regex_str,re.DOTALL)
    return(regex)

#===================================

#常用字符串
def CONST_STR_help():
    abbrev = '''
        octs     _all_octets_str
        ckocts   _all_cookie_octets_str
        sps      _all_separators_str
        dels     _all_delimiters_str
        ndigits  _all_non_digits_str
        ndels    _all_non_delimiters_str
        ctls     _all_ctls_str
    '''
    print(abbrev)

def CONST_REGEX_help():
    abbrev = '''
        octs     re.escape _all_octets_str
        ckocts   re.escape _all_cookie_octets_str
        sps      re.escape _all_separators_str
        dels     re.escape _all_delimiters_str
        ndigits  re.escape _all_non_digits_str
        ndels    re.escape _all_non_delimiters_str
        ctls     re.escape _all_ctls_str
    '''
    print(abbrev)

def _all_octets_str():
    '''any 8-bit sequence of data except NUL'''
    octets = ""
    for i in range(1,256):
        octets = octets + chr(i)
    return(octets)

def _all_cookie_octets_str():
    '''
        %x21 / %x23-2B / %x2D-3A / %x3C-5B / %x5D-7E; 
        US-ASCII characters excluding CTLs,
        whitespace DQUOTE, comma, semicolon,
        and backslash 
    '''
    all_cookie_octets_str = "\x21"
    for i in range(0x23,0x2C):
        all_cookie_octets_str = all_cookie_octets_str + chr(i)
    for i in range(0x2D,0x3A):
        all_cookie_octets_str = all_cookie_octets_str + chr(i)
    for i in range(0x3C,0x5C):
        all_cookie_octets_str = all_cookie_octets_str + chr(i)
    for i in range(0x5D,0x7E):
        all_cookie_octets_str = all_cookie_octets_str + chr(i)
    return(all_cookie_octets_str)

def _all_separators_str():
    '''()<>@,;:"/[]?={} \t\\'''
    return('()<>@,;:"/[]?={} \t\\')

def _all_delimiters_str():
    '''delimiter = %x09 / %x20-2F / %x3B-40 / %x5B-60 / %x7B-7E'''
    delimiters = "\x09"
    for i in range(0x20,0x30):
        delimiters = delimiters + chr(i)
    for i in range(0x3B,0x41):
        delimiters = delimiters + chr(i)
    for i in range(0x5B,0x61):
        delimiters = delimiters + chr(i)
    for i in range(0x7B,0x7F):
        delimiters = delimiters + chr(i)
    return(delimiters)

def _all_non_digits_str():
    '''non-digit = %x00-2F / %x3A-FF'''
    nds = ""
    for i in range(0x00,0x30):
        nds = nds + chr(i)
    for i in range(0x3A,0x100):
        nds = nds + chr(i)
    return(nds)

def _all_non_delimiters_str():
    '''non-delimiter   = %x00-08 / %x0A-1F / DIGIT / ":" / ALPHA / %x7F-FF'''
    ndels = ":"
    for i in range(0x00,0x09):
        ndels = ndels + chr(i)
    for i in range(0x0A,0x20):
        ndels = ndels + chr(i)
    for i in range(0,10):
        ndels = ndels + str(i)
    for i in range(97,123):
        ndels = ndels + chr(i)
    for i in range(65,91):
        ndels = ndels + chr(i)
    for i in range(0x7F,0x100):
        ndels = ndels + chr(i)
    return(ndels)

def _all_ctls_str():
    ctrls =""
    for i in range(0,32):
        ctrls = ctrls + chr(i)
    ctrls = ctrls + "\x7f"
    return(ctrls)

CONST_STR = {
    'octs':_all_octets_str(),
    'ckocts':_all_cookie_octets_str(),
    'sps':_all_separators_str(),
    'dels':_all_delimiters_str(),
    'ndigits':_all_non_digits_str(),
    'ndels':_all_non_delimiters_str(),
    'ctls':_all_ctls_str()
}
#===============================================


#用于正则表达式的常用字符串
CONST_REGEX = {
    'octs':re.escape(CONST_STR['octs']),
    'ckocts':re.escape(CONST_STR['ckocts']),
    'sps':re.escape(CONST_STR['sps']),
    'dels':re.escape(CONST_STR['dels']),
    'ndigits':re.escape(CONST_STR['ndigits']),
    'ndels':re.escape(CONST_STR['ndels']),
    'ctls':re.escape(CONST_STR['ctls'])
}

#===============================================



#判断类型 
def _isNUL(c):
    '''null octet'''
    return(c=='\x00')

def _isOCTET(c):
    '''any 8-bit sequence of data except NUL'''
    regex_str = CONST_STR['octs']
    prefix = "^[" 
    suffix = "]$"
    regex = _creat_regex(regex_str,prefix=prefix,suffix=suffix)
    m=regex.search(c)
    return(bool(_real_dollar(c,m)))

def _isWSP(c):
    '''whitespace'''
    return(c=='\x20')

def _isOWS(s):
    '''
        *( [ obs-fold ] WSP )
    '''
    regex = re.compile("^((\r\n)? )*$")
    m=regex.search(s)
    return(bool(_real_dollar(s,m)))

def _is_obs_fold(cc):
    '''CRLF'''
    return(cc=='\r\n')

def _is_cookie_octet(c):
    '''
        %x21 / %x23-2B / %x2D-3A / %x3C-5B / %x5D-7E; 
        US-ASCII characters excluding CTLs,
        whitespace DQUOTE, comma, semicolon,
        and backslash 
    '''
    regex_str = CONST_STR['ckocts']
    prefix = "^[" 
    suffix = "]$"
    regex = _creat_regex(regex_str,prefix=prefix,suffix=suffix)
    m=regex.search(c)
    return(bool(_real_dollar(s,m)))

def _is_cookie_value(s):
    '''*cookie-octet / ( DQUOTE *cookie-octet DQUOTE )'''
    regex_str = CONST_STR['ckocts']
    prefix = "^[" 
    suffix = "]*$"
    regex1 = _creat_regex(regex_str,prefix=prefix,suffix=suffix)
    m1=regex1.search(s)
    regex_str = CONST_STR['ckocts']
    prefix = "^\"[" 
    suffix = "]*\"$"
    regex2 = _creat_regex(regex_str,prefix=prefix,suffix=suffix)
    m2=regex2.search(s)
    rslt = (bool(_real_dollar(s,m1))) | (bool(_real_dollar(s,m2)))
    return(rslt)

def _is_separators(c):
    '''
        HT = "\t"
        separators= 
            "(" | ")" | "<" | ">" | "@"| "," |
            ";" | ":" | "\" | <">| "/" | "[" |
            "]" | "?" | "=" | "{" | "}" | SP |
            HT 
    '''
    regex = re.compile("^[\(\)<>@,;:\\\\\"/\[\]\?=\{\} \t]$")
    m=regex.search(c)
    return(bool(_real_dollar(c,m)))

def _is_token(s):
    '''1*<any CHAR except CTLs or separators> '''
    regex_ctls_str = CONST_STR['ctls']
    regex_separators_str = CONST_STR['sps']
    regex_str = regex_ctls_str + regex_separators_str
    prefix = "^[^"
    suffix = "]+$"
    regex = _creat_regex(regex_str,prefix=prefix,suffix=suffix)
    m=regex.search(s)
    return(bool(_real_dollar(s,m)))

def _is_cookie_pair(s):
    '''cookie-pair       = cookie-name "=" cookie-value'''
    try:
        eq_loc = s.index("=")
    except:
        return(False)
    else:
        pass
    name = s[:eq_loc]
    value = s[(eq_loc+1):]
    cond1 = _is_token(name)
    cond2 = _is_cookie_value(value)
    if(cond1 & cond2):
        return(True)
    else:
        return(False)

def _is_sane_cookie_date(s):
    '''
        sane-cookie-date  = <rfc1123-date, defined in [RFC2616], Section 3.3.1>
        SP = " "
        date1  = 2DIGIT SP month SP 4DIGIT
        wkday = "Mon" | "Tue" | "Wed" | "Thu" | "Fri" | "Sat" | "Sun"
        rfc1123-date = wkday "," SP date1 SP time SP "GMT"
    '''
    tf = xtime.detect_time_format(date_value,mode="strict")
    if(tf == "rfc1123"):
        return(True)
    else:
        return(False)

##@@@@@@@@@@@@@@@
def _expires__value(s):
    '''"Expires=" sane-cookie-date
        In practice, both expires-av and max-age-av
        are limited to dates representable by the
        user agent. 
    '''
    return(_is_sane_cookie_date(s))


def _expires__av(s):
    '''"Expires=" sane-cookie-date
        In practice, both expires-av and max-age-av                       
        are limited to dates representable by the                       
        user agent. 
    '''
    if(s[:8]=="Expires="):
        scd = s[9:]
        return(_is_sane_cookie_date(scd))
    else:
        return(False)

def __max__age__value(s):
    '''"Max-Age=" non-zero-digit *DIGIT
        In practice, both expires-av and max-age-av
        are limited to dates representable by the
        user agent. 
    '''
    regex= re.compile("^[1-9][0-9]*$")
    m = regex.search(s)
    return(bool(_real_dollar(s,m)))

def _max__age__av(s):
    '''"Max-Age=" non-zero-digit *DIGIT
        In practice, both expires-av and max-age-av
        are limited to dates representable by the
        user agent. 
    '''
    if(s[:8]=="Max-Age="):
        nums = s[9:]
        regex= re.compile("^[1-9][0-9]*$")
        m = regex.search(nums)
        return(bool(_real_dollar(nums,m)))
    else:
        return(False)
        
def _secure__av(s):
    '''"Secure"'''
    return(s=='Secure')

def _httponly__av(s):
    '''"HttpOnly"'''
    return(s=='HttpOnly')

def _path__value(s):
    '''<any CHAR except CTLs or ";">''' 
    regex_ctls_str = _all_ctls_str()
    regex_str = regex_ctls_str + ";"
    prefix = "^[^"
    suffix = "]+$"
    regex = _creat_regex(regex_str,prefix=prefix,suffix=suffix)
    m=regex.search(s)
    return(bool(_real_dollar(s,m)))

def _extension__av(s):
    '''<any CHAR except CTLs or ";">'''
    regex_ctls_str = _all_ctls_str()
    regex_str = regex_ctls_str + ";"
    prefix = "^[^"
    suffix = "]+$"
    regex = _creat_regex(regex_str,prefix=prefix,suffix=suffix)
    m=regex.search(s)
    return(bool(_real_dollar(s,m)))

def _path__av(s):
    '''
        "Path=" path-value  
    '''
    if(s[:5]=="Path="):
        p = s[6:]
        return(_path__value(p))
    else:
        return(False)

def _domain__value(s):
    '''
        domain-value = <subdomain>; 
        defined in [RFC1034], Section 3.5
            <subdomain> ::= <label> | <subdomain> "." <label>
            <label> ::= <letter> [ [ <ldh-str> ] <let-dig> ]
            <ldh-str> ::= <let-dig-hyp> | <let-dig-hyp> <ldh-str>
            <let-dig-hyp> ::= <let-dig> | "-"
            <let-dig> ::= <letter> | <digit>
            <letter> ::= any one of the 52 alphabetic characters A through Z in upper case and a through z in lower case
            <digit> ::= any one of the ten digits 0 through 9
        enhanced by [RFC1123], Section 2.1
        
    '''
    regex_label = re.compile("^[a-zA-Z](([0-9a-zA-Z\-])*[0-9a-zA-Z])*$")
    arr = s.split(".")
    rslt = True
    for i in range(0,arr.__len__()):
        m = regex_label.search(arr[i])
        cond = bool(_real_dollar(arr[i],m))
        if(cond):
            pass
        else:
            rslt = False
            break
    return(rslt)


def _domain__av(s):
    '''
        "Domain=" domain-value  
    '''
    if(s[:7]=="Domain="):
        dm = s[8:]
        return(_domain__value(dm))
    else:
        return(False)

def _cookie__av(s):
    '''
        cookie-av = expires-av / max-age-av / domain-av /path-av / secure-av / httponly-av /extension-av
    '''
    expires = _expires__av(s)
    max__age = _max__age__av(s)
    domain = _domain__av(s)
    path = _path__av(s)
    secure = _secure__av(s)
    httponly = _httponly__av(s)
    extension = _extension__av(s)
    return(expires|max__age|domain|path|secure|httponly|extension)

def _set__cookie__string(s):
    '''set-cookie-string = cookie-pair *( ";" SP cookie-av )'''
    arr = s.split("; ")
    cond = _is_cookie_pair(arr[0])
    if(cond):
        pass
    else:
        return(False)
    rslt = True
    for i in range(1,arr.__len__()):
        cond = _cookie__av(arr[i])
        if(cond):
            pass
        else:
            rslt = False
    return(rslt)

def _set__cookie__header(s):
    '''set-cookie-header = "Set-Cookie:" SP set-cookie-string '''
    if(s[:13]=="Set-Cookie: "):
        ckh = s[13:]
        return(_set__cookie__header(ckh))
    else:
        return(False)

def _delimiter(c):
    '''delimiter = %x09 / %x20-2F / %x3B-40 / %x5B-60 / %x7B-7E'''
    regex_str = _all_delimiters_str()
    prefix = "^["
    suffix = "]$"
    regex = _creat_regex(regex_str,prefix=prefix,suffix=suffix)
    m=regex.search(c)
    return(bool(_real_dollar(c,m)))

def _time__field(s):
    '''time-field      = 1*2DIGIT'''
    regex = re.compile("^[0-9]{1,2}$")
    m=regex.search(s)
    return(bool(_real_dollar(s,m)))

def _hms__time(s):
    '''hms-time = time-field ":" time-field ":" time-field'''
    regex_str = "^[0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}$"
    regex = re.compile(regex_str)
    m=regex.search(s)
    rslt = (bool(_real_dollar(s,m)))
    return(rslt)

def _non__digit(c):
    '''non-digit = %x00-2F / %x3A-FF'''
    nds = _all_non_digits_str()
    regex_str = nds
    prefix = "^[" 
    suffix = "]$"
    regex = _creat_regex(regex_str,prefix=prefix,suffix=suffix)
    m=regex.search(c)
    return(bool(_real_dollar(c,m)))

def _non__delimiter(c):
    '''non-delimiter   = %x00-08 / %x0A-1F / DIGIT / ":" / ALPHA / %x7F-FF'''
    ndels = _all_non_delimiters_str()
    regex_str = ndels
    prefix = "^[" 
    suffix = "]$"
    regex = _creat_regex(regex_str,prefix=prefix,suffix=suffix)
    m=regex.search(c)
    return(bool(_real_dollar(c,m)))

def _date__token(s):
    '''date-token      = 1*non-delimiter'''
    dt = _all_non_delimiters_str()
    regex_str = dt
    prefix = "^[" 
    suffix = "]+$"
    regex = _creat_regex(regex_str,prefix=prefix,suffix=suffix)
    m=regex.search(s)
    return(bool(_real_dollar(s,m)))

def _date__token__list(s):
    '''date-token-list = date-token *( 1*delimiter date-token )'''
    dt = re.escape(_all_non_delimiters_str())
    ads = re.escape(_all_delimiters_str())
    regex_str = "^[" + dt + "]+" +"([" +ads+ "]+"+"[" + dt + "]+)*$"
    m=regex.search(s)
    return(bool(_real_dollar(s,m)))

def _cookie__date(s):
    '''cookie-date     = *delimiter date-token-list *delimiter'''
    ads = re.escape(_all_delimiters_str())
    regex_str = "([" + ads + "]*)" + "(.*)" + "([" + ads + "]*)"
    regex = re.compile(regex_str,re.DOTALL)
    m = regex.search(s)
    try:
        dtl = m.group(2)
    except:
        return(False)
    else:
        pass
    return(_date__token__list(dtl))

def _time(s):
    '''time            = hms-time ( non-digit *OCTET )'''
    regex_str = "^([0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2})"
    nds = "[" + re.escape(_all_non_digits_str()) + "]"
    prefix = "["
    octs = re.escape(_all_octets_str())
    suffix = "]*$"
    regex_str = regex_str + nds + prefix + octs + suffix
    regex = re.compile(regex_str)
    m=regex.search(s)
    rslt = (bool(_real_dollar(s,m)))
    return(rslt)

def _year(s):
    '''year            = 2*4DIGIT ( non-digit *OCTET )'''
    regex_str = "^([0-9]{2,4})"
    nds = "[" + re.escape(_all_non_digits_str()) + "]"
    prefix = "["
    octs = re.escape(_all_octets_str())
    suffix = "]*$"
    regex_str = regex_str + nds + prefix + octs + suffix
    regex = re.compile(regex_str)
    m=regex.search(s)
    rslt = (bool(_real_dollar(s,m)))
    return(rslt)

def _month(s):
    '''( "jan" / "feb" / "mar" / "apr" /"may" / "jun" / "jul" / "aug" /"sep" / "oct" / "nov" / "dec" ) *OCTET'''
    regex_str = "^(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)"
    prefix = "["
    octs = re.escape(_all_octets_str())
    suffix = "]*$"
    regex_str = regex_str + prefix + octs + suffix
    regex = re.compile(regex_str)
    m=regex.search(s)
    rslt = (bool(_real_dollar(s,m)))
    return(rslt)

def _day__of__month(s):
    '''day-of-month    = 1*2DIGIT ( non-digit *OCTET )'''
    regex_str = "^[0-9]{1,2}"
    ndts = re.escape(_all_non_digits_str())
    prefix = "["
    octs = re.escape(_all_octets_str())
    suffix = "]*$"
    regex_str = regex_str + "[" + ndts + "]" + prefix + octs + suffix
    regex = re.compile(regex_str)
    m=regex.search(s)
    rslt = (bool(_real_dollar(s,m)))
    return(rslt)

Core_Rules = {
    'NUL' : _isNUL,
    'OCTET' : _isOCTET,
    'WSP' : _isWSP,
    'OWS' : _isOWS,
    'obs-fold' : _is_obs_fold,
    'cookie-octet' : _is_cookie_octet,
    'cookie-value' : _is_cookie_value,
    'cookie-name' : _is_token,
    'sane-cookie-date' : _is_sane_cookie_date,
    'cookie-pair' : _is_cookie_pair,
    'expires-av' : _expires__av,
    'max-age-av' : _max__age__av,
    'secure-av' : _secure__av,
    'httponly-av' : _httponly__av,
    'path-value' : _path__value,
    'extension-av' : _extension__av,
    'path-av' : _path__av,
    'domain-av' : _domain__av,
    'cookie-av' : _cookie__av,
    'set-cookie-string' : _set__cookie__string,
    'set-cookie-header' : _set__cookie__header,
    'delimiter' : _delimiter,
    'time-field' : _time__field,
    'hms-time' : _hms__time,
    'time' : _time,
    'non-digit' : _non__digit,
    'non-delimiter' : _non__delimiter,
    'date-token' : _date__token,
    'date-token-list' : _date__token__list,
    'cookie-date' : _cookie__date,
    'time': _time,
    'year': _year,
    'month': _month,
    'day-of-month': _day__of__month
}

########################
def split_cookie_date_str(s):
    '''split cookie_date_str to date-tokens list'''
    def _open_token(tok,input_symbol,rslt):
        tok = tok + input_symbol
        return(tok)
    _append_token = _open_token
    def _close_token(tok,input_symbol,rslt):
        rslt.append(tok)
        tok = ''
        return(tok)
    machine = fsm.FSM()
    machine.add("INIT",_delimiter,None,"DEL")
    machine.add("INIT",_non__delimiter,_open_token,"TOK")
    machine.add("DEL",_delimiter,None,"DEL")
    machine.add("DEL",_non__delimiter,_open_token,"TOK")
    machine.add("TOK",_delimiter,_close_token,"DEL")
    machine.add("TOK",_non__delimiter,_append_token,"TOK")
    curr_state = "INIT"
    rslt = []
    tok= ''
    for i in range(0,s.__len__()):
        input_symbol = s[i]
        action,next_state,trigger_checker = machine.search(curr_state,input_symbol)
        if(action):
            tok = action(tok,input_symbol,rslt)
        else:
            pass
        curr_state = next_state
    if(curr_state == 'INIT'):
        return([])
    elif(curr_state == 'DEL'):
        pass
    else:
        rslt.append(tok)
    return(rslt)

def parse_cookie_date(s):
    '''parsed-cookie-date'''
    toks = split_cookie_date_str(s)
    cookie_date_dict = {
        'found-time':False,
        'hour-value':None,
        'minute-value':None,
        'second-value': None,
        'found-day-of-month':False,
        'day-of-month-value':None,
        'found-month':False,
        'month-value':None,
        'found-year':False,
        'year-value':None,
        '_timestamp':None,
    }
    tests = ['hms-time','day-of-month','month','year']
    for tok in toks:
        if('hms-time' in tests):
            cond = Core_Rules['hms-time'](tok)
            if(cond):
                tmp = tok.split(":")
                if((int(tmp[0])<0) | (int(tmp[0])>23)):
                    return(None)
                else:
                    cookie_date_dict['hour-value'] = int(tmp[0])
                if((int(tmp[1])<0) | (int(tmp[1])>59)):
                    return(None)
                else:
                    cookie_date_dict['minute-value'] = tmp[1]
                if((int(tmp[2])<0) | (int(tmp[2])>59)):
                    return(None)
                else:
                    cookie_date_dict['second-value'] = tmp[2]
                cookie_date_dict['found-time'] = True
                tests.remove('hms-time')
            else:
                pass
        elif('day-of-month' in tests):
            cond = Core_Rules['day-of-month'](tok)
            if(cond):
                regex = re.compile("[0-9]{1,2}")
                tmp = regex.search(tok).group(0)
                if((int(tmp)<1) | (int(tmp)>31)):
                    return(None)
                else:
                    cookie_date_dict['day-of-month-value'] = int(tmp)
                cookie_date_dict['found-day-of-month'] = True
                tests.remove('day-of-month')
            else:
                pass
        elif('month' in tests):
            cond = Core_Rules['month'](tok)
            if(cond):
                tmp = tok[0:3]
                cookie_date_dict['month-value'] = int(tmp)
                cookie_date_dict['found-month'] = True
                tests.remove('month')
            else:
                pass
        elif('year' in tests):
            cond = Core_Rules['year'](tok)
            if(cond):
                regex = re.compile("[0-9]{2,4}")
                tmp = regex.search(tok).group(0)
                if((int(tmp)>=70)&(int(tmp)<=99)):
                    tmp = 1900 + int(tmp)
                elif((int(tmp)>=0)&(int(tmp)<=69)):
                    tmp = 2000 + int(tmp)
                else:
                    tmp = int(tmp)
                cookie_date_dict['year-value'] = tmp
                cookie_date_dict['found-year'] = True
                tests.remove('year')
            else:
                pass
        else:
            pass
    cookie_date_dict['_timestamp'] = xtime.str2ts(s)
    return(cookie_date_dict)


########################

#=========================================================================================================================

def _fillin_max__age(Cookie,max_age_value):
    cond = _max__age__value(max_age_value)
    if(cond):
        Cookie['Max-Age'] = max_age_value
    else:
        Cookie['Max-Age'] = None
    return(Cookie)

def _fillin_expires(Cookie,expires):
    cond = _expires__value(expires)
    if(cond):
        Cookie['Expires'] = expires
    else:
        Cookie['Expires'] = None
    return(Cookie)

def _fillin_expiry__time(Cookie):
    '''
        If a cookie has both the Max-Age and the Expires attribute, 
        the Max   Age attribute has precedence and controls the expiration date of the cookie. 
        If a cookie has neither the Max-Age nor the Expires attribute, 
        the user agent will retain the cookie until "the currentsession is over" 
        (as defined by the user agent).
    '''
    if(Cookie['Max-Age']):
        ts = time.time() + Cookie['Max-Age']
        Cookie['persistent-flag'] = True
        Cookie['expiry-time'] = ts
    elif(Cookie['Expires']):
        ts = xtime.str2ts(Cookie['Expires'])
        Cookie['persistent-flag'] = True
        Cookie['expiry-time'] = ts
    else:
        Cookie['persistent-flag'] = False
    return(Cookie)

def _expired(Cookie):
    '''if the Cookie is expired'''
    Cookie = _fillin_expire__time(Cookie)
    if(Cookie['expiry-time']):
        cond = Cookie['expiry-time'] < time.time()
        return(cond)
    else:
        return(True)

def _format_domain(domain):
    '''
        Note that a leading %x2E ("."), if present,
        is ignored even though that character is not permitted, 
        but a trailing %x2E ("."), if present, 
        will cause the user agent to ignore   the attribute.
    '''
    domain = xutils.str_lstrip(domain,".",1)
    return(domain)

def _is_valid_domain_format(domain):
    '''
        domain-value = <subdomain>; 
        defined in [RFC1034], Section 3.5
            <subdomain> ::= <label> | <subdomain> "." <label>
            <label> ::= <letter> [ [ <ldh-str> ] <let-dig> ]
            <ldh-str> ::= <let-dig-hyp> | <let-dig-hyp> <ldh-str>
            <let-dig-hyp> ::= <let-dig> | "-"
            <let-dig> ::= <letter> | <digit>
            <letter> ::= any one of the 52 alphabetic characters A through Z in upper case and a through z in lower case
            <digit> ::= any one of the ten digits 0 through 9
        enhanced by [RFC1123], Section 2.1
        
    '''
    domain = _format_domain(domain)
    return(_domain__value(domain))

def _domain_in_domain(dom2,dom1):
    dom2 = dom2.lower()
    dom1 = dom1.lower()
    dom1_arr = dom1.split(".")
    dom2_arr = dom2.split(".")
    length1 = dom1_arr.__len__()
    length2 = dom2_arr.__len__()
    if(length1 > length2):
        return(False)
    else:
        for i in range(length1-1,-1,-1):
            cond = (dom1_arr[i] == dom2_arr[i])
            if(cond):
                pass
            else:
                return(False)
        return(True)
    

def _origin_in_domain(domain,src_url):
    '''
        The user agent will reject cookies unless the Domain attribute
        specifies a scope for the cookie that would include the origin server.
        For example, the user agent will accept a cookie with a Domain attribute
        of "example.com" or of "foo.example.com" from foo.example.com, but the 
        user agent will not accept a cookie with a Domain attribute of "bar.example.com" 
        or of "baz.foo.example.com".
    '''
    domain = _format_domain(domain)
    netloc =  urllib.parse.urlparse(src_url).netloc
    netloc = _format_domain(netloc)
    cond = _domain_in_domain(netloc,domain)
    return(cond)

def _dst_in_domain(domain,dst_url):
    domain = _format_domain(domain)
    netloc =  urllib.parse.urlparse(dst_url).netloc
    netloc = _format_domain(netloc)
    cond = _domain_in_domain(netloc,domain)
    return(cond)

def _in_domain(domain,src_url,dst_url,reject_public_suffixes=[]):
    cond_src = _origin_in_domain(domain,src_url)
    cond_dst = _dst_in_domain(domain,dst_url)
    cond_pub_suffixes = True
    domain = _format_domain(domain)
    for i in range(0,reject_public_suffixes):
        cond = (domain == reject_public_suffixes[i])
        if(cond):
            pass
        else:
            cond_pub_suffixes = False
            break
    if(cond_src & cond_dst & cond_pub_suffixes):
        return(True)
    else:
        return(False)

def _fillin_domain(Cookie,domain,server_url):
    '''If the server omits the Domain attribute, the user   agent will return the cookie only to the origin server'''
    if(domain == None):
        domain =urllib.parse.urlparse(server_url).netloc
        Cookie['host-only-flag'] = True
        Cookie['Domain'] = domain
    else:
        domain = _format_domain(domain)
        cond = _is_valid_domain_format(domain)
        if(cond):
            Cookie['host-only-flag'] = False
            Cookie['Domain'] = domain
        else:
            domain = urllib.parse.urlparse(server_url).netloc
            Cookie['host-only-flag'] = True
            Cookie['Domain'] = domain
    return(Cookie)

def _format_path(s,mode="strict"):
    '''
        1 .Let uri-path be the path portion of the request-uri if such a portion exists (and empty otherwise).
        For example, if the request-uri contains just a path (and optional query string),
        then the uri-path is that path (without the %x3F ("?") character or query string), 
        and if the request-uri contains a full absoluteURI, 
        the uri-path is the path component of that URI.
        
        2 .If the uri-path is empty or if the first character of the uri
        path is not a %x2F ("/") character, output %x2F ("/") and skip the remaining steps
        ---------------this step is puzzle ,the loose mode will be this behavior
        3. If the uri-path contains no more than one %x2F ("/") character,
        output %x2F ("/") and skip the remaining step.
        
        4. Output the characters of the uri-path from the first character up to, 
        but not including, the right-most %x2F ("/").
    '''
    #step 1
    s =  urllib.parse.urlparse(s)
    #step 2
    if(s == ""):
        return("/")
    elif(s[0]!="/"):
        if(mode == "loose"):
            return("/")
        else:
            s = "/" + s
            s = xutils.str_rstrip(s,"/",1)
            return(s)
    #step 3
    elif(s=="/"):
        return("/")
    #step 4:
    else:
        s = xutils.str_rstrip(s,"/",1)
        return(s)

def _path_in_path(path2,path1,mode='strict'):
    path1 = _format_path(path1,mode=mode)
    path1 = xutils.str_lstrip(path1,"/",1)
    path2 = _format_path(path2,mode=mode)
    path2 = xutils.str_lstrip(path2,"/",1)
    p1_arr = path1.split("/")
    if(p1_arr == [""]):
        return(True)
    else:
        pass
    p2_arr = path2.split("/")
    length1 = p1_arr.__len__()
    length2 = p2_arr.__len__()
    if(length1 > length2):
        return(False)
    else:
        for i in range(length1-1,-1,-1):
            cond = (p1_arr[i] == p2_arr[i])
            if(cond):
                pass
            else:
                return(False)
        return(True)

def _path_matching(path,dst_path):
    '''
        A request-path path-matches a given cookie-path if at least one of   the following conditions holds:
        o  The cookie-path and the request-path are identical.
        o  The cookie-path is a prefix of the request-path, 
           and the last character of the cookie-path is %x2F ("/").
        o  The cookie-path is a prefix of the request-path, 
           and the first character of the request-path that 
           is not included in the cookie path is a %x2F ("/") character.
    '''
    plength = path.__len__()
    if(plength > dst_path.__len__()):
        cond = False
    elif(path == dst_path):
        cond = True
    elif(dst_path[0:plength] == path):
        if(path[-1] == "/"):
            cond = True
        else:
            if(dst_path[plength]=="/"):
                cond = True
            else:
                cond = False
    else:
        cond = False
    return(cond)

def _url_in_path(dst_url,path):
    '''
        A request-path path-matches a given cookie-path if at least one of   the following conditions holds:
        o  The cookie-path and the request-path are identical.
        o  The cookie-path is a prefix of the request-path, 
           and the last character of the cookie-path is %x2F ("/").
        o  The cookie-path is a prefix of the request-path, 
           and the first character of the request-path that 
           is not included in the cookie path is a %x2F ("/") character.
    '''
    dst_path = urllib.parse.urlparse(dst_url).path
    return(_path_matching(path,dst_path))

def _fillin_path(Cookie,path,server_url,mode="strict"):
    '''
        If the server omits the Path attribute, 
        the user agent will use the "directory" of the request-uri’s path component as the default value.
    '''
    if(path == None):
        path = urllib.parse.urlparse(server_url).path
        path = _format_path(path,mode=mode)
    else:
        cond = _path__value(path)
        if(cond):
            pass
        else:
            path = urllib.parse.urlparse(server_url).path
    Cookie['Path'] = path
    return(Cookie)

def  _canonicalize_hostname(hn):
    '''
        A canonicalized host name is the string generated by the following algorithm:
            1.  Convert the host name to a sequence of individual domain name labels.
            2.  Convert each label that is not a Non-Reserved LDH (NR-LDH) label,
                to an A-label (see Section 2.3.2.1 of [RFC5890] for the former and latter), 
                or to a "punycode label" (a label resulting from the "ToASCII" conversion in Section 4 of [RFC3490]), 
                as appropriate (see Section 6.3 of this specification).
            3.  Concatenate the resulting labels, separated by a %x2E (".") character.
    '''
    print("NOT IMPLEMENTED YET")
    return(hn)

def _is_valid_hostname(s):
    print("NOT IMPLEMENTED YET")
    return(True)

def _domain_matching(domain,s):
    '''
        A string domain-matches a given domain string if at least one of the following conditions hold:
           o  The domain string and the string are identical.  
             (Note that both the domain string and the string will have been canonicalized to lower case at this point.)
           o  All of the following conditions hold:
              *  The domain string is a suffix of the string.
              *  The last character of the string that is not included in the 
                 domain string is a %x2E (".") character.
              *  The string is a host name (i.e., not an IP address).
    '''
    domain = domain.lower()
    s = s.lower()
    dlen = domain.__len__()
    slen = s.__len__()
    if(dlen > slen):
        cond = False
    else:
        if(domain == s):
            cond = True
        elif(domain == s[0:dlen]):
            if(s[dlen]=="."):
                if(_is_valid_hostname(s)):
                    cond = True
                else:
                    cond = False
            else:
                return(False)
        else:
            cond = False
    return(cond)


#=====================================
def _decode_set__cookie__av(s,do_unquote=False):
    '''
        >>> rfc6265._decode_set__cookie__av("a=b")
        ('a', 'b')
        >>>
    '''
    regex = re.compile("(.*?)=(.*)")
    m = regex.search(s)
    return((m.group(1),m.group(2)))

avstr2tuple = _decode_set__cookie__av

def avstr2dict(s,do_unquote=False):
    regex = re.compile("(.*?)=(.*)")
    m = regex.search(s)
    k = m.group(1)
    v = m.group(2)
    if(do_unquote):
        k = urllib.parse.unquote(k)
        v = urllib.parse.unquote(v)
    else:
        pass
    return({k:v})

def tuple2avstr(t,do_quote=False):
    k = t[0]
    v = t[1]
    if(do_unquote):
        k = urllib.parse.quote(str(k))
        v = urllib.parse.quote(str(v))
    else:
        pass
    return(k+'='+v)

def dict2avstr(d,do_quote=False):
    k = d.keys()[0]
    v = d.values()[0]
    if(do_quote):
        k = urllib.parse.quote(str(k))
        v = urllib.parse.quote(str(v))
    else:
        pass
    return(k+'='+v)

def new_cookie():
    Cookie = {
        'Expires':None,
        'Max-Age':None,
        'Domain':None,
        'Path':None,
        'Secure':None,
        'HttpOnly':None,
        'name':None,  
        'value':None,
        'expiry-time':None,
        'domain':None,
        'path':None,
        'creation-time':None, 
        'last-access-time': None,
        'persistent-flag': None,
        'host-only-flag': None, 
        'secure-only-flag':None,
        'http-only-flag':None,
        '_req-type':'Cookie',
        '_resp-type':'Set-Cookie'
    }
    return(Cookie)



def _parse_set__cookie__string(s,server_url,mode="strict"):
    '''
        NOTE: The algorithm below is more permissive than the grammar in Section 4.1.
        For example, the algorithm strips leading and trailing whitespace from the 
        cookie name and value (but maintains internal whitespace), whereas the grammar 
        in Section 4.1 forbids whitespace in   these positions. 
        User agents use this algorithm so as to interoperate with servers that do not follow
        the recommendations in Section 4.

        1.  If the set-cookie-string contains a %x3B (";") character:
            The name-value-pair string consists of the characters up to,
            but not including, the first %x3B (";"), and the unparsed 
            attributes consist of the remainder of the set-cookie-string
            (including the %x3B (";") in question).
            Otherwise:
                The name-value-pair string consists of all the characters
                contained in the set-cookie-string, and the unparsed
                attributes is the empty string.
            2.  If the name-value-pair string lacks a %x3D ("=") character,
                ignore the set-cookie-string entirely.
            3.  The (possibly empty) name string consists of the characters up to, 
                but not including, the first %x3D ("=") character, and the
                (possibly empty) value string consists of the characters after 
                the first %x3D ("=") character.
            4.  Remove any leading or trailing WSP characters from the name
                string and the value string.
            5.  If the name string is empty, ignore the set-cookie-string entirely.
            6.  The cookie-name is the name string, and the cookie-value is the value string.
        The user agent MUST use an algorithm equivalent to the following   algorithm to parse the unparsed-attributes:
            1.  If the unparsed-attributes string is empty, skip the rest of these steps.
            2.  Discard the first character of the unparsed-attributes (which will be a %x3B (";") character).
            3.  If the remaining unparsed-attributes contains a %x3B (";")character:
                Consume the characters of the unparsed-attributes up to, 
                but not including, the first %x3B (";") character.
                Otherwise:
                   Consume the remainder of the unparsed-attributes.
                Let the cookie-av string be the characters consumed in this step.
            4.  If the cookie-av string contains a %x3D ("=") character:
                The (possibly empty) attribute-name string consists of the characters up to, 
                but not including, the first %x3D ("=") character, 
                and the (possibly empty) attribute-value string consists 
                of the characters after the first %x3D ("=") character.
                Otherwise:
                   The attribute-name string consists of the entire cookie-av string, 
                   and the attribute-value string is empty.
            5.  Remove any leading or trailing WSP characters from the attribute 
                name string and the attribute-value string.
            6.  Process the attribute-name and attribute-value according to the 
                requirements in the following subsections. 
                (Notice that attributes with unrecognized attribute-names are ignored.)
            7.  Return to Step 1 of this algorithm.
                When the user agent finishes parsing the set-cookie-string, 
                the user agent is said to "receive a cookie" from the request-uri 
                with name cookie-name, value cookie-value, and attributes cookie-attribute list.
                (See Section 5.3 for additional requirements triggered by   receiving a cookie.
        attribute-name :  case-insensitively;
        domain : Convert the cookie-domain to lower case.
        >>> import rfc6265
        >>> from xdict.jprint import pobj
        >>> from xdict.jprint import pdir
        >>> server_url = "https://x.y.z/abc"
        >>> s = 'TS=0105b666; Path=/; Secure; HTTPOnly'
        >>> pobj(rfc6265.set_cookie_str2ck(s,server_url))
        {
         'value': '0105b666',
         'Secure': 'Secure',
         'host-only-flag': True,
         'secure-only-flag': True,
         'expiry-time': None,
         'creation-time': None,
         'last-access-time': None,
         'HttpOnly': 'HttpOnly',
         'Expires': None,
         'Max-Age': None,
         'Path': '/',
         '_resp-type': 'Set-Cookie',
         'Domain': 'x.y.z',
         'name': 'TS',
         '_req-type': 'Cookie',
         'persistent-flag': False,
         'http-only-flag': True
        }
    '''
    Cookie = new_cookie()
    arr = s.split(";")
    nvarr = []
    for i in range(0,arr.__len__()):
        tmp = arr[i].strip(" ")
        if(tmp == ""):
            pass
        else:
            nvarr.append(tmp)
    nv = nvarr[0]
    if("=" in nv):
        n,v = _decode_set__cookie__av(nv)
        n = n.strip(" ")
        v = v.strip(" ")
        if(n == ""):
            pass
        else:
            condn = _is_token(n)
            condv = _is_cookie_value(v)
            if(condn & condv):
                Cookie['name'] = n
                Cookie['value'] = v
            else:
                pass
    else:
        pass
    nvarr.pop(0)
    for nv in nvarr:
        if("=" in nv):
            n,v = _decode_set__cookie__av(nv)
            n = n.strip(" ")
            v = v.strip(" ")
            if(n == ""):
                pass
            else:
                if(n.lower() == 'Expire'.lower()):
                    _fillin_expires(Cookie,v)
                elif(n.lower() == 'Max-Age'.lower()):
                    _fillin_max__age(Cookie,v)
                elif(n.lower() == 'Domain'.lower()):
                    _fillin_domain(Cookie,v,server_url)
                elif(n.lower() == 'Path'.lower()):
                    _fillin_path(Cookie,v,server_url,mode=mode) 
                else:
                    pass
        else:
            n = nv.strip(' ')
            if(n.lower() == 'Secure'.lower()):
                Cookie['Secure'] = 'Secure'
                Cookie['secure-only-flag'] = True
            elif(n.lower() == 'HttpOnly'.lower()):
                Cookie['HttpOnly'] = 'HttpOnly'
                Cookie['http-only-flag'] = True
            else:
                pass
    _fillin_expiry__time(Cookie)
    if(Cookie['domain'] == None):
        _fillin_domain(Cookie,None,server_url)
    else:
        pass
    return(Cookie)

set_cookie_str2ck = _parse_set__cookie__string
scks2ck = _parse_set__cookie__string
str2ck = _parse_set__cookie__string


#========================================================

def _parse_set_cookie_tuple(tl,server_url,mode="strict"):
    s = tl[1]
    return(_parse_set__cookie__string(s,server_url,mode=mode))

set_cookie_tuple2ck = _parse_set_cookie_tuple
sckt2ck = _parse_set_cookie_tuple
tuple2ck = _parse_set_cookie_tuple

def _parse_set__cookie__header(set_cookie_header,server_url,mode="strict"):
    s = set_cookie_header[13:]
    return(_parse_set__cookie__string(s,server_url,mode=mode))

set_cookie_header2ck = _parse_set__cookie__header
sckh2ck = _parse_set__cookie__header
header2ck = _parse_set__cookie__header

#===========================================================


def ck2set_cookie_str(Cookie):
    ck_str =""
    if(Cookie['name']):
        ck_str = ck_str + Cookie['name'] 
    else:
        return(None)
    if(Cookie['value']):
        ck_str = ck_str + "=" + Cookie['value'] +";"
    else:
        return(None)
    if(Cookie['Domain']):
        ck_str = ck_str + "Domain=" + Cookie['Domain'] +";"
    else:
        pass
    if(Cookie['Path']):
        ck_str = ck_str + "Path=" + Cookie['Path'] +";"
    else:
        pass
    if(Cookie['persistent-flag']):
        if(Cookie['Max-Age']):
            ck_str = ck_str + "Max-Age=" + Cookie['Max-Age'] +";"
        else:
            pass
        if(Cookie['Expires']):
            ck_str = ck_str + "Expires=" + Cookie['Expires'] +";"
        else:
            pass
    else:
        pass
    if(Cookie['secure-only-flag']):
        if(Cookie['Secure']):
            ck_str = ck_str + Cookie['Secure'] +";"
        else:
            pass
    else:
        pass
    if(Cookie['http-only-flag']):
        if(Cookie['HttpOnly']):
            ck_str = ck_str  + Cookie['HttpOnly'] +";"
        else:
            pass
    else:
        pass
    ck_str = xutils.str_rstrip(ck_str,";",1)
    return(ck_str)

ck2scks = ck2set_cookie_str
ck2str = ck2set_cookie_str

#================================================================

def ck2set_cookie_tuple(Cookie):
    return(('Set-Cookie',ck2set_cookie_str(Cookie)))

ck2sckt = ck2set_cookie_tuple
ck2tuple = ck2set_cookie_tuple

def ck2set_cookie_header(Cookie):
    return('Set-Cookie: ' +ck2set_cookie_str(Cookie))

ck2sckh = ck2set_cookie_header
ck2header = ck2set_cookie_header

#=================================================================

def cookie_str_to_avstrList(req_ckstr):
    '''_gh_sess=eyJs--d8; tz=Asia%2FShanghai; logged_in=no; _octo=GH1.1.1737332611.1518621215; _ga=GA1.2.1308889339.1518621215'''
    arr = req_ckstr.split("; ")
    return(arr)

cks2avsl = cookie_str_to_avstrList

def avstrList_to_cookie_str(avsl):
    rslt = ""
    length = avsl.__len__()
    for i in range(0,length):
        rslt = rslt + avsl[i] + "; "
    rslt = xutils.str_rstrip(rslt," ",1)
    rslt = xutils.str_rstrip(rslt,";",1)
    return(rslt)

avsl2cks = avstrList_to_cookie_str

def cookie_str_to_dictList(req_ckstr):
    '''_gh_sess=eyJs--d8; tz=Asia%2FShanghai; logged_in=no; _octo=GH1.1.1737332611.1518621215; _ga=GA1.2.1308889339.1518621215'''
    ckdl = []
    arr = req_ckstr.split("; ")
    length = arr.__len__()
    for i in range(0,length):
        ele = avstr2dict(arr[i])
        ckdl.append(ele)
    return(ckdl)

cks2dl = cookie_str_to_dictList
str2dl = cookie_str_to_dictList

def dictList_to_cookie_str(dl):
    length = dl.__len__()
    rslt = ""
    for i in range(0,length):
        avstr = dict2avstr(dl[i])
        rslt = rslt + avstr + "; "
    rslt = xutils.str_rstrip(rslt," ",1)
    rslt = xutils.str_rstrip(rslt,";",1)
    return(rslt)


dl2cks = dictList_to_cookie_str
dl2str = dictList_to_cookie_str

def cookie_str_to_tupleList(req_ckstr):
    '''_gh_sess=eyJs--d8; tz=Asia%2FShanghai; logged_in=no; _octo=GH1.1.1737332611.1518621215; _ga=GA1.2.1308889339.1518621215'''
    cktl = []
    arr = req_ckstr.split("; ")
    length = arr.__len__()
    for i in range(0,length):
        ele = avstr2tuple(arr[i])
        cktl.append(ele)
    return(cktl)

cks2tl = cookie_str_to_tupleList
str2tl = cookie_str_to_tupleList

def tupleList_to_cookie_str(tl):
    '''_gh_sess=eyJs--d8; tz=Asia%2FShanghai; logged_in=no; _octo=GH1.1.1737332611.1518621215; _ga=GA1.2.1308889339.1518621215'''
    length = tl.__len__()
    rslt = ""
    for i in range(0,length):
        avstr = tuple2avstr(dl[i])
        rslt = rslt + avstr + "; "
    rslt = xutils.str_rstrip(rslt," ",1)
    rslt = xutils.str_rstrip(rslt,";",1)
    return(rslt)


tl2cks = tupleList_to_cookie_str
tl2str = tupleList_to_cookie_str

def cookie_header_to_dictList(req_ckheader):
    req_ckstr = req_ckheader[8:]
    return(cks2dl(req_ckstr))

ckh2dl = cookie_header_to_dictList
header2dl = cookie_header_to_dictList

def dictList_to_cookie_header(dl):
    req_ckstr = dl2cks(dl)
    return("Cookie: " + req_ckstr)


dl2ckh = dictList_to_cookie_header
dl2header = dictList_to_cookie_header

def cookie_header_to_tupleList(req_ckheader):
    req_ckstr = req_ckheader[8:]
    return(cks2tl(req_ckstr))

ckh2tl = cookie_header_to_tupleList
header2tl = cookie_header_to_tupleList

def tupleList_to_cookie_header(req_ckheader):
    req_ckstr = tl2cks(dl)
    return("Cookie: " + req_ckstr)

tl2ckh = tupleList_to_cookie_header
tl2header = tupleList_to_cookie_header

#=========================================================================================================


def cookieStr_prepend_with_avstr(cks):
    pass

prepend_cks_with_avstr = cookieStr_prepend_with_avstr
cks_prepend_with_avstr = cookieStr_prepend_with_avstr

def cookieStr_prepend_with_tuple(cks):
    pass


prepend_cks_with_tuple = cookieStr_prepend_with_tuple
cks_prepend_with_tuple = cookieStr_prepend_with_tuple

def cookieStr_prepend_with_dict(cks):
    pass

prepend_cks_with_dict = cookieStr_prepend_with_dict
cks_prepend_with_dict = cookieStr_prepend_with_dict

def cookieStr_prepend_with_avstrList(cks):
    pass

prepend_cks_with_avstrList = cookieStr_prepend_with_avstrList
cks_prepend_with_avstrList = cookieStr_prepend_with_avstrList

def cookieStr_prepend_with_tupleList(cks):
    pass

prepend_cks_with_tupleList = cookieStr_prepend_with_tupleList
cks_prepend_with_tupleList = cookieStr_prepend_with_tupleList

def cookieStr_prepend_with_dictList(cks):
    pass

prepend_cks_with_dictList = cookieStr_prepend_with_dictList
cks_prepend_with_dictList = cookieStr_prepend_with_dictList


#=============================================================================















# If the user agent receives a new cookie with the same cookie-name,   
# domain-value, and path-value as a cookie that it has already stored,   
# the existing cookie is evicted and replaced with the new cookie.



# 10.  If the cookie was received from a "non-HTTP" API and the        cookie’s http-only-flag is set, abort these steps and ignore the        cookie entirely.
   # 11.  If the cookie store contains a cookie with the same name,        domain, and path as the newly created cookie:
        # 1.  Let old-cookie be the existing cookie with the same name,            domain, and path as the newly created cookie.  (Notice that            this algorithm maintains the invariant that there is at most            one such cookie.)
        # 2.  If the newly created cookie was received from a "non-HTTP"            API and the old-cookie’s http-only-flag is set, abort these            steps and ignore the newly created cookie entirely.
        # 3.  Update the creation-time of the newly created cookie to            match the creation-time of the old-cookie.
        # 4.  Remove the old-cookie from the cookie store.
 


#"Cookie: BIGipServer~Public~vs-onlinechannel2.ext.wd.govt.nz_443.app~vs-onlinechannel2.ext.wd.govt.nz_443_pool=rd1906o00000000000000000000ffff0ae82285o80; TS013d8ed5=0105b6b7b66d6b29124893459b055cd1f4a5a7335b12046ffe1a55a0b1d7c59a2898116c3630e396b30c74f7a246bceef6f531669bc27c85ed400d8f7a5caa16c9e4bbe36ec00851c66cab0d5c90325df26f2234f1; TSPD_101=08819c2a25ab28002cfb583c7dbacbe5871ed5c87ecb3f59eb3a88cabd414fc824ba07b50c9ffc25ee5cd77337f984e508c7223e67051000d70c291105bfdc6e9483047df012ed90:; __RequestVerificationToken=h835fLFxEuqhkzpklhfFifRibVRTPPcgTAcOQqYS4usAV_20QUDv-fpkYg9z7YRTyXJFzmqLNoi0nelpGLtGmZQaBy41"

#Unless the cookie’s attributes indicate otherwise, the cookie is   returned only to the origin server (and not, for example, to any   subdomains), and it expires at the end of the current session (as   defined by the user agent).  User agents ignore unrecognized cookie   attributes (but not the entire cookie).


# (
  # 'Set-Cookie',
  # 'BIGipServer~Public~vs-onlinechannel2.ext.wd.govt.nz_443.app~vs-onlinechannel2.ext.wd.govt.nz_443_pool=rd1906o00000000000000000000ffff0ae82284o80; path=/'
 # ),
 # (
  # 'Set-Cookie',
  # 'TS013d8ed5=0105b6b7b661820adb08f47c5ea240ddfc5866334894c224bcaa1865eb72664797ad1905f3d90d64182687996238bb77e476bd5daa7bfa3381cca3fff2f42dba045a7bb096; Path=/; Secure; HTTPOnly'
 # )

def help():
    abbrev = '''
        ck    Cookie  
                  {
                   'domain': None,
                   'value': '0105b666',
                   'Secure': 'Secure',
                   'host-only-flag': True,
                   'secure-only-flag': True,
                   'path': None,
                   'expiry-time': None,
                   'creation-time': None,
                   'last-access-time': None,
                   'HttpOnly': 'HttpOnly',
                   'Expires': None,
                   'Max-Age': None,
                   'Path': '/',
                   '_resp-type': 'Set-Cookie',
                   'Domain': 'x.y.z',
                   'name': 'TS',
                   '_req-type': 'Cookie',
                   'persistent-flag': False,
                   'http-only-flag': True
                  }
        ckl   list of  Cookie
             
        avs   cookie-av string  or cookie-pair str
              
        avsl  list of avs 
            
        ckh   cookie-header
              
        cks   cookie-string
              
        ckdl  cookies-dict-list
              
        cktl  cookies-tuple-list
              
        sckh  set-cookie-header
                  "Set-Cookie: TS=0105b666; Path=/; Secure; HTTPOnly"
        scks  set-cookie-string
                  "TS=0105b666; Path=/; Secure; HTTPOnly"
        sckt  set-cookie-tuple
                  ('Set-Cookie','TS=0105b666; Path=/; Secure; HTTPOnly')

    '''
    print(abbrev)


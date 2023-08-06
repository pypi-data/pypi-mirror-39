import edict.edict as eded
import elist.elist as elel
import tlist.tlist as tltl
import Levenshtein as edis


s ='''100 Continue
101 Switching Protocol
200 OK
201 Created
202 Accepted
203 Non-Authoritative Information
204 No Content
205 Reset Content
206 Partial Content
300 Multiple Choices
301 Moved Permanently
302 Found
303 See Other
304 Not Modified
307 Temporary Redirect
308 Permanent Redirect
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
405 Method Not Allowed
406 Not Acceptable
407 Proxy Authentication Required
408 Request Timeout
409 Conflict
410 Gone
411 Length Required
412 Precondition Failed
413 Payload Too Large
414 URI Too Long
415 Unsupported Media Type
416 Range Not Satisfiable
417 Expectation Failed
418 I am a teapot
422 Unprocessable Entity
426 Upgrade Required
428 Precondition Required
429 Too Many Requests
431 Request Header Fields Too Large
451 Unavailable For Legal Reasons
500 Internal Server Error
501 Not Implemented
502 Bad Gateway
503 Service Unavailable
504 Gateway Timeout
505 HTTP Version Not Supported
511 Network Authentication Required'''

def map_func(sen):
    sen = sen.strip("\x20")
    arr = sen.split("\x20")
    t0 = int(arr[0])
    t1 = elel.join(arr[1:],"\x20")
    return((t0,t1))
    

def s2d(s):
    s = s.strip(" ").strip("\n").strip(" ")
    arr = s.split("\n")    
    tl = elel.array_map(arr,map_func)
    d = tltl.tlist2dict(tl)
    return(d)




REASONS = {
 100: 'Continue',
 101: 'Switching Protocol',
 200: 'OK',
 201: 'Created',
 202: 'Accepted',
 203: 'Non-Authoritative Information',
 204: 'No Content',
 205: 'Reset Content',
 206: 'Partial Content',
 300: 'Multiple Choices',
 301: 'Moved Permanently',
 302: 'Found',
 303: 'See Other',
 304: 'Not Modified',
 307: 'Temporary Redirect',
 308: 'Permanent Redirect',
 400: 'Bad Request',
 401: 'Unauthorized',
 403: 'Forbidden',
 404: 'Not Found',
 405: 'Method Not Allowed',
 406: 'Not Acceptable',
 407: 'Proxy Authentication Required',
 408: 'Request Timeout',
 409: 'Conflict',
 410: 'Gone',
 411: 'Length Required',
 412: 'Precondition Failed',
 413: 'Payload Too Large',
 414: 'URI Too Long',
 415: 'Unsupported Media Type',
 416: 'Range Not Satisfiable',
 417: 'Expectation Failed',
 418: "I am a teapot",
 422: 'Unprocessable Entity',
 426: 'Upgrade Required',
 428: 'Precondition Required',
 429: 'Too Many Requests',
 431: 'Request Header Fields Too Large',
 451: 'Unavailable For Legal Reasons',
 500: 'Internal Server Error',
 501: 'Not Implemented',
 502: 'Bad Gateway',
 503: 'Service Unavailable',
 504: 'Gateway Timeout',
 505: 'HTTP Version Not Supported',
 511: 'Network Authentication Required'
}

REASONS_MD = {
 'Continue': 100,
 'Switching Protocol': 101,
 'OK': 200,
 'Created': 201,
 'Accepted': 202,
 'Non-Authoritative Information': 203,
 'No Content': 204,
 'Reset Content': 205,
 'Partial Content': 206,
 'Multiple Choices': 300,
 'Moved Permanently': 301,
 'Found': 302,
 'See Other': 303,
 'Not Modified': 304,
 'Temporary Redirect': 307,
 'Permanent Redirect': 308,
 'Bad Request': 400,
 'Unauthorized': 401,
 'Forbidden': 403,
 'Not Found': 404,
 'Method Not Allowed': 405,
 'Not Acceptable': 406,
 'Proxy Authentication Required': 407,
 'Request Timeout': 408,
 'Conflict': 409,
 'Gone': 410,
 'Length Required': 411,
 'Precondition Failed': 412,
 'Payload Too Large': 413,
 'URI Too Long': 414,
 'Unsupported Media Type': 415,
 'Range Not Satisfiable': 416,
 'Expectation Failed': 417,
 "I am a teapot": 418,
 'Unprocessable Entity': 422,
 'Upgrade Required': 426,
 'Precondition Required': 428,
 'Too Many Requests': 429,
 'Request Header Fields Too Large': 431,
 'Unavailable For Legal Reasons': 451,
 'Internal Server Error': 500,
 'Not Implemented': 501,
 'Bad Gateway': 502,
 'Service Unavailable': 503,
 'Gateway Timeout': 504,
 'HTTP Version Not Supported': 505,
 'Network Authentication Required': 511
}

def code2reason(code):
    return(REASONS[code])


def reason2code(reason,mode='loose'):
    if(mode=="strict"):
        return(REASONS_MD[reason])
    else:
        rslt = []
        reason = reason.replace(" ","")
        reason = reason.lower()
        for key in REASONS_MD:
            k = key.replace(" ","")
            k = k.lower()
            cond1 = (k == reason)
            cond2 = (k in reason)
            cond3 = (reason in k)
            lngth = min(k.__len__(),reason.__len__())
            mdis = lngth // 3
            dis = edis.distance(reason,k)
            if(dis <= mdis):
                cond4 = True
            else:
                cond4 = False
            cond = (cond1 | cond2 | cond3 | cond4)
            if(cond):
                v = REASONS_MD[key]
                rslt.append((key,v))
            else:
                pass
        if(rslt.__len__()==1):
            return(rslt[0][1])
        else:
            return(rslt)
                 







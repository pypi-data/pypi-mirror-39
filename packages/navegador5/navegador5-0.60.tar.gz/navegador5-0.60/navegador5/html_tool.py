import html
import re

def gen_html_entity_dict(self,end=128):
    html_entity_dict ={}
    html_entity_dict['&lt;'] = '<'
    html_entity_dict['&gt;'] = '>'
    html_entity_dict['&amp;'] = '&'
    html_entity_dict['&quot;'] = '"'
    html_entity_dict['&nbsp;'] = chr(160)
    html_entity_dict['&emsp;'] = chr(8195)
    html_entity_dict['&ensp;'] = chr(8194)
    html_entity_dict['&trade;'] = chr(8482)
    html_entity_dict['&copy;'] = chr(169)
    html_entity_dict['&reg;'] = chr(174)
    for i in range(0,end):
        html_entity_dict[chr(i)] = '&#{0};'.format(str(i))
        html_entity_dict['&#{0};'.format(str(i))] = chr(i)
        return(html_entity_dict)

def html_number_escape_char(ch):
    '''
        >>> es = html_number_escape_char('a')
        >>> es
        '&#97;'
        >>> html.unescape(es)
        'a'
        >>> es = html_number_escape_char('用')
        >>> es
        '&#29992;'
        >>> html.unescape(es)
        '用'
        >>> 
    '''
    num = utils.char_str_to_unicode_num(ch)
    escaped = ''.join(('&#',str(num),';'))
    return(escaped)

def html_number_escape_str(s):
    '''
        >>> 
        >>> ess = html_number_escape_str('加强武器')
        >>> ess
        '&#21152;&#24378;&#27494;&#22120;'
        >>> html.unescape(ess)
        '加强武器'
        >>> ess = html_number_escape_str('xyzw')
        >>> ess
        '&#120;&#121;&#122;&#119;'
        >>> html.unescape(ess)
        'xyzw'
        >>> 
    '''
    escaped = ''
    for i in range(0,s.__len__()):
        esch = html_number_escape_char(s[i])
        escaped = ''.join((escaped,esch))
    return(escaped)

def get_block_op_pairs(pairs_str):
    '''
        # >>> get_block_op_pairs("{}[]")  
        # {1: ('{', '}'), 2: ('[', ']')}
        # >>> get_block_op_pairs("{}[]()")
        # {1: ('{', '}'), 2: ('[', ']'), 3: ('(', ')')}
        # >>> get_block_op_pairs("{}[]()<>")
        # {1: ('{', '}'), 2: ('[', ']'), 3: ('(', ')'), 4: ('<', '>')}
    '''
    pairs_str_len = pairs_str.__len__()
    pairs_len = pairs_str_len // 2
    pairs_dict = {}
    for i in range(1,pairs_len +1):
        pairs_dict[i] = pairs_str[i*2-2],pairs_str[i*2-1]
    return(pairs_dict)

def get_jdict_token_set(block_op_pairs_dict=get_block_op_pairs('{}[]()'),**kwargs):
    def get_slashxs(ch):
        d = {1:ch}
        if('\\' in d.__str__()):
            return(True)
        else:
            return(False)
    if('spaces' in kwargs):
        spaces = kwargs['spaces']
    else:
        spaces = [' ','\t']
    if('colons' in kwargs):
        colons = kwargs['colons']
    else:
        colons = [':']
    if('commas' in kwargs):
        commas = kwargs['commas']
    else:
        commas = [',']
    if('line_sps' in kwargs):
        line_sps = kwargs['line_sps']
    else:
        line_sps = ['\r','\n']
    if('quotes' in kwargs):
        quotes = kwargs['quotes']
    else:
        quotes = ['"',"'"]
    if('path_sps' in kwargs):
        path_sps = kwargs['path_sps']
    else:
        path_sps = ['/']
    #html.unescape("{1: '&#8;&#2;'}")  "{1: ''}"
    if('slashxs' in kwargs):
        slashxs = kwargs['slashxs']
    else:
        slashxs = []
        for i in range(0,256):
            if(get_slashxs(chr(i))):
                slashxs.append(chr(i))
            else:
                pass
    if('ctrls' in kwargs):
        ctrls = kwargs['ctrls']
    else:
        ctrls = ['\x00', '\x01', '\x02', '\x03', '\x04', '\x05', '\x06', '\x07', '\x08', '\t', '\n', '\x0b', '\x0c', '\r', '\x0e', '\x0f', '\x10', '\x11', '\x12', '\x13', '\x14', '\x15', '\x16', '\x17', '\x18', '\x19', '\x1a', '\x1b', '\x1c', '\x1d', '\x1e', '\x1f']
    for each in spaces:
        try:
            ctrls.remove(each)
        except:
            pass
        else:
            pass
    for each in colons:
        try:
            ctrls.remove(each)
        except:
            pass
        else:
            pass
    for each in commas:
        try:
            ctrls.remove(each)
        except:
            pass
        else:
            pass
    for each in line_sps:
        try:
            ctrls.remove(each)
        except:
            pass
        else:
            pass
    for each in quotes:
        try:
            ctrls.remove(each)
        except:
            pass
        else:
            pass
    for each in path_sps:
        try:
            ctrls.remove(each)
        except:
            pass
        else:
            pass
    d = {}
    s = set({})
    def add_bi_table(s,d,x):
        for each in x:
            k = each
            v = html_number_escape_str(k)
            d[k] = v
            d[v] = k
            s.add(k)
            s.add(v)
    add_bi_table(s,d,spaces)
    add_bi_table(s,d,colons)
    add_bi_table(s,d,commas)
    add_bi_table(s,d,line_sps)
    add_bi_table(s,d,quotes)
    add_bi_table(s,d,path_sps)
    for i in range(1,block_op_pairs_dict.__len__()+1):
        s.add(block_op_pairs_dict[i][0])
        s.add(block_op_pairs_dict[i][1])
        recover_token_l = html_number_escape_str(block_op_pairs_dict[i][0])
        recover_token_r = html_number_escape_str(block_op_pairs_dict[i][1])
        s.add(recover_token_l)
        s.add(recover_token_r)
        d[block_op_pairs_dict[i][0]] = recover_token_l 
        d[block_op_pairs_dict[i][1]] = recover_token_r
        d[recover_token_l] = block_op_pairs_dict[i][0]
        d[recover_token_r] = block_op_pairs_dict[i][1]
    return({'token_set':s,'replace_ref_dict':d})

def convert_token_in_quote(j_str,block_op_pairs_dict=get_block_op_pairs('{}[]()'),**kwargs):
    if('spaces' in kwargs):
        spaces = kwargs['spaces']
    else:
        spaces = [' ','\t']
    if('colons' in kwargs):
        colons = kwargs['colons']
    else:
        colons = [':']
    if('commas' in kwargs):
        commas = kwargs['commas']
    else:
        commas = [',']
    if('line_sps' in kwargs):
        line_sps = kwargs['line_sps']
    else:
        line_sps = ['\r','\n']
    if('quotes' in kwargs):
        quotes = kwargs['quotes']
    else:
        quotes = ['"',"'"]
    if('path_sps' in kwargs):
        path_sps = kwargs['path_sps']
    else:
        path_sps = ['/']
    temp = get_jdict_token_set(block_op_pairs_dict,spaces=spaces,colons=colons,commas=commas,line_sps=line_sps,quotes=quotes,path_sps=path_sps)
    token_set = temp['token_set']
    replace_ref_dict = temp['replace_ref_dict']
    # ----------------------------------------------------------------- #
    #Q: QUOTE
    #PISIQ: PRE_IS_SLASH_IN_QUOTE
    
    
    #SQ:SINGLE_QUOTE
    #DQ:DOUBLE_QUOTE
    #PISIQ:PRE_IS_SLASH_IN_SQ
    #PISID:PRE_IS_SLASH_IN_DQ
    #input_symbol_array = ['"',"'",'\\']
    #states_array = ["INIT","Q","PIIQ"]
    
    def do_replace(ch):
        if(ch in token_set):
            ch = replace_ref_dict[ch]
        return(ch)
    
    regex_quotes = []
    regex_nonqses = []
    non_regex_quote_str = '[^'
    
    for i in range(0,quotes.__len__()):
        regex_quote_str = ''.join(('[',quotes[i],']'))
        regex_quote = re.compile(regex_quote_str)
        regex_quotes.append(regex_quote)
        regex_nonqs_str = ''.join(('[^',quotes[i],'\\\\]'))
        regex_nonqs = re.compile(regex_nonqs_str)
        regex_nonqses.append(regex_nonqs)
        non_regex_quote_str = ''.join((non_regex_quote_str,quotes[i]))
    
    non_regex_quote_str = ''.join((non_regex_quote_str,']'))
    non_regex_quote = re.compile(non_regex_quote_str)
    # ############################
    fsm_dict = {
        ("INIT",non_regex_quote) : (None,"INIT")
    }
    for i in range(0,regex_quotes.__len__()):
        k = ("INIT",regex_quotes[i])
        sn = ''.join(("Q",'_',str(i)))
        v = (None,sn)
        fsm_dict[k] = v
        k = (sn,regex_quotes[i])
        v = (None,"INIT")
        fsm_dict[k] = v
        pisiq = ''.join(("PISIQ",'_',str(i)))
        k = (sn,re.compile("\\\\"))
        v = (None,pisiq)
        fsm_dict[k] = v
        k = (pisiq,re.compile("."))
        v = (do_replace,sn)
        fsm_dict[k] = v
        k = (sn,regex_nonqses[i])
        v = (do_replace,sn)
        fsm_dict[k] = v
        
    # #################################
    def search_fsm(curr_state,input_symbol,fsm_dict):
        for key in fsm_dict:
            if(key[0] == curr_state):
                if(key[1].search(input_symbol)):
                    return(fsm_dict[key])
                else:
                    pass
            else:
                pass
        return(None)
    curr_state = "INIT"
    rslt = ''
    for i in range(0,j_str.__len__()):
        input_symbol = j_str[i]
        temp = search_fsm(curr_state,input_symbol,fsm_dict)
        action = temp[0]
        if(action):
            ch = action(input_symbol)
        else:
            ch = input_symbol
        rslt = ''.join((rslt,ch))
        curr_state = temp[1]
    return(rslt)
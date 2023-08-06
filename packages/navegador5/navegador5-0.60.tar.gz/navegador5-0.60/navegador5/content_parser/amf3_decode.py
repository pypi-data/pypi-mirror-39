import struct

##-----------------------------------------------------------------##
##3.1 AMF 3 Data Types Overview                                    ##
##-----------------------------------------------------------------##

amf3_Data_Types = {
    'name-to-marker':{
        'undefined-marker':b'\x00',
        'null-marker':b'\x01',
        'false-marker':b'\x02',
        'true-marker':b'\x03',  
        'integer-marker':b'\x04',  
        'double-marker':b'\x05',
        'string-marker':b'\x06',
        'xml-doc-marker':b'\x07',
        'date-marker':b'\x08',
        'array-marker':b'\x09',
        'object-marker': b'\x0A',
        'xml-marker':b'\x0B',
        'byte-array-marker':b'\x0C',
        'vector-int-marker' : b'\x0D',
        'vector-uint-marker' : b'\x0E',
        'vector-double-marker' : b'\x0F',
        'vector-object-marker' : b'\x10',
        'dictionary-marker' : b'\x11'
    },
    'marker-to-name': {
        b'\x00':  'undefined-marker',
        b'\x01':  'null-marker',
        b'\x02':  'false-marker',
        b'\x03':  'true-marker',
        b'\x04':  'integer-marker',
        b'\x05':  'double-marker',
        b'\x06':  'string-marker',
        b'\x07':  'xml-doc-marker',
        b'\x08':  'date-marker',
        b'\x09':  'array-marker',
        b'\x0A':  'object-marker',
        b'\x0B':  'xml-marker',
        b'\x0C':  'byte-array-marker',
        b'\x0D':  'vector-int-marker',
        b'\x0E':  'vector-uint-marker',
        b'\x0F':  'vector-double-marker',
        b'\x10':  'vector-object-marker',
        b'\x11':  'dictionary-marker'
    }
}

##-----------------------------------------------------------------##
##1.3 Basic Rules                                                  ##
##-----------------------------------------------------------------##

# 1.3.1 amf3_U8 :
# An unsigned byte, 8-bits of data, an octet
# unhandled_Bytes is <class 'bytes'> 
def amf3_Get_U8_raw(unhandled_Bytes):
    handled_Bytes = b''
    (unhandled_Bytes,U8_raw) = (unhandled_Bytes[1:],unhandled_Bytes[0:1])
    return((unhandled_Bytes,U8_raw))

def amf3_U8_to_INT(U8_raw):
    return(U8_raw[0])

def amf3_INT_to_U8(INT):
    high = '{0:0>2}'.format(hex(INT).lstrip('0x'))[0:2]
    high = int(high,16)
    return(chr(high).encode('latin-1'))

# 1.3.2 amf3_U16 : 
# An unsigned 16-bit integer in big endian (network) byte order 
def amf3_Get_U16_raw(unhandled_Bytes):
    handled_Bytes = b''
    (unhandled_Bytes,U16_raw) = (unhandled_Bytes[2:],unhandled_Bytes[0:2])
    return((unhandled_Bytes,U16_raw))

def amf3_U16_to_INT(U16_raw):
    return(struct.unpack('!H',U16_raw)[0])

def amf3_INT_to_U16(INT):
    return(struct.pack('!H',INT))

# 1.3.3 amf3_U32
# An unsigned 32-bit integer in big endian (network) byte order 

def amf3_Get_U32_raw(unhandled_Bytes):
    handled_Bytes = b''
    (unhandled_Bytes,U32_raw) = (unhandled_Bytes[4:],unhandled_Bytes[0:4])
    return((unhandled_Bytes,U32_raw))

def amf3_U32_to_INT(U32_raw):
    return(struct.unpack('!I',U32_raw)[0])

def amf3_INT_to_U32(INT):
    return(struct.pack('!I',INT))

# 1.3.4 amf3_DOUBLE :
# 8 byte IEEE-754 double precision floating point value in network byte order (sign bit in low memory). 

def amf3_Get_DOUBLE_raw(unhandled_Bytes):
    handled_Bytes = b''
    (unhandled_Bytes,DOUBLE_raw) = (unhandled_Bytes[8:],unhandled_Bytes[0:8])
    return((unhandled_Bytes,DOUBLE_raw))

def amf3_DOUBLE_to_Float(DOUBLE_raw):
    return(struct.unpack('!d',DOUBLE_raw)[0])
    
def amf3_Get_Date_Time(DOUBLE_raw):
    since_epoch = amf3_DOUBLE_to_Float(DOUBLE_raw)
    date='Wed, 11 Apr 2012 09:37:05 +0800'
    dd=datetime.datetime.strptime(date,'%a, %d %b %Y %H:%M:%S %z')
    current_DD = dd.fromtimestamp(since_epoch)
    return(current_DD.strftime("%Y-%m-%d %H:%M:%S:%f"))

# 1.3.5 MB = A megabyte or 1048576 bytes.
amf3_MB = 1048576

# 1.3.6
# In ABNF syntax, [RFC3629] describes UTF-8 as follows:   
# UTF8-char = UTF8-1 | UTF8-2 | UTF8-3 | UTF8-4 
# UTF8-1 = %x00-7F 
# UTF8-2 = %xC2-DF UTF8-tail 
# UTF8-3 = %xE0 %xA0-BF UTF8-tail | %xE1-EC 2(UTF8-tail) | \
         # %xED %x80-9F UTF8-tail | %xEE-EF 2(UTF8-tail) 
# UTF8-4 = %xF0 %x90-BF 2(UTF8-tail) | %xF1-F3 3(UTF8-tail) | \
         # %xF4 %x80-8F 2(UTF8-tail) 
# UTF8-tail = %x80-BF 
def amf3_Get_UTF8_char_Raw(unhandled_Bytes):
    if(unhandled_Bytes[0] < 128):
        if(unhandled_Bytes[0] < 128):
            handled_Bytes = unhandled_Bytes[0:1]
            unhandled_Bytes = unhandled_Bytes[1:]
            return((unhandled_Bytes,handled_Bytes))
        else:
            return(None)
    elif((unhandled_Bytes[0] > 193) & (unhandled_Bytes[0] < 224)):
        if((unhandled_Bytes[0] > 193) & (unhandled_Bytes[0] < 224) & (unhandled_Bytes[1] > 127) & (unhandled_Bytes[1] < 192)):
            handled_Bytes = unhandled_Bytes[0:2]
            unhandled_Bytes = unhandled_Bytes[2:]
            return((unhandled_Bytes,handled_Bytes))
        else:
            return(None)
    elif((unhandled_Bytes[0] > 223) & (unhandled_Bytes[0] < 240)):
        if((unhandled_Bytes[0] == 224) & (unhandled_Bytes[1] > 159) & (unhandled_Bytes[1] < 192) & (unhandled_Bytes[2] > 127) & (unhandled_Bytes[2] < 192)):
            handled_Bytes = unhandled_Bytes[0:3]
            unhandled_Bytes = unhandled_Bytes[3:]
            return((unhandled_Bytes,handled_Bytes))
        elif((unhandled_Bytes[0] > 224) &(unhandled_Bytes[0] < 237) & (unhandled_Bytes[1] > 127) & (unhandled_Bytes[1] < 192) & (unhandled_Bytes[2] > 127) & (unhandled_Bytes[2] < 192)):
            handled_Bytes = unhandled_Bytes[0:3]
            unhandled_Bytes = unhandled_Bytes[3:]
            return(unhandled_Bytes,handled_Bytes)
        elif((unhandled_Bytes[0] == 237) & (unhandled_Bytes[1] > 127) & (unhandled_Bytes[1] < 160) & (unhandled_Bytes[2] > 127) & (unhandled_Bytes[2] < 192)):
            handled_Bytes = unhandled_Bytes[0:3]
            unhandled_Bytes = unhandled_Bytes[3:]
            return(unhandled_Bytes,handled_Bytes)
        elif((unhandled_Bytes[0] > 237) &(unhandled_Bytes[0] < 240) & (unhandled_Bytes[1] > 127) & (unhandled_Bytes[1] < 192) & (unhandled_Bytes[2] > 127) & (unhandled_Bytes[2] < 192)):
            handled_Bytes = unhandled_Bytes[0:3]
            unhandled_Bytes = unhandled_Bytes[3:]
            return(unhandled_Bytes,handled_Bytes)
        else:
            return(None)
    elif(unhandled_Bytes[0] > 240):
        if((unhandled_Bytes[0] == 240) & (unhandled_Bytes[1] > 143) & (unhandled_Bytes[1] < 192) & (unhandled_Bytes[2] > 127) & (unhandled_Bytes[2] < 192) & (unhandled_Bytes[3] > 127) & (unhandled_Bytes[3] < 192)):
            handled_Bytes = unhandled_Bytes[0:4]
            unhandled_Bytes = unhandled_Bytes[4:]
            return(unhandled_Bytes,handled_Bytes)
        elif((unhandled_Bytes[0] > 240) &(unhandled_Bytes[0] < 244) & (unhandled_Bytes[1] > 127) & (unhandled_Bytes[1] < 192) & (unhandled_Bytes[2] > 127) & (unhandled_Bytes[2] < 192) & (unhandled_Bytes[3] > 127) & (unhandled_Bytes[3] < 192)):
            handled_Bytes = unhandled_Bytes[0:4]
            unhandled_Bytes = unhandled_Bytes[4:]
            return(unhandled_Bytes,handled_Bytes)
        elif((unhandled_Bytes[0] == 244) & (unhandled_Bytes[1] > 127) & (unhandled_Bytes[1] < 144) & (unhandled_Bytes[2] > 127) & (unhandled_Bytes[2] < 192) & (unhandled_Bytes[3] > 127) & (unhandled_Bytes[3] < 192) ):
            handled_Bytes = unhandled_Bytes[0:4]
            unhandled_Bytes = unhandled_Bytes[4:]
            return(unhandled_Bytes,handled_Bytes)
        else:
            return(None)
    else:
        return(None)

# 1.3.7 UTF-8 = U16 *(UTF8-char)  
# A 16-bit byte-length header implies a theoretical maximum of 65,535 bytes \
# to encode a string in UTF-8 (essentially 64KB).     

def amf3_Get_UTF8_string_Len_Raw(unhandled_Bytes):
    handled_Bytes = b''
    (unhandled_Bytes,count_Raw) = amf3_Get_U16_raw(unhandled_Bytes)
    return((unhandled_Bytes,count_Raw))

def amf3_UTF8_string_Len(UTF8_string_Len_Raw):
    count = amf3_U16_to_INT(UTF8_string_Len_Raw)
    return(count)

def amf3_Get_UTF8_string_Raw(unhandled_Bytes,UTF8_string_Len_Raw):
    count = amf3_U16_to_INT(UTF8_string_Len_Raw)
    handled_Bytes = b''
    for i in range(1,count+1):
        (unhandled_Bytes,UTF8_Char_Raw) = amf3_Get_UTF8_char_Raw(unhandled_Bytes)
        handled_Bytes = handled_Bytes + UTF8_Char_Raw
    return((unhandled_Bytes,handled_Bytes))

def amf3_UTF8_String(UTF8_string_Raw):
    return(UTF8_string_Raw.decode('utf-8'))



# 1.3.8 In ABNF syntax, the variable length unsigned 29-bit integer type is described as follows:
# U29 = U29-1 | U29-2 | U29-3 | U29-4
# U29-1 = %x00-7F
# U29-2 = %x80-FF %x00-7F
# U29-3 = %x80-FF %x80-FF %x00-7F
# U29-4 = %x80-FF %x80-FF %x80-FF %x00-FF

def amf3_Get_U29_raw(unhandled_Bytes):
    U29_raw = b''
    i = 0 
    while(i<4):
        if(unhandled_Bytes[i]<128):
            U29_raw = U29_raw + unhandled_Bytes[i:i+1]
            break
        else:
            U29_raw = U29_raw + unhandled_Bytes[i:i+1]
        i = i + 1
    return((unhandled_Bytes[(i+1):],U29_raw))

def amf3_U29_to_INT(U29_raw):
    len = U29_raw.__len__()
    if(len == 1):
        return(U29_raw[0])
    elif(len == 2):
        seven_1 = (U29_raw[0] - 128 )* 2**7
        seven_2 = U29_raw[1]
        return(seven_1 + seven_2)
    elif(len == 3):
        seven_1 = ( U29_raw[0] - 128 ) * 2**14
        seven_2 = ( U29_raw[1] - 128 ) * 2**7
        seven_3 = U29_raw[2]
        return(seven_1 + seven_2 + seven_3)
    elif(len == 4):
        seven_1 = (U29_raw[0] - 128 ) * (2**22)
        seven_2 = (U29_raw[1] - 128 ) * (2**15)
        seven_3 = (U29_raw[2] - 128 ) * (2**8)
        seven_4 = U29_raw[3]
        return(seven_1 + seven_2 + seven_3 + seven_4)
    else:
        return(None)

def amf3_INT_to_U29(INT):
    bin_Str = bin(INT).lstrip('0b')
    len = bin_Str.__len__()
    if(len < 8):
        new_Bin_Str = '{0:0>8}'.format(bin_Str[0:7])
        new_Bin_Str = '{0:0>2}'.format(hex(int(new_Bin_Str,2)).lstrip('0x'))
        return(new_Bin_Str.encode())
    elif(len < 15):
        seven_1 = '{0:0>8}'.format(bin_Str[0:7])
        seven_2 = '1{0:0>7}'.format(bin_Str[7:14])
        new_Bin_Str = seven_1 + seven_2
        new_Bin_Str = '{0:0>2}'.format(hex(int(new_Bin_Str,2)).lstrip('0x'))
        return(new_Bin_Str.encode())
    elif(len < 22):
        seven_1 = '{0:0>8}'.format(bin_Str[0:7])
        seven_2 = '1{0:0>7}'.format(bin_Str[7:14])
        seven_3 = '1{0:0>7}'.format(bin_Str[14:21])
        new_Bin_Str = seven_1 + seven_2 + seven_3
        new_Bin_Str = '{0:0>2}'.format(hex(int(new_Bin_Str,2)).lstrip('0x'))
        return(new_Bin_Str.encode())
    elif(len < 30):
        seven_1 = '{0:0>8}'.format(bin_Str[0:7])
        seven_2 = '1{0:0>7}'.format(bin_Str[7:14])
        seven_3 = '1{0:0>7}'.format(bin_Str[14:21])
        seven_4 = '{0:0>8}'.format(bin_Str[21:])
        new_Bin_Str = seven_1 + seven_2 + seven_3 + seven_4
        new_Bin_Str = '{0:0>2}'.format(hex(int(new_Bin_Str,2)).lstrip('0x'))
        return(new_Bin_Str.encode())
    else:
        return(None)


# U29S-ref = U29 ; 
# The first (low) bit is a flag with 
# value 0. The remaining 1 to 28 
# significant bits are used to encode a 
# string reference table index (an 
# integer).

# U29S-value = U29 ; The first (low) bit is a flag with 
# value 1. The remaining 1 to 28 
# significant bits are used to encode the 
# byte-length of the UTF-8 encoded 
# representation of the string

def amf3_Decode_U29S(U29_raw):
    int_Little_Endian = U29_raw[-1]
    if(int_Little_Endian % 2 == 0):
        U29S = {}
        U29S['ref'] = amf3_U29_to_INT(U29_raw) // 2
        U29S['value'] = None
    else:
        U29S = {}
        U29S['ref'] = None
        U29S['value'] = (amf3_U29_to_INT(U29_raw)-1) // 2
    return(U29S)

# UTF-8-empty = 0x01  
# The UTF-8-vr empty string which is 
# never sent by reference.

amf3_UTF_8_empty = b'\x01'

# UTF-8-vr = U29S-ref | (U29S-value *(UTF8-char))
# amf3_UTF8_vr =
# {
# 'U29S-raw':
# 'ref':
# 'value':
# 'string-raw':
# 'string'
# }

def amf3_Get_UTF8_vr_Raw(unhandled_Bytes):
    vr = {}
    step = amf3_Get_U29_raw(unhandled_Bytes)
    unhandled_Bytes = step[0]
    U29_raw = step[1]
    vr['U29S-raw'] = U29_raw
    vr['ref'] = amf3_Decode_U29S(U29_raw)['ref']
    vr['value'] = amf3_Decode_U29S(U29_raw)['value']
    string = b''
    if(vr['value'] == None):
        vr['value'] = 0
    for i in range(1,vr['value']+1):
        step = amf3_Get_UTF8_char_Raw(unhandled_Bytes)
        unhandled_Bytes = step[0]
        string = string + step[1]
    vr['string-raw'] = string
    vr['string'] = string.decode('utf-8')
    return((unhandled_Bytes,vr))


# assoc-value = UTF-8-vr value-type 
def amf3_Get_Assoc_Value_Raw(unhandled_Bytes):
    assoc_Value = {}
    step = amf3_Get_UTF8_vr_Raw(unhandled_Bytes)
    unhandled_Bytes = step[0]
    assoc_Value['name'] = step[1]
    if(assoc_Value['name']['U29S-raw'] == amf3_UTF_8_empty):
        assoc_Value['body'] = None
    else:
        step = amf3_Get_Value_Type(unhandled_Bytes,amf3_Data_Types,U29O_traits_Ext_U8_count)
        unhandled_Bytes = step[0]
        assoc_Value['body'] = step[1]
    return((unhandled_Bytes,assoc_Value))

# U29O-ref = U29 ;   -0
# The first (low) bit is a flag  
# ; (representing whether an instance  
# ; follows) with value 0 to imply that  
# ; this is not an instance but a  
# ; reference. The remaining 1 to 28  
# ; significant bits are used to encode an 
# ; object reference index (an integer).     
# U29O-traits-ref = U29  -01
# ; The first (low) bit is a flag with  
# ; value 1. The second bit is a flag  
# ; (representing whether a trait  
# ; reference follows) with value 0 to  
# ; imply that this objects traits are  
# ; being sent by reference. The remaining 
# ; 1 to 27 significant bits are used to  
# ; encode a trait reference index (an  
# ; integer).     
# U29O-traits-ext = U29  -111
# ; The first (low) bit is a flag with  
# ; value 1. The second bit is a flag with 
# ; value 1. The third bit is a flag with  
# ; value 1. The remaining 1 to 26  
# ; significant bits are not significant  
# ; (the traits member count would always  
# ; be 0).     
# U29O-traits = U29  -011
# ; The first (low) bit is a flag with  
# ; value 1. The second bit is a flag with 
# ; value 1. The third bit is a flag with  
# ; value 0.  The fourth bit is a flag  
# ; specifying whether the type is  
# ; dynamic. A value of 0 implies not  
# ; dynamic, a value of 1 implies dynamic. 
# ; Dynamic types may have a set of name  
# ; value pairs for dynamic members after  
# ; the sealed member   section. The  
# ; remaining 1 to 25 significant bits are 
# ; used to encode the number of sealed  
# ; traits member names that follow after  
# ; the class name (an integer).

def amf3_Decode_U29O(U29_raw):
    int_Little_Endian = U29_raw[-1]
    U29O = {}
    U29O['ref'] = None
    U29O['traits-ref'] = None
    U29O['traits-ext'] = None
    U29O['traits'] = None
    if(int_Little_Endian & 1 == 0):
        U29O['ref'] = amf3_U29_to_INT(U29_raw) // 2
        return(U29O)
    elif(int_Little_Endian & 3 == 1):
        U29O['traits-ref'] = (amf3_U29_to_INT(U29_raw) - 1) // 4
        return(U29O)
    elif(int_Little_Endian & 7 == 3):
        temp = (amf3_U29_to_INT(U29_raw) - 3) // 16
        U29O['traits'] = {}
        U29O['traits']['dynamic'] = False
        U29O['traits']['sealed-names-count'] = temp
        if(int_Little_Endian & 15 == 11):
            temp = (amf3_U29_to_INT(U29_raw) - 11) // 16
            U29O['traits']['dynamic'] = True
            U29O['traits']['sealed-names-count'] = temp
        return(U29O)
    elif(int_Little_Endian & 7 == 7):
        U29O['traits-ext'] = (amf3_U29_to_INT(U29_raw) - 3) // 8
        return(U29O)
    else:
        return(None)

# class-name = UTF-8-vr    
# ; Note: use the empty string for  
# ; anonymous classes.     
# dynamic-member = UTF-8-vr value-type  
# ; Another dynamic member follows  
# ; until the string-type is the  
# ; empty string.

def amf3_Get_Dynamic_Member_Raw(unhandled_Bytes,amf3_Data_Types,U29O_traits_Ext_U8_count):
    Dynamic_Member = {}
    step = amf3_Get_UTF8_vr_Raw(unhandled_Bytes)
    unhandled_Bytes = step[0]
    Dynamic_Member['name'] = step[1]
    if(Dynamic_Member['name']['U29S-raw'] == amf3_UTF_8_empty):
        Dynamic_Member['body'] = None
    else:
        step = amf3_Get_Value_Type(unhandled_Bytes,amf3_Data_Types,U29O_traits_Ext_U8_count)
        unhandled_Bytes = step[0]
        Dynamic_Member['body'] = step[1]
    return((unhandled_Bytes,Dynamic_Member))

# value_Type = {
# 'marker-raw':
# 'marker':
# 'body':
# }
def amf3_Get_Value_Type(unhandled_Bytes,amf3_Data_Types,U29O_traits_Ext_U8_count):
    step = amf3_Get_U8_raw(unhandled_Bytes)
    unhandled_Bytes = step[0]
    marker_Raw = step[1]
    VT = {}
    VT['marker-raw'] = marker_Raw
    VT['marker'] = amf3_Data_Types['marker-to-name'][marker_Raw]
    step = amf3_Get_Value_Type_Body(unhandled_Bytes,marker_Raw,amf3_Data_Types,U29O_traits_Ext_U8_count)
    unhandled_Bytes = step[0]
    VT['body'] = step[1]
    return((unhandled_Bytes,VT))

##-----------------------------------------------------------------##
##                                                                 ##
##-----------------------------------------------------------------##


def amf3_Get_Value_Type_Body(unhandled_Bytes,marker_Raw,amf3_Data_Types,U29O_traits_Ext_U8_count):
    # undefined-type = undefined-marker
    if(marker_Raw == amf3_Data_Types['name-to-marker']['undefined-marker']):
        return((unhandled_Bytes,b''))
    # null-type = null-marker
    elif(marker_Raw == amf3_Data_Types['name-to-marker']['null-marker']):
        return((unhandled_Bytes,b''))
    # false-type = false-marker
    elif(marker_Raw == amf3_Data_Types['name-to-marker']['false-marker']):
        return((unhandled_Bytes,b''))
    # true-type = true-marker
    elif(marker_Raw == amf3_Data_Types['name-to-marker']['true-marker']):
        return((unhandled_Bytes,b''))
    # integer-type = integer-marker U29
    elif(marker_Raw == amf3_Data_Types['name-to-marker']['integer-marker']):
        integer_Type = {}
        step = amf3_Get_U29_raw(unhandled_Bytes)
        unhandled_Bytes = step[0]
        integer_Type['U29-raw'] = step[1]
        integer_Type['INT'] = amf3_U29_to_INT(integer_Type['U29-raw'])
        return((unhandled_Bytes,integer_Type))
    # double-type = double-marker DOUBLE
    elif(marker_Raw == amf3_Data_Types['name-to-marker']['double-marker']):
        double_Type = {}
        step = amf3_Get_DOUBLE_raw(unhandled_Bytes)
        unhandled_Bytes = step[0]
        double_Type['DOUBLE-raw'] = step[1]
        double_Type['Float'] = amf3_DOUBLE_to_Float(double_Type['DOUBLE-raw'])
        return((unhandled_Bytes,double_Type))
    # string-type = string-marker UTF-8-vr
    elif(marker_Raw == amf3_Data_Types['name-to-marker']['string-marker']):
        step = amf3_Get_UTF8_vr_Raw(unhandled_Bytes)
        unhandled_Bytes = step[0]
        string_Type = step[1]
        return((unhandled_Bytes,string_Type))
    # xml-doc-type = xml-doc-marker (U29O-ref | (U29X-value *(UTF8-char)))
    elif(marker_Raw == amf3_Data_Types['name-to-marker']['xml-doc-marker']):
        step = amf3_Get_UTF8_vr_Raw(unhandled_Bytes)
        unhandled_Bytes = step[0]
        xml_Doc_Type = step[1]
        return((unhandled_Bytes,xml_Doc_Type))
    # date-type = date-marker (U29O-ref | (U29D-value date-time))
    # date_Type =
    # {
    # 'U29-raw':
    # 'ref':
    # 'value':
    # 'data-time-raw':
    # 'data-time':
    # }
    elif(marker_Raw == amf3_Data_Types['name-to-marker']['date-marker']):
        date_Type = {}
        step = amf3_Get_U29_raw(unhandled_Bytes)
        unhandled_Bytes = step[0]
        date_Type['U29-raw'] = step[1]
        date_Type['ref'] = amf3_Decode_U29S(step[1])['ref']
        date_Type['value'] = amf3_Decode_U29S(step[1])['value']
        if(date_Type['value'] == None):
            date_Type['data-time-raw'] = None
            date_Type['data-time'] = None
        else:
            step = amf3_Get_DOUBLE_raw(unhandled_Bytes)
            unhandled_Bytes = step[0]
            date_Type['data-time-raw'] = step[1]
            date_Type['data-time'] = amf3_Get_Date_Time(date_Type['data-time-raw'])
        return((unhandled_Bytes,date_Type))
    # array-type = array-marker (U29O-ref | (U29A-value  (UTF-8-empty | *(assoc-value) UTF-8-empty)  *(value-type)))
    # array-type = {
    # 'U29-raw':
    # 'ref':
    # 'dense-count':
    # 'associative':{
    #                1:
    #                ......
    #                na:
    #               }
    # 'dense':{
    #                1:
    #                ......
    #                nd:
    #               }
    # }
    elif(marker_Raw == amf3_Data_Types['name-to-marker']['array-marker']):
        array_Type = {}
        step = amf3_Get_U29_raw(unhandled_Bytes)
        unhandled_Bytes = step[0]
        array_Type['U29-raw'] = step[1]
        array_Type['ref'] = amf3_Decode_U29S(step[1])['ref']
        array_Type['dense-count'] = amf3_Decode_U29S(step[1])['value']
        array_Type['associative'] = {}
        assoc_Seq = 1
        step = amf3_Get_Assoc_Value_Raw(unhandled_Bytes)
        unhandled_Bytes = step[0]
        array_Type['associative'][assoc_Seq] = step[1]
        while(not(step[1] == amf3_UTF_8_empty)):
            step = amf3_Get_Assoc_Value_Raw(unhandled_Bytes)
            unhandled_Bytes = step[0]
            array_Type['associative'][assoc_Seq] = step[1]
            assoc_Seq = assoc_Seq + 1
        array_Type['dense'] = {}
        for i in range(1,array_Type['dense-count'] + 1):
            step = amf3_Get_Value_Type_Raw(unhandled_Bytes)
            unhandled_Bytes = step[0]
            array_Type['dense'][i] = step[1]
        return((unhandled_Bytes,array_Type))
    # object-type = object-marker (U29O-ref | (U29O-traits-ext class-name *(U8)) | U29O-traits-ref | (U29O- traits class-name *(UTF-8-vr))) *(value-type) *(dynamic-member)
    # object-type = {
    # 'U29-raw':
    # 'ref':
    # 'traits-ref':
    # 'traits-ext':
    # 'traits':{
    #           'dynamic':
    #           'sealed-names-count':
    # }
    # 'class-name':
    # 'sealed-names':{
    #                1:
    #                ......
    #                ns:
    #               }
    # 'sealed-value-types':{
    #                1:
    #                ......
    #                ns:
    #               }
    # 'dynamic-members':{
    #                1:
    #                ......
    #                nd:
    #               }
    # }
    elif(marker_Raw == amf3_Data_Types['name-to-marker']['object-marker']):
        object_Type = {}
        step = amf3_Get_U29_raw(unhandled_Bytes)
        unhandled_Bytes = step[0]
        object_Type['U29-raw'] = step[1]
        temp = amf3_Decode_U29O(object_Type['U29-raw'])
        object_Type['ref'] = temp['ref']
        object_Type['traits-ref'] = temp['traits-ref']
        object_Type['traits-ext'] = temp['traits-ext']
        object_Type['traits'] = temp['traits']
        object_Type['class-name'] = None
        object_Type['traits-ext-U8s'] = None
        object_Type['sealed-names'] = None
        object_Type['sealed-value-types'] = None
        object_Type['dynamic-members'] = None
        if(not(object_Type['ref']== None)):
            return((unhandled_Bytes,object_Type))
        elif(not(object_Type['traits-ref']== None)):
            return((unhandled_Bytes,object_Type))
        elif(not(object_Type['traits-ext']== None)):
            step = amf3_Get_UTF8_vr_Raw(unhandled_Bytes)
            unhandled_Bytes = step[0]
            object_Type['class-name'] = step[1]
            for i in range(1,U29O_traits_Ext_U8_count+1):
                step = amf3_Get_U8_raw(unhandled_Bytes)
                unhandled_Bytes = step[0]
                object_Type['traits-ext-U8s'] = object_Type['traits-ext-U8s'] + step[1]
            return((unhandled_Bytes,object_Type))
        elif(not(object_Type['traits']== None)):
            step = amf3_Get_UTF8_vr_Raw(unhandled_Bytes)
            unhandled_Bytes = step[0]
            object_Type['class-name'] = step[1]
            object_Type['sealed-names'] = {}
            for i in range(1,object_Type['traits']['sealed-names-count']+1):
                step = amf3_Get_UTF8_vr_Raw(unhandled_Bytes)
                unhandled_Bytes = step[0]
                object_Type['sealed-names'][i] = step[1]
            object_Type['sealed-value-types'] = {}
            for i in range(1,object_Type['traits']['sealed-names-count']+1):
                step = amf3_Get_Value_Type(unhandled_Bytes,amf3_Data_Types,U29O_traits_Ext_U8_count)
                unhandled_Bytes = step[0]
                object_Type['sealed-value-types'][i] = step[1]
            if(object_Type['traits']['dynamic']):
                object_Type['dynamic-members'] = {}
                dynamic_Seq = 1
                step = amf3_Get_Dynamic_Member_Raw(unhandled_Bytes,amf3_Data_Types,U29O_traits_Ext_U8_count)
                unhandled_Bytes = step[0]
                object_Type['dynamic-members'][dynamic_Seq] = step[1]
                while(not(step[1]['name']['U29S-raw'] == amf3_UTF_8_empty)):
                    dynamic_Seq = dynamic_Seq + 1
                    step = amf3_Get_Dynamic_Member_Raw(unhandled_Bytes,amf3_Data_Types,U29O_traits_Ext_U8_count)
                    unhandled_Bytes = step[0]
                    object_Type['dynamic-members'][dynamic_Seq] = step[1]
            return((unhandled_Bytes,object_Type))
        else:
            return(None)
    # xml-type = xml-marker (U29O-ref |  (U29X-value *(UTF8-char)))
    elif(marker_Raw == amf3_Data_Types['name-to-marker']['xml-marker']):
        step = amf3_Get_UTF8_vr_Raw(unhandled_Bytes)
        unhandled_Bytes = step[0]
        xml_Type = step[1]
        return((unhandled_Bytes,xml_Type))
    # bytearray-type = bytearray-marker (U29O-ref | U29B-value *(U8))
    # bytearray_Type = {
    # 'ref':
    # 'value':
    # 'bytes-array':
    # }
    elif(marker_Raw == amf3_Data_Types['name-to-marker']['bytearray-type']):
        bytearray_Type = {}
        bytearray_Type['ref'] = None
        bytearray_Type['value'] = None
        bytearray_Type['bytes-array'] = b''
        step = amf3_Get_U29_raw(unhandled_Bytes)
        unhandled_Bytes = step[0]
        U29B = amf3_Decode_U29S(step[1])
        if(not(U29B['ref']==None)):
            bytearray_Type['ref'] = U29B['ref']
        else:
            bytearray_Type['value'] = U29B['value']
            for i in range(1,bytearray_Type['value'] + 1):
                step = amf3_Get_U8_raw(unhandled_Bytes)
                unhandled_Bytes = step[0]
                bytearray_Type['value'] = bytearray_Type['value'] + step[1]
        return((unhandled_Bytes,bytearray_Type))
    # vector-object-type = vector-object-marker (U29O-ref |  U29V-value fixed-vector object-type-name *(value-type)) 
    elif(marker_Raw == amf3_Data_Types['name-to-marker']['vector-type']):
        vector_Type = {}
        step = amf3_Get_U29_raw(unhandled_Bytes)
        unhandled_Bytes = step[0]
        U29V = amf3_Decode_U29S(step[1])
        vector_Type['ref'] = U29V['ref']
        vector_Type['item-count'] = U29V['value']
        step = amf3_Get_U8_raw(unhandled_Bytes)
        unhandled_Bytes = step[0]
        vector_Type['fixed-vector'] = step[1]
        step = amf3_Get_UTF8_vr_Raw(unhandled_Bytes)
        unhandled_Bytes = step[0]
        vector_Type['object-type-name'] = step[1]
        vector_Type['vector-int-type'] = {}
        vector_Type['vector-uint-type'] = {}
        vector_Type['vector-double-type'] = {}
        vector_Type['vector-object-type'] = {}
        if(vector_Type['fixed-vector'] == b'\x01'):
            if(vector_Type['object-type-name'] == 'int'):
                for i in range(1,vector_Type['item-count']+1):
                    step = amf3_Get_U32_raw(unhandled_Bytes)
                    unhandled_Bytes = step[0]
                    vector_Type['vector-int-type'][i] = step[1]
            elif(vector_Type['object-type-name'] == 'uint'):
                for i in range(1,vector_Type['item-count']+1):
                    step = amf3_Get_U32_raw(unhandled_Bytes)
                    unhandled_Bytes = step[0]
                    vector_Type['vector-uint-type'][i] = step[1]
            elif(vector_Type['object-type-name'] == 'double'):
                for i in range(1,vector_Type['item-count']+1):
                    step = amf3_Get_U32_raw(unhandled_Bytes)
                    unhandled_Bytes = step[0]
                    vector_Type['vector-double-type'][i] = step[1]
            else:
                pass
        elif(vector_Type['fixed-vector'] == b'\x00'):
            for i in range(1,vector_Type['item-count']+1):
                step = amf3_Get_Value_Type(unhandled_Bytes)
                unhandled_Bytes = step[0]
                vector_Type['vector-object-type'][i] = step[1]
        else:
             pass
        return((unhandled_Bytes,vector_Type))
    # dictionary-type = dictionary-marker (U29O-ref |  U29Dict-value weak-keys *(entry-key  entry-value))
    # dictionary_Type = 
    # {
    #  'ref':
    #  'value':
    #  'weak-keys':
    #  'entry':{
    #           1:{'key':,'value':}
    #           ne:{'key':,'value':}
    #          }
    elif(marker_Raw == amf3_Data_Types['name-to-marker']['dictionary-type']):
        dictionary_Type = {}
        step = amf3_Get_U29_raw(unhandled_Bytes)
        unhandled_Bytes = step[0]
        dictionary_Type['ref'] = step[1]['ref']
        dictionary_Type['value'] = step[1]['value']
        step = amf3_Get_U8_raw(unhandled_Bytes)
        unhandled_Bytes = step[0]
        dictionary_Type['weak-keys'] = step[1]
        dictionary_Type['entry'] = {}
        for i in range(1,dictionary_Type['value']+1):
            dictionary_Type['entry'][i] = {}
            step = amf3_Get_Value_Type(unhandled_Bytes)
            unhandled_Bytes = step[0]
            dictionary_Type['entry'][i]['key'] = step[1]
            step = amf3_Get_Value_Type(unhandled_Bytes)
            unhandled_Bytes = step[0]
            dictionary_Type['entry'][i]['value'] = step[1]
        return((unhandled_Bytes,dictionary_Type))
    else:
        return(None)

##-----------------------------------------------------------------##
##                                                                 ##
##-----------------------------------------------------------------##

def amf3_Decode(unhandled_Bytes,amf3_Data_Types,U29O_traits_Ext_U8_count):
    VT_dict = {}
    seq = 1
    while(not(unhandled_Bytes == b'')):
        step = amf3_Get_Value_Type(unhandled_Bytes,amf3_Data_Types,U29O_traits_Ext_U8_count)
        unhandled_Bytes = step[0]
        VT_dict[seq] = step[1]
        seq = seq + 1
    return(VT_dict)


#
def get_unhandled_Bytes(filename):
    fd = open(filename,'rb')
    return(fd.read())
    fd.close()

# #############################################################################################################################################################
#filename = sys.argv[1]
#unhandled_Bytes = get_unhandled_Bytes(filename)
#U29O_traits_Ext_U8_count = int(sys.argv[2])
#VT_dict =  amf3_Decode(unhandled_Bytes,amf3_Data_Types,U29O_traits_Ext_U8_count)
#print(jsbeautifier.beautify(str(VT_dict)))


# A. amf3_Bytes_File

# more ./test_1.amf3

# lex.messaging.messages.CommandMessageoperation
# __e+a+i-+Id+e__ageIdc+ie++Id+i+eT-Li+e+i+e_+a+-headersde
# stination       bodyI50A43A42-6AB3-FA5B-0601-AA658F60C1F5

#        DSIdnil%DSMessagingVersion
# 


# B. bytes_Stream  of  amf3_Bytes_File

# >>> get_unhandled_Bytes('test_1.amf3')
# b'\n\x81\x13Mflex.messaging.messages.CommandMessage\x13operation\x1bcorrelationId\x13messageId\x11clientId\x15timeToLive\x13timestamp\x0fheaders\x17destination\tbody\x04\x05\x06\x01\x06I50A43A42-6AB3-FA5B-0601-AA658F60C1F5\x01\x04\x00\x04\x00\n\x0b\x01\tDSId\x06\x07nil%DSMessagingVersion\x04\x01\x01\x06\x01\n\x05\x01'
# >>>



# C.

# python3 amf3_Decode.py "test_1.amf3" 0
# {
    # 1: {
        # 'marker': 'object-marker',
        # 'marker-raw': b '\n',
        # 'body': {
            # 'traits-ext-U8s': None,
            # 'ref': None,
            # 'sealed-names': {
                # 1: {
                    # 'string-raw': b 'operation',
                    # 'value': 9,
                    # 'string': 'operation',
                    # 'ref': None,
                    # 'U29S-raw': b '\x13'
                # },
                # 2: {
                    # 'string-raw': b 'correlationId',
                    # 'value': 13,
                    # 'string': 'correlationId',
                    # 'ref': None,
                    # 'U29S-raw': b '\x1b'
                # },
                # 3: {
                    # 'string-raw': b 'messageId',
                    # 'value': 9,
                    # 'string': 'messageId',
                    # 'ref': None,
                    # 'U29S-raw': b '\x13'
                # },
                # 4: {
                    # 'string-raw': b 'clientId',
                    # 'value': 8,
                    # 'string': 'clientId',
                    # 'ref': None,
                    # 'U29S-raw': b '\x11'
                # },
                # 5: {
                    # 'string-raw': b 'timeToLive',
                    # 'value': 10,
                    # 'string': 'timeToLive',
                    # 'ref': None,
                    # 'U29S-raw': b '\x15'
                # },
                # 6: {
                    # 'string-raw': b 'timestamp',
                    # 'value': 9,
                    # 'string': 'timestamp',
                    # 'ref': None,
                    # 'U29S-raw': b '\x13'
                # },
                # 7: {
                    # 'string-raw': b 'headers',
                    # 'value': 7,
                    # 'string': 'headers',
                    # 'ref': None,
                    # 'U29S-raw': b '\x0f'
                # },
                # 8: {
                    # 'string-raw': b 'destination',
                    # 'value': 11,
                    # 'string': 'destination',
                    # 'ref': None,
                    # 'U29S-raw': b '\x17'
                # },
                # 9: {
                    # 'string-raw': b 'body',
                    # 'value': 4,
                    # 'string': 'body',
                    # 'ref': None,
                    # 'U29S-raw': b '\t'
                # }
            # },
            # 'class-name': {
                # 'string-raw': b 'flex.messaging.messages.CommandMessage',
                # 'value': 38,
                # 'string': 'flex.messaging.messages.CommandMessage',
                # 'ref': None,
                # 'U29S-raw': b 'M'
            # },
            # 'U29-raw': b '\x81\x13',
            # 'dynamic-members': None,
            # 'traits-ref': None,
            # 'traits': {
                # 'dynamic': False,
                # 'sealed-names-count': 9
            # },
            # 'sealed-value-types': {
                # 1: {
                    # 'marker': 'integer-marker',
                    # 'marker-raw': b '\x04',
                    # 'body': {
                        # 'INT': 5,
                        # 'U29-raw': b '\x05'
                    # }
                # },
                # 2: {
                    # 'marker': 'string-marker',
                    # 'marker-raw': b '\x06',
                    # 'body': {
                        # 'string-raw': b '',
                        # 'value': 0,
                        # 'string': '',
                        # 'ref': None,
                        # 'U29S-raw': b '\x01'
                    # }
                # },
                # 3: {
                    # 'marker': 'string-marker',
                    # 'marker-raw': b '\x06',
                    # 'body': {
                        # 'string-raw': b '50A43A42-6AB3-FA5B-0601-AA658F60C1F5',
                        # 'value': 36,
                        # 'string': '50A43A42-6AB3-FA5B-0601-AA658F60C1F5',
                        # 'ref': None,
                        # 'U29S-raw': b 'I'
                    # }
                # },
                # 4: {
                    # 'marker': 'null-marker',
                    # 'marker-raw': b '\x01',
                    # 'body': b ''
                # },
                # 5: {
                    # 'marker': 'integer-marker',
                    # 'marker-raw': b '\x04',
                    # 'body': {
                        # 'INT': 0,
                        # 'U29-raw': b '\x00'
                    # }
                # },
                # 6: {
                    # 'marker': 'integer-marker',
                    # 'marker-raw': b '\x04',
                    # 'body': {
                        # 'INT': 0,
                        # 'U29-raw': b '\x00'
                    # }
                # },
                # 7: {
                    # 'marker': 'object-marker',
                    # 'marker-raw': b '\n',
                    # 'body': {
                        # 'traits-ext-U8s': None,
                        # 'ref': None,
                        # 'sealed-names': {},
                        # 'class-name': {
                            # 'string-raw': b '',
                            # 'value': 0,
                            # 'string': '',
                            # 'ref': None,
                            # 'U29S-raw': b '\x01'
                        # },
                        # 'U29-raw': b '\x0b',
                        # 'dynamic-members': {
                            # 1: {
                                # 'body': {
                                    # 'marker': 'string-marker',
                                    # 'marker-raw': b '\x06',
                                    # 'body': {
                                        # 'string-raw': b 'nil',
                                        # 'value': 3,
                                        # 'string': 'nil',
                                        # 'ref': None,
                                        # 'U29S-raw': b '\x07'
                                    # }
                                # },
                                # 'name': {
                                    # 'string-raw': b 'DSId',
                                    # 'value': 4,
                                    # 'string': 'DSId',
                                    # 'ref': None,
                                    # 'U29S-raw': b '\t'
                                # }
                            # },
                            # 2: {
                                # 'body': {
                                    # 'marker': 'integer-marker',
                                    # 'marker-raw': b '\x04',
                                    # 'body': {
                                        # 'INT': 1,
                                        # 'U29-raw': b '\x01'
                                    # }
                                # },
                                # 'name': {
                                    # 'string-raw': b 'DSMessagingVersion',
                                    # 'value': 18,
                                    # 'string': 'DSMessagingVersion',
                                    # 'ref': None,
                                    # 'U29S-raw': b '%'
                                # }
                            # },
                            # 3: {
                                # 'body': None,
                                # 'name': {
                                    # 'string-raw': b '',
                                    # 'value': 0,
                                    # 'string': '',
                                    # 'ref': None,
                                    # 'U29S-raw': b '\x01'
                                # }
                            # }
                        # },
                        # 'traits-ref': None,
                        # 'traits': {
                            # 'dynamic': True,
                            # 'sealed-names-count': 0
                        # },
                        # 'sealed-value-types': {},
                        # 'traits-ext': None
                    # }
                # },
                # 8: {
                    # 'marker': 'string-marker',
                    # 'marker-raw': b '\x06',
                    # 'body': {
                        # 'string-raw': b '',
                        # 'value': 0,
                        # 'string': '',
                        # 'ref': None,
                        # 'U29S-raw': b '\x01'
                    # }
                # },
                # 9: {
                    # 'marker': 'object-marker',
                    # 'marker-raw': b '\n',
                    # 'body': {
                        # 'traits-ext-U8s': None,
                        # 'ref': None,
                        # 'sealed-names': None,
                        # 'class-name': None,
                        # 'U29-raw': b '\x05',
                        # 'dynamic-members': None,
                        # 'traits-ref': 1,
                        # 'traits': None,
                        # 'sealed-value-types': None,
                        # 'traits-ext': None
                    # }
                # }
            # },
            # 'traits-ext': None
        # }
    # },
    # 2: {
        # 'marker': 'null-marker',
        # 'marker-raw': b '\x01',
        # 'body': b ''
    # }
# }
##############################################################################################################################################################

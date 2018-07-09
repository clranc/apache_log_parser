from datetime import datetime, timedelta, tzinfo
import re

#
# @Class
#   Parser
#
# @Initialization Prototype
#   Parser( format_str )
#
# @Purpose
#   Parser class for constructing an apache log
#
# @Revision
#   Author: Christopher L. Ranc
#   Modified:
#
# @Internal variables
#   delim_list  : List of delimiting characters that seperate log
#                 variables
#   parser_list : List of parser funtions and format bracket data
#                 for the parser
#
# @Class Methods
#   parse(log_str) : Method for parsing the given log_str and returning an
#                    ApacheLog object with the data of the log_str
#
# @Notes
#   Input
#       method_str
#       request_URI_str
#       http_vers_str
#
class Parser:

    def __init__( self, format_str ):
        (self.delim_list, self.parser_list) = parseFormatString(format_str)

    def parse(self, log_str ):
        i = 0
        d = 0

        log = ApacheLog()

        for parser in self.parser_list:
            while d < len(self.delim_list) and self.delim_list[d] == log_str[i] :
                i += 1
                d += 1

            if parser[1] == '':
                i += parser[0](log_str[i:], log)
            else:
                i += parser[0](log_str[i:], log, parser[1])

        return log



#
# @Class
#   HTTPLine
#
# @Initialization Prototype
#   HTTPLine(method_str, request_URI_str, http_vers_str)
#
# @Purpose
#   Class for storing httpline components to easily use each
#   portion of the http request line
#
# @Revision
#   Author: Christopher L. Ranc
#   Modified:
#
# @Internal variables
#   method_str
#   request_URI_str
#   http_vers_str
#
# @Class Methods
#
# @Notes
#   Input
#       method_str
#       request_URI_str
#       http_vers_str
#
class HTTPLine:
    def __init__(self, method_str, request_URI_str, http_version_str):
        self.method_str = method_str
        self.request_URI_str = request_URI_str
        self.http_version_str = http_version_str

#
# @Class
#   ApacheLog
#
# @Initialization Prototype
#   ApacheLog()
#
# @Purpose
#   Class meant for easy storing of possible apache log data
#
# @Revision
#   Author: Christopher L. Ranc
#   Modified:
#
# @Internal variables
#    self.remote_ip_str
#    self.local_ip_str
#    self.byte_count_nh_int
#    self.byte_count_nhclf_int
#    self.cookie_str
#    self.request_time_int
#    self.environment_var_str
#    self.filename_str
#    self.remote_host_str
#    self.request_protocol_str
#    self.header_line_str
#    self.keep_alive_cnt_int
#    self.remote_log_str
#    self.request_method_str
#    self.note_str
#    self.reply_str
#    self.port_str
#    self.proc_id_str
#    self.query_str
#    self.http_line
#    self.handler_str
#    self.last_request_time_int
#    self.time
#    self.unit_str
#    self.remote_user_str
#    self.url_path
#    self.request_server_name_str
#    self.server_name_str
#    self.connection_status_str
#    self.bytes_recieved_int
#    self.bytes_sent_int
#    self.request_str
#    self.response_str
#
# @Class Methods
#
# @Notes
#
class ApacheLog:
    def __init__(self):
        self.remote_ip_str = None

        self.local_ip_str = None

        self.byte_count_nh_int = None

        self.byte_count_nhclf_int = None

        self.cookie_str = None

        self.request_time_int = None

        self.environment_var_str = None

        self.filename_str = None

        self.remote_host_str = None

        self.request_protocol_str = None

        self.header_line_str = None

        self.keep_alive_cnt_int = None

        self.remote_log_str = None

        self.request_method_str = None

        self.note_str = None

        self.reply_str = None

        self.port_str = None

        self.proc_id_str = None

        self.query_str = None

        self.http_line = None

        self.handler_str = None

        self.last_request_time_int = None

        self.time = None

        self.unit_str = None

        self.remote_user_str = None

        self.url_path_str = None

        self.request_server_name_str = None

        self.server_name_str = None

        self.connection_status_str = None

        self.bytes_recieved_int = None

        self.bytes_sent_int = None

        self.request_str = None

        self.response_str = None



#
# @Class
#   FixedOffset : subclass of tzinfo
#
# @Initialization Prototype
#   FixedOffset(offset_str)
#
# @Purpose
#   Required subclass to create a tzinfo object for offset needed by the
#   date object
#
# @Revision
#   Author: Christopher L. Ranc
#   Modified:
#
# @Internal variables
#   self.__offset
#   self.__name
#
# @Class Methods
#   utcoffset(dt) : required method for tzinfo subclasses
#   tzname(dt)    : required method for tzinfo subclasses
#   dst(dt)       : required method for tzinfo subclasses
#   __repr__()    : required method for tzinfo subclasses
#
# @Notes
#   Input
#       offset_str : "+0000" the offset portion of the Apache log time string
#
class FixedOffset(tzinfo):
    def __init__(self, offset_str):
        ## Direction
        if offset_str[0] == '-':
            direction = -1
        elif offset_str[0] == '+':
            direction = +1
        else:
            direction = +1

        ## Calculating offset from time offset_str
        offset = int(offset_str[2:4]) * 60 + int(offset_str[4:6])

        self.__offset = timedelta(minutes = direction * offset)

        self.__name = offset_str

    def utcoffset(self, dt):
        return self.__offset

    def tzname(self, dt):
        return self.__name

    def dst(self, dt):
        return timedelta(0)

    def __repr__(self):
        return repr(self.__name)


#
# Lambda for checking if a values is not a space
#
isNEqualSPNL = lambda x : x != ' ' and x != '\n'

#
# @Prototype
#   Function: getString()
#   Example:  getString(some_str)
#             getString(some_str, isNEqualTab)
#
# @Purpose
#   This function returns the beginning of a string
#   and the index of where it meets its stopping condition
#   provided by the user or at a space if one is not provided
#
# @Revision
#   Author: Christopher L. Ranc
#   Modified:
#
# @Notes:
#   Input:
#      input_str   : String for parsing
#      isValidChar : Stop condition function
#   Output:
#      (parsed_string, i) : Parsed out string and the end
#                           index of it from the input string
#
def getString(input_str, isValidChar=isNEqualSPNL):
    i = 0

    for char in input_str:
        if isValidChar(char):
            i += 1
        else:
            return (input_str[0:i], i)

    return (input_str, i)

#
# @Prototype
#   Function: getInt()
#   Example:  getInt(some_str)
#
# @Purpose
#   This function returns the beginning of a string that is
#   expected to be a number and the ending index of the string
#
# @Revision
#   Author: Christopher L. Ranc
#   Modified:
#
# @Notes:
#   Input:
#      input_str   : String for parsing
#   Output:
#      (number, i) : Touple of integer value and end index
#
def getInt(input_string):
    (num_string, i) = getString(input_string)

    if(num_string == '-'):
        return (None, i)

    return (int(num_string), i)


#
# @Prototype
#   Function: getEscDelim
#   Example: getEscDelim( delim_chr )
#
# @Purpose
#   This helper function is to be used by parseFormatString for correctly
#   determing hard written escaped characters from the format string to
#   be returned and added to the delim_list built by parseFormatString.
#
# @Revision
#   Author: Christopher L. Ranc
#   Modified:
#
# @Notes
#   Input:
#       delim_chr : Delimiting character to be checked to see what escaped
#                   character it is
#   Output:
#       Returns the correct delimiting escaped character for the delim_list
#
def getEscDelim( delim_chr ):

    # Return Tab as a delimiter
    if delim_chr == "t":
        return "\t"

    # Return Veritcal Tab as a delimiter
    elif delim_chr == "v":
        return "\v"

    # Return Bell as a delimiter cause why not have audible tones as delimiters
    elif delim_chr == "a":
        return "\a"

    # Return Back Space as a delimiter because you can use that
    elif delim_chr == "b":
        return "\b"

    # Return Form Feed as a delimiter because why not have page seperators
    # as delimitors
    elif delim_chr == "f":
        return "\f"

    # Return Carriage Return as a delimiter
    elif delim_chr == "r":
        return "\r"

    # Other hard written escaped characters in the format string like \, ",
    # or ' will work correctly when returned.  Newlines, \n, or worse Null
    # terminators, \0, should be avoided cause they will mess with the file
    # reading and parsing. Since the whole log entyr is expected to be on a
    # newline and Null terminators break reading a file in general.
    #
    # If someone wants to use those in the format string please yell at them.
    #
    else:
        return delim_chr


#
# @Prototype
#   Function: parseFormatString()
#   Example:  parseFormatString( format_string, log )
#
# @Purpose
#   This function parses the format string of the expected Apache log
#   and returns a touple of lists of the delimiting characters in the format
#   string.
#
# @Revision
#   Author: Christopher L. Ranc
#   Modified:
#
# @Notes:
#   Input:
#      format_str : String for parsing the structure of the logs
#   Output:
#      (delim_list, parser_list) : Touple of delim_list and parser_list.  The
#                                  delim_list consists of characters spacing
#                                  the format variables in the format string.
#                                  The parser_list consists of the parser
#                                  functions applicable to the variables of
#                                  the format string.
#
def parseFormatString( format_string ):
    delim_list = []
    parser_list = []

    str_length_int = len( format_string )
    i = 0

    while i < str_length_int:
        if format_string[i] == '%':
            i += 1

            # Check if this is a % sign that can be added to the delimiter list
            if format_string[i] =='%':
                delim_list.append( format_string[i] )
                i += 1
            else:
                i = appendParserList( format_string, parser_list, i )

        # Check for back slashes to identify escaped characters
        elif format_string[i] == '\\':
            i += 1

            delim_chr = getEscDelim( format_string[i] )
            delim_list.append( delim_chr )

            i += 1

        # Append to delimiter list
        else:
            delim_list.append( format_string[i] )
            i += 1


    return (delim_list, parser_list)


# See if character is a number from 0 - 9 or an ! to indicate if this
# is the beginning of a http request modifier
isModifier = lambda x : ('/' < x and x < ':') or x == '!'


#
# @Prototype
#   Function: appendParserList()
#   Example:  appendParserList( input_str, parser_list, index )
#
# @Purpose
#   This function is meant for processing and appending parts of the
#   log format string. to the
#
# @Revision
#   Author: Christopher L. Ranc
#   Modified:
#
# @Notes:
#   Input:
#      input_str   : String for parsing
#      parser_list : Parser function list to add functions to
#      index       : Index for the passed string
#
#   Output:
#      index : Index for where to continue from the string input_str the
#              calling code made
#
def appendParserList( input_str, parser_list, index ):
    base_index = 0
    format_bracket_str = ''

    # Skip over request modifier text for different http codes if any
    if isModifier(input_str[index]):
        while input_str[index] != '{':
            index += 1

    # Check for format bracket text
    if input_str[index] == '{':
        index += 1
        base_index = index

        while input_str[index] != '}':
            index += 1

        format_bracket_str = input_str[base_index:index]

        index += 1

        # for ti and to log characters
        if input_str[index] == '^':
            base_index = index + 1
            index += 3
            format_str = input_str[base_index : index]

        # Otherwise parse single character
        else:
            format_str = input_str[index]
            index += 1

    # Else See if this is %>s which isn't different in terms of parsing
    # for %s
    elif input_str[index] == '>':
        index += 1
        format_str = input_str[index]
        index += 1

    # Get format character
    else:
        format_str = input_str[index]
        index += 1

    parser_list.append( [parse_func_dict[format_str], format_bracket_str] )

    return index



#
# @Prototype
#   Function: storeRemoteIP()
#   Example:  storeRemoteIP( rip_str, log )
#
# @Purpose
#   This function stores the remote ip string into the given apache log
#   object and returns the ending index of the parsed string
#
# @Revision
#   Author: Christopher L. Ranc
#   Modified:
#
# @Notes:
#   Input:
#       rip_str : String for parsing
#   Output:
#       i : ending index of parsed string value
def storeRemoteIP(rip_str, log) :
    (log.remote_ip_str, i) = getString(rip_str)

    return i


#
# @Prototype
#   Function: storeLocalIP()
#   Example:  storeLocalIP( lip_str, log )
#
# @Purpose
#   This function stores the local ip string into the given apache log
#   object and returns the ending index of the parsed string
#
# @Revision
#   Author: Christopher L. Ranc
#   Modified:
#
# @Notes:
#   Input:
#       lip_str : String for parsing
#   Output:
#       i : ending index of parsed string value
#
def storeLocalIP(lip_str, log) :
    (log.local_ip_str, i) = getString(lip_str)

    return i


#
# @Prototype
#   Function: storeByteCountNH()
#   Example:  storeByteCountNH( bc_str, log )
#
# @Purpose
#   This function stores the byte count of a request, without headers, as an
#   integer into the given apache log object and returns the ending index of
#   the parsed string.
#
# @Revision
#   Author: Christopher L. Ranc
#   Modified:
#
# @Notes:
#   Input:
#       bc_str : String for parsing
#   Output:
#       i : ending index of parsed string value
#
def storeByteCountNH( bc_str, log ):
    (log.byte_count_nh_int, i) = getInt( bc_str )

    return i


#
# @Prototype
#   Function: storeByteCountNHCLF()
#   Example:  storeByteCountNHCLF( bc_str, log )
#
# @Purpose
#   This function stores the byte count of a request, without headers, as an
#   integer into the given apache log object and returns the ending index of
#   the parsed string.  If the value is 0 then a '-' is returned.
#
# @Revision
#   Author: Christopher L. Ranc
#   Modified:
#
# @Notes:
#   Input:
#       bc_str : String for parsing
#   Output:
#       i : ending index of parsed string value
#
def storeByteCountNHCLF( bc_str, log ):
    (log.byte_count_nhclf_int, i) = getInt( bc_str )

    return i

#
# @Prototype
#   Function: storeCookie()
#   Example:  storeCookie( cookie_str, log )
#
# @Purpose
#   This function stores the cookie string into the given apache log
#   object and returns the ending index of the parsed string
#
# @Revision
#   Author: Christopher L. Ranc
#   Modified:
#
# @Notes:
#   Input:
#       cookie_str : String for parsing
#   Output:
#       i : ending index of parsed string value
#
def storeCookie(cookie_str, log, fb_str = None):
    (log.cookie_str, i) = getString( cookie_str )

    return i


#
# @Prototype
#   Function: storeByteCount()
#   Example:  storeByteCount( rt_str, log )
#
# @Purpose
#   This function stores the request time as a integer into the given
#   apache log object and returns the ending index of the parsed string
#
# @Revision
#   Author: Christopher L. Ranc
#   Modified:
#
# @Notes:
#   Input:
#       rt_str : String for parsing
#   Output:
#       i : ending index of parsed string value
#
def storeRequestTime( rt_str, log):
    (log.request_time, i) = getInt( rt_str )

    return i

#
# @Prototype
#   Function: storeEnvironVar()
#   Example:  storeEnvironVar( ev_str, log )
#
# @Purpose
#   This function stores the environment variable string into the given apache
#   log object and returns the ending index of the parsed string
#
# @Revision
#   Author: Christopher L. Ranc
#   Modified:
#
# @Notes:
#   Input:
#       ev_str : String for parsing
#   Output:
#       i : ending index of parsed string value
#
def storeEnvironVar(ev_str, log, fb_str = None):
    (log.environment_var_str, i) = getString( ev_str )

    return i

#
# @Prototype
#   Function: storeFilename()
#   Example:  storeFilename( fn_str, log )
#
# @Purpose
#   This function stores the filename string into the given apache log
#   object and returns the ending index of the parsed string
#
# @Revision
#   Author: Christopher L. Ranc
#   Modified:
#
# @Notes:
#   Input:
#       fn_str : String for parsing
#   Output:
#       i : ending index of parsed string value
#
def storeFilename( fn_str, log):
    (log.filename_str, i) = getString( filename_str )

    return i

#
# @Prototype
#   Function: storeRemoteHost()
#   Example:  storeRemoteHost( rh_str, log)
#
# @Purpose
#   This function stores the remote host string into the given apache log
#   object and return the ending index of parsed string
#
# @Revision
#   Author: Christopher L. Ranc
#   Modified:
#
# @Notes:
#   Input:
#       input_str : String for parsing
#   Output:
#       i : ending index of parsed string value
#
def storeRemoteHost( rh_str, log ):
    (log.remote_host, i) = getString(rh_str)

    return i

#
# @Prototype
#   Function: storeRequestProtocol()
#   Example:  storeRequestProtocol( rp_str, log )
#
# @Purpose
#   This function stores the request protocol string into the given apache log
#   object and returns the ending index of the parsed string
#
# @Revision
#   Author: Christopher L. Ranc
#   Modified:
#
# @Notes:
#   Input:
#       rp_str : String for parsing
#   Output:
#       i : ending index of parsed string value
#
def storeRequestProtocol( rp_str, log) :
    (log.request_protocol_str, i) = getString(rp_str)

    return i

#
# @Prototype
#   Function: storeHeaderLine()
#   Example:  storeHeaderLine( hl_str, log )
#
# @Purpose
#   This function stores the headerline string into the given apache log
#   object and returns the ending index of the parsed string
#
# @Revision
#   Author: Christopher L. Ranc
#   Modified:
#
# @Notes:
#   Input:
#       hl_str : String for parsing
#   Output:
#       i : ending index of parsed string value
#
def storeHeaderLine( hl_str, log ) :
    (log.header_line_str, i) = getString( hl_str )

    return i


#
# @Prototype
#   Function: storeKeepAliveCount()
#   Example:  storeKeepAliveCount( kac_str, log )
#
# @Purpose
#   This function stores the keep alive count string into the given apache log
#   object as an integer and returns the ending index of the parsed string
#
# @Revision
#   Author: Christopher L. Ranc
#   Modified:
#
# @Notes:
#   Input:
#       kac_str : String for parsing
#   Output:
#       i : ending index of parsed string value
#
def storeKeepAliveCount( kac_str, log) :
    (log.keep_alive_cnt_int, i) = getInt(kac_str)

    return i


#
# @Prototype
#   Function: storeRemoteLog()
#   Example:  storeRemoteLog( rl_str, log)
#
# @Purpose
#   This function stores the remote log string into the given apache log
#   object and returns the ending index of the parsed string
#
# @Revision
#   Author: Christopher L. Ranc
#   Modified:
#
# @Notes:
#   Input:
#       input_str : String for parsing
#   Output:
#       i : ending index of parsed string value
#
def storeRemoteLog( rl_str, log ):
    (log.remote_log, i) = getString(rl_str)

    return i

#
# @Prototype
#   Function: storeRequestMethod()
#   Example:  storeRequestMethod( rm_str, log )
#
# @Purpose
#   This function stores the request method string into the given apache log
#   object and returns the ending index of the parsed string
#
# @Revision
#   Author: Christopher L. Ranc
#   Modified:
#
# @Notes:
#   Input:
#       rm_str : String for parsing
#   Output:
#       i : ending index of parsed string value
#
def storeRequestMethod( rm_str, log ) :
    (log.request_method_str, i) = getString(rm_str)

    return i

#
# @Prototype
#   Function: storeNote()
#   Example:  storeNote( note_str, log )
#
# @Purpose
#   This function stores the note string into the given apache log
#   object and returns the ending index of the parsed string
#
# @Revision
#   Author: Christopher L. Ranc
#   Modified:
#
# @Notes:
#   Input:
#       note_str : String for parsing
#   Output:
#       i : ending index of parsed string value
#
def storeNote( note_str, log, fb_str = None) :
    (log.note_str, i) = getString(note_str)

    return i

#
# @Prototype
#   Function: storeReply()
#   Example:  storeReply( rep_str, log )
#
# @Purpose
#   This function stores the reply string into the given apache log
#   object and returns the ending index of the parsed string
#
# @Revision
#   Author: Christopher L. Ranc
#   Modified:
#
# @Notes:
#   Input:
#       rep_str : String for parsing
#   Output:
#       i : ending index of parsed string value
#
def storeReply( r_str, log, fb_str = None) :
    (log.reply_str, i) = getString(r_str)

    return i

#
# @Prototype
#   Function: storePort()
#   Example:  storePort( port_str, log )
#
# @Purpose
#   This function stores the port string into the given apache log
#   object and returns the ending index of the parsed string
#
# @Revision
#   Author: Christopher L. Ranc
#   Modified:
#
# @Notes:
#   Input:
#       port_str : String for parsing
#   Output:
#       i : ending index of parsed string value
#
def storePort( port_str, log, fb_str = None) :
    (log.port_str, i) = getString(port_str)

    return i

#
# @Prototype
#   Function: storeProcID()
#   Example:  storeProcID( pid_str, log )
#
# @Purpose
#   This function stores the process id string into the given apache log
#   object and returns the ending index of the parsed string
#
# @Revision
#   Author: Christopher L. Ranc
#   Modified:
#
# @Notes:
#   Input:
#       pid_str : String for parsing
#   Output:
#       i : ending index of parsed string value
#
def storeProcID( pid_str, log, fb_str = None) :
    (log.proc_id_str, i) = getString(pid_str)

    return i

#
# @Prototype
#   Function: storeQuery()
#   Example:  storeQuery( q_str, log )
#
# @Purpose
#   This function stores the query string into the given apache log
#   object and returns the ending index of the parsed string
#
# @Revision
#   Author: Christopher L. Ranc
#   Modified:
#
# @Notes:
#   Input:
#       q_str : String for parsing
#   Output:
#       i : ending index of parsed string value
#
def storeQuery( q_str, log) :
    (log.query_str, i) = getString(q_str)

    return i


#
# Lambda function for checking if the characters are the valid characters
# for the http version string
#
isHTTPChar = lambda x : x == 'H' or x == 'T' or x == 'P' or (x > '-' and x < ':')

#
# @Prototype
#   Function: storeHTTPLine()
#   Example:  storeHTTPLine( http_str, log )
#
# @Purpose
#   This function stores the http request string as a HTTPLine object into the
#   given apache log object and returns the ending index of the parsed string
#
# @Revision
#   Author: Christopher L. Ranc
#   Modified:
#
# @Notes:
#   Input:
#       http_str : String for parsing
#   Output:
#       i : ending index of parsed string value
#
def storeHTTPLine( http_str, log ) :
    (method_str, i) = getString(http_str)
    i += 1
    (request_URI_str, ii) = getString(http_str[i:])
    i += ii + 1
    (http_vers_str, ii) = getString(http_str[i:], isHTTPChar)
    i += ii

    log.http_line = HTTPLine( method_str, request_URI_str, http_vers_str )

    return i


#
# @Prototype
#   Function: storeHandler()
#   Example:  storeHandler( h_str, log )
#
# @Purpose
#   This function stores the  handler string into the given apache log
#   object and returns the ending index of the parsed string
#
# @Revision
#   Author: Christopher L. Ranc
#   Modified:
#
# @Notes:
#   Input:
#       h_str : String for parsing
#   Output:
#       i : ending index of parsed string value
#
def storeHandler( h_str, log ) :
    (log.handler_str, i) = getString(h_str)

    return i


#
# @Prototype
#   Function: storeRequestTime()
#   Example:  storeRequestTime( http_str, log )
#
# @Purpose
#   This function stores the last request time as a integer into the given
#   apache log object and returns the ending index of the parsed string
#
# @Revision
#   Author: Christopher L. Ranc
#   Modified:
#
# @Notes:
#   Input:
#       lrt_str : String for parsing
#   Output:
#       i : ending index of parsed string value
#
def storeLastRequestTime( lrt_str, log ):
    (log.last_request_time, i) = getInt( lrt_str )

    return i


#
# @Prototype
#   Function: storeTime()
#   Example:  storeTime( time_str, log, fb_str )
#
# @Purpose
#   This function stores the date string as a datetime object into the given
#   apache log object and returns the ending index of the parsed string
#
# @Revision
#   Author: Christopher L. Ranc
#   Modified:
#
# @Notes:
#   Input:
#       time_str : Apache time string
#       log      : Apache log object for storing
#       fb_str   : Format bracket string for log data if it exists
#   Output:
#       i : ending index of parsed string value
#
#   Default Apache time string structures
#     0000000000111111111122222222 <--- Indexes so this is easier to
#     0123456789012345678901234567 <--- make sense of.  Index 2 --> 27
#     [00/Sep/2012:06:05:11 +0000]                            7
#
#   **** Needs functionality for parsing format bracket string for
#        for custom time formats if the default isn't used
#
#
def storeTime( time_str, log, fb_str = None ):
    i = 0

    # Meant for finding the length of the time string
    # this is added for the case for handling different
    # time string formats specified for the %{format}t
    # version of apache log time data
    while time_str[i] != ']':
        i += 1

    month_dict = { 'Jan' : 1, 'Feb': 2, 'Mar' : 3, 'Apr' : 4, 'May' : 5, 'Jun' : 6,
        'Jul' : 6, 'Aug' : 8, 'Sep' : 9, 'Oct' : 10, 'Nov' : 11, 'Dec' : 12 }

    time = datetime(year=int(time_str[8:12]), month=month_dict[time_str[4:7]],
        day=int(time_str[1:3]), hour=int(time_str[13:15]),
        minute=int(time_str[16:18]), second=int(time_str[19:21]),
        tzinfo=FixedOffset(time_str[22:27]))

    log.time = time

    i += 1

    return i



def storeUnit( u_str, log) :
    (log.unit_str, log) = getString(u_str)

    return i



#
# @Prototype
#   Function: storeRemoteUser()
#   Example:  storeRemoteUser( ru_str, log )
#
# @Purpose
#   This function stores the remote log string into the given apache log
#   object and returns the ending index of the parsed string
#
# @Revision
#   Author: Christopher L. Ranc
#   Modified:
#
# @Notes:
#   Input:
#       ru_str : String for parsing
#   Output:
#       i : ending index of parsed string value
#
def storeRemoteUser( ru_str, log ):
    (log.remote_user, i) = getString(ru_str)

    return i

#
# @Prototype
#   Function: storeURLPath()
#   Example:  storeURLPath( up_str, log )
#
# @Purpose
#   This function stores the URL path string into the given apache log
#   object and returns the ending index of the parsed string
#
# @Revision
#   Author: Christopher L. Ranc
#   Modified:
#
# @Notes:
#   Input:
#       up_str : String for parsing
#   Output:
#       i : ending index of parsed string value
#
def storeURLPath(up_str, log) :
    (log.url_path_str, i) = getString(up_str)

    return i

#
# @Prototype
#   Function: storeRequestServerName()
#   Example:  storeRequestServerName( rsn_str, log )
#
# @Purpose
#   This function stores the request server name string into the given apache
#   log object and returns the ending index of the parsed string
#
# @Revision
#   Author: Christopher L. Ranc
#   Modified:
#
# @Notes:
#   Input:
#       rsn_str : String for parsing
#   Output:
#       i : ending index of parsed string value
#
def storeRequestServerName(rsn_str, log) :
    (log.request_server_name_str, i) = getString(rsn_str)

    return i

#
# @Prototype
#   Function: storeServerName()
#   Example:  storeServerName( sn_str, log )
#
# @Purpose
#   This function stores the server name string into the given apache
#   log object and returns the ending index of the parsed string
#
# @Revision
#   Author: Christopher L. Ranc
#   Modified:
#
# @Notes:
#   Input:
#       sn_str : String for parsing
#   Output:
#       i : ending index of parsed string value
#
def storeServerName(sn_str, log) :
    (log.server_name_str, log) = getString(sn_str)

    return i

#
# @Prototype
#   Function: storeConnectionStatus()
#   Example:  storeConnectionStatus( cs_str, log )
#
# @Purpose
#   This function stores the connection status string into the given apache
#   log object and returns the ending index of the parsed string
#
# @Revision
#   Author: Christopher L. Ranc
#   Modified:
#
# @Notes:
#   Input:
#       cs_str : String for parsing
#   Output:
#       i : ending index of parsed string value
#
def storeConnectionStatus(cs_str, log) :
    (log.connection_status_str, i) = getString(cs_str)

    return i

#
# @Prototype
#   Function: storeBytesRecieved()
#   Example:  storeBytesRecieved( br_str, log )
#
# @Purpose
#   This function stores the bytes recieved string into the given apache
#   log object as an integer and returns the ending index of the parsed string
#
# @Revision
#   Author: Christopher L. Ranc
#   Modified:
#
# @Notes:
#   Input:
#       br_str : String for parsing
#   Output:
#       i : ending index of parsed string value
#
def storeBytesRecieved(br_str, log) :
    (log.bytes_recieved_int, i) = getInt(br_str)

    return i

#
# @Prototype
#   Function: storeBytesSent()
#   Example:  storeBytesSent( bs_str, log )
#
# @Purpose
#   This function stores the bytes sent string into the given apache log
#   object as an integer and returns the ending index of the parsed string
#
# @Revision
#   Author: Christopher L. Ranc
#   Modified:
#
# @Notes:
#   Input:
#       br_str : String for parsing
#   Output:
#       i : ending index of parsed string value
#
def storeBytesSent(bs_str, log) :
    (log.bytes_sent_int, i) = getInt(bs_str)

    return i

#
# @Prototype
#   Function: storeRequest()
#   Example:  storeRequest( req_str, log )
#
# @Purpose
#   This function stores the request string into the given apache log
#   object and returns the ending index of the parsed string
#
# @Revision
#   Author: Christopher L. Ranc
#   Modified:
#
# @Notes:
#   Input:
#       br_str : String for parsing
#   Output:
#       i : ending index of parsed string value
#
def storeRequest(req_str, log) :
    (log.request_str, i) = getString(req_str, log)

    return i

#
# @Prototype
#   Function: storeResponse()
#   Example:  storeResponse( resp_str, log )
#
# @Purpose
#   This function stores the response string into the given apache log
#   object and returns the ending index of the parsed string
#
# @Revision
#   Author: Christopher L. Ranc
#   Modified:
#
# @Notes:
#   Input:
#       resp_str : String for parsing
#   Output:
#       i : ending index of parsed string value
#
def storeResponse(resp_str, log) :
    (log.response_str, i) = getString(resp_str, log)

    return i


#
# Parse function dictionary referenced when building parser list
#
parse_func_dict = {
    'a'  : storeRemoteIP,
    'A'  : storeLocalIP,
    'B'  : storeByteCountNH,
    'b'  : storeByteCountNHCLF,
    'C'  : storeCookie,
    'D'  : storeRequestTime,
    'e'  : storeEnvironVar,
    'f'  : storeFilename,
    'h'  : storeRemoteHost,
    'H'  : storeRequestProtocol,
    'i'  : storeHeaderLine,
    'k'  : storeKeepAliveCount,
    'l'  : storeRemoteLog,
    'm'  : storeRequestMethod,
    'n'  : storeNote,
    'o'  : storeReply,
    'p'  : storePort,
    'P'  : storeProcID,
    'q'  : storeQuery,
    'r'  : storeHTTPLine,
    'R'  : storeHandler,
    's'  : storeLastRequestTime,
    't'  : storeTime,
    'T'  : storeUnit,
    'u'  : storeRemoteUser,
    'U'  : storeURLPath,
    'v'  : storeRequestServerName,
    'V'  : storeServerName,
    'X'  : storeConnectionStatus,
    'I'  : storeBytesRecieved,
    'O'  : storeBytesSent,
    'ti' : storeRequest,
    'to' : storeResponse
}

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
#   Parser class for constructing a
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
        p = 0

        log = ApacheLog()

        for delim in self.delim_list:
            print( delim, log_str[i:] )
            if delim != log_str[i]:
                parser = self.parser_list[p]

                if parser[1] == '':
                    i += parser[0](log_str[i:], log)
                else:
                    i += parser[0](log_str[i:], log, parser[1])

                p += 1
            else:
                i += 1

        return log


class ParseStruct(object):
    def __init__(self, inVal=None):
        self.val = inVal

#
# @Class
#   HTTPLine
#
# @Initialization Prototype
#   HTTPLine(method_str, request_URI_str, http_vers_str)
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
class HTTPLine(ParseStruct):
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
#   Class meant for easy storing of apache log data
#
# @Revision
#   Author: Christopher L. Ranc
#   Modified:
#
# @Internal variables
#   remote_host_str
#   remote_log_str
#   remote_user
#   date
#   http_request
#   last_request_time_int
#   byte_count_int
#   request_time_int
#
# @Class Methods
#
# @Notes
#
class ApacheLog:
    def __init__(self):
        self.remote_host_str = None
        self.remote_log_str = None
        self.remote_user_str = None
        self.date = None
        self.http_request = None
        self.last_request_time_int = None
        self.byte_count_int = None
        self.request_time_int = None

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

            # Check if this is % sign that can be added to the delimiter list
            if format_string[i] =='%':
                delim_list.append( format_string[i] )
                i += 1
            else:
                i = appendParserList( format_string, parser_list, i )

        # Check to skip back slashes for escaped characters
        elif format_string[i] == '\\':
            i += 1

        # Append to delimiter list
        else:
            delim_list.append( format_string[i] )
            i += 1

    print(delim_list)

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

    date = datetime(year=int(time_str[8:12]), month=month_dict[time_str[4:7]],
        day=int(time_str[1:3]), hour=int(time_str[13:15]),
        minute=int(time_str[16:18]), second=int(time_str[19:21]),
        tzinfo=FixedOffset(time_str[22:27]))

    log.date = date

    i += 1

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
def storeHTTPLine( http_str, log) :
    (method_str, i) = getString(http_str)
    (request_URI_str, i) = getString(http_str[i:])
    (http_vers_str, i) = getString(http_str[i:], isHTTPChar)

    log.httpRequest = HTTPLine( method_str, request_URI_str, http_vers_str )

    return i

#
# @Prototype
#   Function: storeHTTPLine()
#   Example:  storeHTTPLine( http_str, log )
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
#   Function: storeByteCount()
#   Example:  storeByteCount( bc_str, log )
#
# @Purpose
#   This function stores the byte count as a integer into the given
#   apache log object and returns the ending index of the parsed string
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
def storeByteCount( bc_str, log ):
    (log.byte_count, i) = getInt( bc_str )

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
# Parse function dictionary referenced when building parser list
#
parse_func_dict = {
  'h' :  storeRemoteHost,
  'l' :  storeRemoteLog,
  'u' :  storeRemoteUser,
  't' :  storeTime,
  'r' :  storeHTTPLine,
  's' :  storeLastRequestTime,
  'b' :  storeByteCount,
  'D' :  storeRequestTime
}

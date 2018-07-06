import ALParser

parser = ALParser.Parser("%h %l %u %t \\\"%r\\\" %>s %b %D")

some_file = open("20180409-ABT-140635-143415-access_log_BPP-4BPMWBU001-nokeepalive.txt")

some_string = some_file.readline()

parser.parse(some_string)

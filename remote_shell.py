#!/usr/bin/env python
import re
import urllib

session = re.search('name="session" value="([^"]+)"',
                    urllib.urlopen('http://shell.appspot.com/').read())\
                    .groups(1)[0]


def execute(command):
    args = urllib.urlencode({'statement': command,
                            'session': session})

    result = urllib.urlopen("http://shell.appspot.com/shell.do?%s" \
                                % args).read()
    if re.search("Status: 200 OK", result.split("\r\n")[0]):
        result = "\n".join(result.split("\r\n")[6:])
    if re.search("Status: 500", result.split("\r\n")[0]):
        return False, '500'
    elif result[0:9] == "Traceback":
        return False, result.split("\n")[-2]
    elif result[0:9 + 5] == "<pre>Traceback":
        return False, result[5:].split("\n")[-2]
    else:
        return result  # "\n".join(result.split("\n")[:5])[:1024]

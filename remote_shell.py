#!/usr/bin/env python

# This file is part of Zeitgeist Borders (https://github.com/fabelier/Zeitgeist-Borders/) 
# Developed by Antoine Mazières, Samuel Huron and Julien Palard.
# Contact : admin at fabelier dot org
#
# Zeitgeist Borders is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Zeitgeist Borders is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Zeitgeist Borders.  If not, see <http://www.gnu.org/licenses/>.

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

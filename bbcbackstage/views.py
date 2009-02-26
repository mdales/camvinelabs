# Copyright (c) 2008-2009 Cambridge Visual Networks

# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

from django.shortcuts import render_to_response

import urllib2
from xml.etree import ElementTree as ET
import datetime

api_root = "http://www0.rdthdo.bbc.co.uk/cgi-perl/api/query.pl?"
method = "%smethod=bbc.schedule.getProgrammes&channel_id=%s&detail=schedule&limit=10"

def schedule_now(request, channel_id):
    
    # request the channel information from BBC Backstage
    
    call = method % (api_root, channel_id)
    response = urllib2.urlopen(call)
    tree = ET.ElementTree(file=response)
    
    schedule_el = tree.find('schedule')
    
    program_list = []
    for program in schedule_el.findall('programme'):
    
        info = {}
    
        info['title'] = program.attrib['title']
        info['description'] = program.find('synopsis').text
        start = program.find('start').text
        time = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%SZ")
        info['time'] = time.strftime("%H:%M")
        
        program_list.append(info)
        

    return render_to_response("schedule.cml", 
        {'program_list': program_list,
        'channel': channel_id})

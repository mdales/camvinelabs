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

def weekly(request):

    response = urllib2.urlopen('http://ws.audioscrobbler.com/2.0/?method=group.getweeklyartistchart&group=mnml&api_key=cc7b69cbb61525b9628c0675cb845f96')
    tree = ET.ElementTree(file=response)

    host = request.META.get('HTTP_X_FORWARDED_HOST', request.META.get('HTTP_HOST', '127.0.0.1'))
    
    uuid = tree.find('weeklyartistchart').get('from')
    from_ = datetime.datetime.fromtimestamp(float(tree.find('weeklyartistchart').get('from')))
    to_ = datetime.datetime.fromtimestamp(float(tree.find('weeklyartistchart').get('to')))

    artists = [{'mbid': node.find('mbid').text,
                'rank': node.get('rank'),
                'name': node.find('name').text}
               for node in tree.find('weeklyartistchart')[:10]]

    for artist in artists:
        response = urllib2.urlopen('http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&mbid=%s&api_key=cc7b69cbb61525b9628c0675cb845f96' % artist['mbid'])
        artist_tree = ET.ElementTree(file=response)
        artist['image_url'] = artist_tree.findall('artist/image')[1].text

    
    return render_to_response('weekly.cml',
                              {'artists': artists,
                               'uuid': uuid,
                               'host': host,
                               'from': from_,
                               'to': to_})

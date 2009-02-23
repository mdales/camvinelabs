from django.shortcuts import render_to_response

import urllib2
from xml.etree import ElementTree as ET

def album(request):

    response = urllib2.urlopen('http://ws.audioscrobbler.com/2.0/?method=group.getweeklyartistchart&group=mnml&api_key=cc7b69cbb61525b9628c0675cb845f96')
    tree = ET.ElementTree(file=response)

    host = request.META.get('HTTP_X_FORWARDED_HOST', request.META.get('HTTP_HOST', '127.0.0.1'))
    
    uuid = tree.find('weeklyartistchart').get('from')

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
                               'host': host})

import json, requests
from datetime import datetime, timedelta
from django.shortcuts import render

from django.http import HttpResponse

from .models import PlayInstance, Comment

from django.contrib.staticfiles.templatetags.staticfiles import static


def playlist(request):
    endtime = datetime.utcnow()
    starttime = endtime - timedelta(hours=1)
    starttime_string = starttime.strftime('%Y-%m-%dT%H:%M:%SZ')

    resp = requests.get('http://128.208.196.80/play/?begin_time=' + starttime_string + '&ordering=-airdate&limit=40')
    data = resp.json()
    #limit results to media play (1) and air breaks (4)
    data_parsed = [x for x in data['results'] if x['playtype']['playtypeid'] == 1 or 4]

    for play_item in data_parsed:
        has_comments = PlayInstance.objects.filter(
            kexp_play_id = play_item["playid"],
        )
        if has_comments:
            play_item['commentator_comments'] = "Blah blah blah"
        else:
            play_item['commentator_comments'] = "no comments"

    context = {
        'playlist': data_parsed,
        'backup_album_image': static('frontend/images/record.svg')
    }
    return render(request, 'playlist/playlist.html', context)

import json, requests
from datetime import datetime, timedelta
from dateutil import parser
from django.utils import timezone
from django.shortcuts import render

from django.http import JsonResponse

from .models import PlayInstance, Comment

from django.contrib.staticfiles.templatetags.staticfiles import static


def playlist(request):
    endtime = timezone.now()
    starttime = endtime - timedelta(hours=1)
    starttime_string = starttime.strftime('%Y-%m-%dT%H:%M:%SZ')

    resp = requests.get('http://128.208.196.80/play/?begin_time=' + starttime_string + '&ordering=-airdate&limit=40')
    data = resp.json()
    #limit results to media play (1) and air breaks (4)
    data_parsed = [x for x in data['results'] if x['playtype']['playtypeid'] == 1 or 4]

    for play_item in data_parsed:
        play_item['airdate_datetime'] = datetime.strptime(play_item['airdate'],'%Y-%m-%dT%H:%M:%SZ')
        db_match= PlayInstance.objects.filter(
            kexp_play_id = play_item["playid"],
        )
        if db_match:
            play_item['playlist_comments'] = db_match.first().comment_set.all()

    context = {
        'playlist': data_parsed,
        'backup_album_image': static('frontend/images/record.svg')
    }
    return render(request, 'playlist/playlist.html', context)


def comment(request):
    response = {'response': '',}
    if request.is_ajax():
        kexp_play_id = request.POST.get('play_instance_kexp_id')
        comment_id = request.POST.get('comment_id')

        play_instance, play_instance_status = PlayInstance.objects.get_or_create(
            kexp_play_id = kexp_play_id,
            name = request.POST.get('play_instance_name'),
            airdate = parser.parse(request.POST.get('play_instance_airdate')).replace(tzinfo=timezone.utc),
        )

        try:
            comment = Comment.objects.filter(id=comment_id, play_instance=play_instance).get()
        except (KeyError, Comment.DoesNotExist):
            comment = Comment(
                play_instance = play_instance,
                date_created = timezone.now(),
            )
        comment.comment_text = request.POST.get('comment_text')
        comment.date_last_edited = timezone.now()
        comment.save()

        response = {
            'response': 'comment ' + str(comment.id) + ' added or edited.',
            'play_instance_kexp_id' : kexp_play_id,
            'comment_id' : comment.id,
            'comment_text' : comment.comment_text,
            'comment_time_edited' : comment.date_created,
        }

    return JsonResponse(response)





        # response['id'] = register.id

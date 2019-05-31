import json, requests
from datetime import datetime, timedelta
from django.shortcuts import render

from django.http import HttpResponse

def playlist(request):
    endtime = datetime.utcnow()
    starttime = endtime - timedelta(hours=1)
    starttime_string = starttime.strftime('%Y-%m-%dT%H:%M:%SZ')

    resp = requests.get('http://128.208.196.80/play/?begin_time=' + starttime_string + '&ordering=-airdate&limit=40')
    # data = resp.json()
    data = resp
    return HttpResponse(data)

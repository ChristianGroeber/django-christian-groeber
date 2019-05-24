from django.shortcuts import render, redirect
import datetime
import pickle
import os.path
from .forms import CreateProject
from .models import Trackable, Color, CalendarEvent

import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

from christian_groeber_ch.settings import BASE_DIR

# Create your views here.

SCOPES = ['https://www.googleapis.com/auth/calendar']
CLIENT_SECRET_FILE = os.path.join(BASE_DIR, 'woven-solution-241515-16bb63aa00cc.json')
# CLIENT_SECRET_FILE = os.path.join(BASE_DIR, 'client_id.json')
service_account_email = 'worktracker@woven-solution-241515.iam.gserviceaccount.com'


def build_service():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        filename=CLIENT_SECRET_FILE,
        scopes=SCOPES)
    http = credentials.authorize(httplib2.Http())
    service = build('calendar', 'v3', http=http)
    print(service)
    return service


def update_colors():
    colors = Color.objects.all()
    if colors:
        pass
    else:
        orig_colors = build_service().colors().get().execute()
        for orig_color in orig_colors['event']:
            if str(orig_color) not in colors:
                color_dict = orig_colors['event'][orig_color]
                background = color_dict['background']
                foreground = color_dict['foreground']
                a = Color(color_id=orig_color, background_hash_code=background, foreground_hash_code=foreground)
                a.save()


def index(request):
    if str(request.user) == "AnonymousUser":
        return redirect('../')
    else:
        update_colors()
        projects = Trackable.objects.all()
        return render(request, 'work_tracker/index.html', {'projects': projects})


def new_project(request):
    if str(request.user) == "AnonymousUser":
        return redirect('../../')
    else:
        colors = Color.objects.all()
        create_project_form = CreateProject()
        if request.method == 'POST':
            create_project_form = CreateProject(request.POST)
            if create_project_form.is_valid():
                create_project_form.save()
                return redirect('../')
        return render(request, 'work_tracker/create.html', {'forms': create_project_form, 'colors': colors})


def create_event(name, color_id):
    service = build_service()
    GMT_OFF = '+02:00'
    time_now = datetime.datetime.now()
    time_now_str = time_now.strftime("%Y-%m-%dT%H:%M:%S")
    date_today = datetime.date.today()
    event = service.events().insert(calendarId='swiss8oy.chg@gmail.com', sendNotifications=False, body={
        'summary': name,
        'start': {'dateTime': time_now_str + GMT_OFF},
        'end': {'dateTime': str(date_today) + 'T23:59:59' + GMT_OFF},
        'colorId': color_id
    }).execute()
    a = CalendarEvent(summary=name, event_id=event['id'])
    a.save()
    print(event)
    return a


def stop_running_event():
    running = Trackable.objects.filter(running=True)
    for event in running:
        event.running = False
        event.save()
        service = build_service()
        calendar_event = service.events().get(calendarId='swiss8oy.chg@gmail.com', eventId=event.current_calendar_event.event_id).execute()
        time_now = datetime.datetime.now()
        time_now_str = time_now.strftime("%Y-%m-%dT%H:%M:%S")
        calendar_event['end'] = {'dateTime': time_now_str + '+02:00'}
        updated_event = service.events().update(calendarId='swiss8oy.chg@gmail.com', eventId=calendar_event['id'], body=calendar_event).execute()


def stop_working(request):
    if str(request.user) == "AnonymousUser":
        return redirect('../../../')
    else:
        stop_running_event()
        return redirect('../')


def start_working(request, project_id):
    if str(request.user) == "AnonymousUser":
        return redirect('../../../')
    else:
        stop_running_event()
        event = Trackable.objects.get(pk=project_id)
        calendar_event = create_event(event.title, event.color.color_id)
        event.running = True
        event.current_calendar_event = calendar_event
        event.save()
        return redirect('../../')

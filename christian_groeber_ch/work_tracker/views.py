from django.contrib.auth import logout
from django.shortcuts import render, redirect
import datetime
import pickle
import os.path
from .forms import CreateProject, DescriptionForm, PlanningForm
from .models import Trackable, Color, CalendarEvent, MyUser

import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

from christian_groeber_ch.settings import BASE_DIR, SOCIAL_AUTH_GOOGLE_OAUTH2_KEY, SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET

# Create your views here.

SCOPES = ['https://www.googleapis.com/auth/calendar']
CLIENT_SECRET_FILE = os.path.join(BASE_DIR, 'client_secret_240082627833-thcll2e8hukf2hb2sngvass639er6ho1.apps.googleusercontent.com.json')
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
    orig_colors = build_service().colors().get().execute()
    colors = Color.objects.all()
    for orig_color in orig_colors['event']:
        if str(orig_color) not in colors:
            color_dict = orig_colors['event'][orig_color]
            background = color_dict['background']
            foreground = color_dict['foreground']
            a = Color(color_id=orig_color, background_hash_code=background, foreground_hash_code=foreground)
            a.save()


def update_running_events():
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    end = str(datetime.date.today()) + 'T' + str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute + 2) +':59Z'
    events_result = build_service().events().list(
        calendarId='swiss8oy.chg@gmail.com',
        timeMin=now,
        timeMax=end,
        maxResults=1,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])
    my_events = Trackable.objects.all()
    if not events:
        for event in my_events:
            event.running = False
            event.save()
        return
    start_time_date = datetime.datetime.strptime(events[0]['start']['dateTime'][:-6], "%Y-%m-%dT%H:%M:%S")
    now_date = datetime.datetime.now()
    if start_time_date >= now_date:
        for event in my_events:
            event.running = False
            event.save()
        return
    for event in my_events:
        if str(event.color.color_id) == str(events[0]['colorId']):
            event.running = True
            new_calendar_event = CalendarEvent(summary=events[0]['summary'], event_id=events[0]['id'])
            new_calendar_event.save()
            event.current_calendar_event = new_calendar_event
            event.save()
            break


def index(request):
    if not Color.objects.all():
        update_colors()
    current_user = MyUser.objects.filter(name=str(request.user))
    if str(request.user) == 'AnonymousUser':
        return redirect('login/')
    if len(current_user) == 0:
        a = MyUser(name=str(request.user), email=str(request.user.email))
        a.save()
        current_user = a
    else:
        current_user = current_user[0]
    projects = current_user.trackables.all()
    update_running_events()
    return render(request, 'work_tracker/index.html', {'projects': projects})


def new_project(request):
    colors = Color.objects.all()
    create_project_form = CreateProject()
    if request.method == 'POST':
        create_project_form = CreateProject(request.POST)
        if create_project_form.is_valid():
            a = Trackable(title=create_project_form.cleaned_data['title'], color=create_project_form.cleaned_data['color'])
            a.save()
            current_user = MyUser.objects.get(name=str(request.user))
            current_user.trackables.add(a)
            current_user.save()
            return redirect('../')
    return render(request, 'work_tracker/create.html', {'forms': create_project_form, 'colors': colors})


def create_event(request, name, color_id, start_time=None, end_time=None, description=None):
    service = build_service()
    GMT_OFF = '+02:00'
    current_user = MyUser.objects.get(name=str(request.user))
    if not start_time:
        time_now = datetime.datetime.now()
        time_now_str = time_now.strftime("%Y-%m-%dT%H:%M:%S")
        date_today = datetime.date.today()
        event = service.events().insert(calendarId=current_user.email, sendNotifications=False, body={
            'summary': name,
            'start': {'dateTime': time_now_str + GMT_OFF},
            'end': {'dateTime': str(date_today) + 'T23:59:59' + GMT_OFF},
            'colorId': color_id
        }).execute()
    else:
        event = service.events().insert(calendarId=current_user.email, sendNotifications=False, body={
            'summary': name + description,
            'start': {'dateTime': str(start_time)},
            'end': {'dateTime': str(end_time)},
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
    stop_running_event()
    return redirect('../')


def start_working(request, project_id):
    stop_running_event()
    event = Trackable.objects.get(pk=project_id)
    calendar_event = create_event(request, event.title, event.color.color_id)
    event.running = True
    event.current_calendar_event = calendar_event
    event.save()
    return redirect('../../')


def edit(request, project_id):
    project = Trackable.objects.get(pk=project_id)
    forms = CreateProject(instance=project)
    colors = Color.objects.all()
    if str(request.method) == 'POST':
        forms = CreateProject(request.POST, instance=project)
        if forms.is_valid():
            forms.save()
            return redirect('../../')
    return render(request, 'work_tracker/create.html', {'forms': forms, 'colors': colors, 'edit': project_id})


def delete(request, project_id):
    project = Trackable.objects.get(pk=project_id)
    project.delete()
    return redirect('../../')


def add_description_to_calendar(event_id, description):
    event = CalendarEvent.objects.get(pk=event_id)
    service = build_service()
    calendar_event = service.events().get(calendarId='swiss8oy.chg@gmail.com',
                                          eventId=event.event_id).execute()
    trackables = Trackable.objects.all()
    title_trackable = ""
    for trackable in trackables:
        print(trackable.current_calendar_event.id)
        if trackable.current_calendar_event.id == int(event_id):
            title_trackable = trackable.title
            break
    calendar_event['summary'] = title_trackable + ' - ' + description
    updated_event = service.events().update(calendarId='swiss8oy.chg@gmail.com', eventId=calendar_event['id'],
                                            body=calendar_event).execute()
    print(updated_event)


def add_description(request, event_id):
    event = CalendarEvent.objects.get(pk=event_id)
    form = DescriptionForm(instance=event)
    if str(request.method) == 'POST':
        form = DescriptionForm(request.POST, instance=event)
        if form.is_valid():
            event.save()
            add_description_to_calendar(event_id, form.cleaned_data['description'])
            return redirect('../../')
    return render(request, 'work_tracker/add-description.html', {'form': form})


def plan(request, project_id):
    form = PlanningForm()
    project = Trackable.objects.get(pk=project_id)
    if str(request.method) == 'POST':
        form = PlanningForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            start_time = str(date) + "T" + str(form.cleaned_data['start_time']) + "+02:00"
            end_time = str(date) + "T" + str(form.cleaned_data['end_time']) + "+02:00"
            print(str(start_time), str(end_time))
            description = form.cleaned_data['description']
            if description is not '':
                description = ' - ' + description
            create_event(request, project.title, str(project.color), start_time=start_time, end_time=end_time, description=description)
            return redirect('../../')
    return render(request, 'work_tracker/planning.html', {'form': form})


def login(request):
    return render(request, 'work_tracker/login.html')


def logout_view(request):
    logout(request)
    return redirect('../')

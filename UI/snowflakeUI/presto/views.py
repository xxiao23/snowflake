﻿from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

import jaydebeapi
import traceback
import sys
@login_required
def index(request):
    conn = jaydebeapi.connect('com.facebook.presto.jdbc.PrestoDriver',
                              'jdbc:presto://localhost:8080/system/information_schema',
                              {'user': 'root', 'password': ''})
    curs = conn.cursor()
    curs.execute('select table_schema, table_name from tables;')
    result = curs.fetchall()

    template = loader.get_template('presto/index.html')
    context = {
        'result': result,
    }
    return HttpResponse(template.render(context, request))

@login_required
def query(request):
    context = {}
    return render(request, "presto/query.html")

def ajax_get(request):
    info = request.GET.get('info')
    
    if info == "check":
        conn = jaydebeapi.connect('com.facebook.presto.jdbc.PrestoDriver',
                                  'jdbc:presto://localhost:8080/system',
                                  {'user': 'root', 'password': ''})
        curs = conn.cursor()
        curs.execute('select table_schema, table_name from information_schema.tables')
        output = curs.fetchall()
    else:
        output = ["Please try it again!"]

    data = {}
    data['info'] = output

    return JsonResponse(data)

def ajax_query(request):
    info = request.GET.get('info')
    data = {}

    try:
        conn = jaydebeapi.connect('com.facebook.presto.jdbc.PrestoDriver',
                                      'jdbc:presto://localhost:8080/hive/default',
                                      {'user': 'root', 'password': ''})
        curs = conn.cursor()
        curs.execute(info)
        output = curs.fetchall()
        data['info'] = output
    except Exception as e:
        data['info'] = [info, traceback.format_exception_only(e.__class__, e)]

    return JsonResponse(data)

def ajax_describe(request):
    command = request.GET.get('command')
    print(command)
    conn = jaydebeapi.connect('com.facebook.presto.jdbc.PrestoDriver',
                                  'jdbc:presto://localhost:8080/system',
                                  {'user': 'root', 'password': ''})
    curs = conn.cursor()
    curs.execute(command)
    output = curs.fetchall()

    data = {}
    data['results'] = output

    return JsonResponse(data)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('../../presto/query')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
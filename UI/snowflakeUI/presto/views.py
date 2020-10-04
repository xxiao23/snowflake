from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

import jaydebeapi


def index(request):
    conn = jaydebeapi.connect('com.facebook.presto.jdbc.PrestoDriver',
                              'jdbc:presto://localhost:8080/system/information_schema',
                              {'user': 'root', 'password': ''})
    curs = conn.cursor()
    curs.execute('SELECT * FROM tables')
    result = curs.fetchall()

    template = loader.get_template('presto/index.html')
    context = {
        'result': result,
    }
    return HttpResponse(template.render(context, request))
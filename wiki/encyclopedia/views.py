from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django import forms
import random
import markdown2

from . import util

class EncyclopediaForm(forms.Form):
    title = forms.CharField(label="Entry Title")

def index(request):
    if request.method == 'POST':
        title = request.POST['q']
        if util.get_entry(title):
            return HttpResponseRedirect('content')
        else:
            new_entries = []
            for i in util.list_entries():
                if title.upper() in i.upper():
                    new_entries.append(i)
            return render(request, 'encyclopedia/index.html', {
                "entries": new_entries
            })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def find(request, title):
    return render(request, 'encyclopedia/content.html', {
        "content": markdown2.markdown(util.get_entry(title)),
        "title": title
    })

def createpage(request):
    if request.method == 'POST':
        if request.POST['title'] not in util.list_entries():
            util.save_entry(request.POST['title'], request.POST['contentArea'])
        else:
            return render(request, 'encyclopedia/error.html')
    return render(request, 'encyclopedia/create.html', {
        'entry': EncyclopediaForm()
    })

def editpage(request):
    if request.method == 'POST':
        content = util.get_entry(request.POST['name'])
        return render(request, 'encyclopedia/editexist.html', {
            'title': request.POST['name'],
            "content": markdown2.markdown(content)
        })

def postedit(request):
    if request.method == 'POST':
        title = request.POST['name']
        content = request.POST['editContent']
        util.save_entry(title, content)
        return render(request, 'encyclopedia/content.html', {
            "content": markdown2.markdown(util.get_entry(title)),
            "title": title
        })

    return HttpResponse('hello')

def randompage(request):
    random_value = random.choice(util.list_entries())
    return render(request, 'encyclopedia/content.html', {
        "content": markdown2.markdown(util.get_entry(random_value)),
        "title": random_value
    })

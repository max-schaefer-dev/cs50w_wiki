from django.shortcuts import render, redirect
import markdown2
import random
import re
from django import forms

from . import util


class NewTaskForm(forms.Form):
    entryTitel = forms.CharField(label="Title")
    entryContent = forms.CharField(widget=forms.Textarea, label="Content")


def index(request):
    if request.method == "POST":
        search = request.POST.__getitem__("q")
        results = []
        for entry in util.list_entries():
            if search.upper() == entry.upper():
                return redirect(f'/wiki/{ search }')
            mat = re.search(f'{ search.upper() }', entry.upper())
            if mat:
                results.append(entry)
        return render(request, "encyclopedia/search-result.html", {
            "results": results
        })
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    if request.method == "POST":
        search = request.POST.__getitem__("q")
        results = []
        for entry in util.list_entries():
            if search.upper() == entry.upper():
                return redirect(f'/wiki/{ search }')
            mat = re.search(f'{ search.upper() }', entry.upper())
            if mat:
                results.append(entry)
        return render(request, "encyclopedia/search-result.html", {
            "results": results
        })
    return render(request, "encyclopedia/entry.html", {
        "entry": markdown2.markdown(util.get_entry(title))
    })


def new_entry(request):
    if request.method == "POST":
        search = request.POST.__getitem__("q")
        results = []
        for entry in util.list_entries():
            if search.upper() == entry.upper():
                return redirect(f'/wiki/{ search }')
            mat = re.search(f'{ search.upper() }', entry.upper())
            if mat:
                results.append(entry)
        return render(request, "encyclopedia/search-result.html", {
            "results": results
        })
    return render(request, "encyclopedia/new-entry.html", {
        "form": NewTaskForm
    })


def random_entry(request):
    # Randomizer #
    randomEntry = random.choice(util.list_entries())

    return redirect(f'/wiki/{ randomEntry }')

from django.shortcuts import render, redirect
import markdown2
import random
from django import forms

from . import util


class NewTaskForm(forms.Form):
    entryTitel = forms.CharField(label="Title")
    entryContent = forms.CharField(widget=forms.Textarea, label="Content")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    return render(request, "encyclopedia/entry.html", {
        "entry": markdown2.markdown(util.get_entry(title))
    })


def new_entry(request):
    return render(request, "encyclopedia/new-entry.html", {
        "form": NewTaskForm
    })


def random_entry(request):
    # Randomizer #
    randomEntry = random.choice(util.list_entries())

    return redirect(f'/wiki/{ randomEntry }')

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
import markdown2
import html2markdown
import random
import re

from django import forms

from . import util


class NewEntryForm(forms.Form):
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
        """ triggers if a search function has been used"""
        if request.POST.__contains__("q"):
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
        elif request.POST.__contains__("editTitle"):
            fullEntry = request.POST.__getitem__("editTitle")
            eTitle = re.findall("^<h1>(\\S+)</h1>", fullEntry)
            eContent = re.findall(
                "^<h1>\\S+</h1>\\r\\n\\r\\n(.+)", fullEntry, flags=re.DOTALL)
            editForm = NewEntryForm(
                initial={
                    'entryTitel': eTitle[0], 'entryContent': html2markdown.convert(eContent[0])}
            )
            return render(request, "encyclopedia/new-entry.html", {
                "editForm": editForm
            })
    return render(request, "encyclopedia/entry.html", {
        "entry": markdown2.markdown(util.get_entry(title)),
        "title": title
    })


def new_entry(request):
    if request.method == "POST":
        """ triggers if new entry has been saved """
        if request.POST.__contains__("newEntry"):
            form = NewEntryForm(request.POST)
            if form.is_valid():
                entryTitle = request.POST.__getitem__("entryTitel")
                for entry in util.list_entries():
                    if entryTitle.upper() == entry.upper():
                        return render(request, "encyclopedia/new-entry.html", {
                            "error": "Error: This entry already exists!"
                        })
                entryContent = request.POST.__getitem__("entryContent")
                md_file = f"entries\\{entryTitle}.md".format()
                with open(md_file, 'w') as f:
                    f.write(f"#{entryTitle}\n\n{entryContent}")
                return redirect(f"/wiki/{ entryTitle }")

        """ triggers if an existing entry get´s has been edited"""
        elif request.POST.__contains__("editedEntry"):
            form = NewEntryForm(request.POST)
            if form.is_valid():
                entryTitle = request.POST.__getitem__("entryTitel")
                entryContent = request.POST.__getitem__("entryContent")
                md_file = f"entries\\{entryTitle}.md".format()
                with open(md_file, 'w') as f:
                    f.write(f"#{entryTitle}\n\n{entryContent}")
                return redirect(f"/wiki/{ entryTitle }")

        """ triggers if a search function has been used"""
        elif request.POST.__contains__("q"):
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
        else:
            return render(request, "encyclopedia/new-entry.html", {
                "form": NewEntryForm
            })
    return render(request, "encyclopedia/new-entry.html", {
        "form": NewEntryForm
    })


def random_entry(request):
    # Randomizer #
    randomEntry = random.choice(util.list_entries())

    return redirect(f'/wiki/{ randomEntry }')

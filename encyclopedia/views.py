from django.shortcuts import render, redirect
import markdown2
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
        if request.POST.__len__() == 3:
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

        elif request.POST.__len__() == 2:
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

from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import util

import logging

logger = logging.getLogger(__name__)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, name):
    if request.method == "POST":
        return render(request, "encyclopedia/edit.html", {
            "name": name,
            "form": NewWikiForm(initial={"name":name, "content":util.get_entry(name)})
        })

    return render(request, "encyclopedia/wiki.html", {
        "name": name,
        "content": util.get_entry(name)
    })

def add(request):
    if request.method == "POST":
        form = NewWikiForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            content = form.cleaned_data["content"]
            file = open(f"entries/{name}.md", "x")
            file.write(content)
            file.close()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "encyclopedia/add.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/add.html", {
            "form": NewWikiForm()
        })

def edit(request):
    if request.method == "POST":
        logger.info("POST")
        form = NewWikiForm(request.POST)
        if form.is_valid():
            logger.info("form is valid")
            name = form.cleaned_data["name"]
            content = form.cleaned_data["content"]
            file = open(f"entries/{name}.md", "w")
            file.write(content)
            file.close()
            return HttpResponseRedirect(reverse("index"))
        else:
            logger.error("form is not valid")
            logger.error(form.errors)
            return render(request, "encyclopedia/edit.html", {
                "name": name,
                "form": form
            })
    else:
        logger.info("else")
        return render(request, "encyclopedia/edit.html", {
            "name": name,
            "form": NewWikiForm(initial={"name":name, "content":util.get_entry(name)})
        })


class NewWikiForm(forms.Form):
    name = forms.CharField(label="name")
    content = forms.CharField(widget=forms.Textarea, label="content")


def search(request): 
    if request.method == "POST":
        inputtxt = request.POST['q']
        if (util.get_entry(inputtxt) is not None):
            return wiki(request, inputtxt)
        else:
            return render(request, "encyclopedia/search.html", {
                "inputtxt": inputtxt,
                "entries": util.search_entries(inputtxt)
            })

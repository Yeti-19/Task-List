from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms




class NewTaskForm(forms.Form):
    task = forms.CharField(label = "New Task")
    #priority = forms.IntegerField(label = "Priority", min_value=1, max_value=10)


# Create your views here.
def index(request):
    if "tasks" not in request.session:
        request.session["tasks"] = []                    # For each user to have different tasks instead of having the same global variable for everyone

    return render(request, "tasks/index.html", {
        "tasks": request.session["tasks"]
    }
    )

def add(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data["task"]
            request.session["tasks"]+=task
            return HttpResponseRedirect(reverse("tasks:index"))
        else:
            return render(request, "tasks/add.html", {
                "form": form
            } )

    return render(request, "tasks/add.html", {
        "form": NewTaskForm()
    })

def remove(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data["task"]
            if task in request.session["tasks"]:
                request.session["tasks"].remove(task)
                request.session.modified = True
                return HttpResponseRedirect(reverse("tasks:index"))

        else:
            return render(request, "tasks/remove.html", {
                "form": form
            } )
    return render(request, "tasks/remove.html", {
        "form": NewTaskForm()
    })
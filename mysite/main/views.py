from http.client import HTTPResponse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList, Item
from .forms import CreateNewList

# Create your views here.

def index(response, id):
    ls = ToDoList.objects.get(id=id)

    if ls in response.user.todolist.all():
        if response.method == 'POST':
            if response.POST.get("save"):
                for item in ls.item_set.all():
                    if response.POST.get("c{}".format(item.id)) == "clicked":
                        item.complete = True
                    else:
                        item.complete = False
                    item.save()
            elif response.POST.get("newItem"):
                txt = response.POST.get("new")
                if len(txt) > 2:
                    ls.item_set.create(text=txt, complete=False)
                else:
                    print("invalid")

        return render(response, "main/list.html", {'ls':ls})
    return HttpResponseRedirect("/view")

def home(response):
    return render(response, "main/home.html", {})

def login(response):
    return HttpResponseRedirect("/login")

def create(response):
    if response.method == "POST":
        form = CreateNewList(response.POST)

        if form.is_valid():
            n = form.cleaned_data['name']
            t = ToDoList(name=n)
            t.save()
            response.user.todolist.add(t)

        return HttpResponseRedirect("/{}".format(t.id))
    else:
        form = CreateNewList()
    return render(response, "main/create.html", {'form':form})

def view(response):
    return render(response, "main/view.html", {})
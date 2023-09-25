from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import Entryform, TopicForm
from .models import Entry, Topic

# Create your views here.


def index(request):
    """Página principal"""
    return render(request, "learning_logs/index.html")


def topics(request):
    """Mostra os assuntos"""
    topics = Topic.objects.order_by("date_added")
    context = {"topics": topics}
    return render(request, "learning_logs/topics.html", context)


def topic(request, topic_id):
    """Mostra um único assunto com suas entradas"""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by("-date_added")
    context = {"topic": topic, "entries": entries}
    return render(request, "learning_logs/topic.html", context)


def new_topic(request):
    """Adiciona um novo assunto."""
    if request.method != "POST":
        # Nenhum dado submetido cria um formulário em branco
        form = TopicForm()
    else:
        # Dados de POST submetidos
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("topics"))

    context = {"form": form}
    return render(request, "learning_logs/new_topic.html", context)


def new_entry(request, topic_id):
    """Adiciona uma nova anotação"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != "POST":
        # Nenhum dado submetido cria um formulário em branco
        form = Entryform()
    else:
        # Dados de POST submetidos
        form = Entryform(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse("topic", args=[topic_id]))

    context = {"topic": topic, "form": form}
    return render(request, "learning_logs/new_entry.html", context)


def edit_entry(request, entry_id):
    """Edita uma anotação"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if request.method != "POST":
        # Requisição inicial para criar o formulário preenchido
        form = Entryform(instance=entry)

    else:
        # Dados de Post submetidos
        form = Entryform(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("topic", args=[topic.id]))

    context = {"entry": entry, "topic": topic, "form": form}
    return render(request, "learning_logs/edit_entry.html", context)


def delete_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if request.method == "POST":
        entry.delete()
        return HttpResponseRedirect(reverse("topic", args=[topic.id]))

    context = {"entry": entry, "topic": topic}
    return render(request, "learning_logs/delete_entry.html", context)

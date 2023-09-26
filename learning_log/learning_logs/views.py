from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import Entryform, TopicForm
from .models import Entry, Topic

# Create your views here.


def index(request):
    """Página principal"""
    return render(request, "learning_logs/index.html")


def page_404(request):
    """Página 404 da aplicação"""
    return render(request, "page_404.html")


@login_required
def topics(request):
    """Mostra os assuntos"""
    topics = Topic.objects.filter(owner=request.user).order_by("date_added")
    context = {"topics": topics}
    return render(request, "learning_logs/topics.html", context)


@login_required
def topic(request, topic_id):
    """Mostra um único assunto com suas entradas"""
    topic = Topic.objects.get(id=topic_id)
    # Somente permite ver anotações do tópico do usuário logado
    if topic.owner != request.user:
        return render(request, "learning_logs/page_404.html")
    else:
        entries = topic.entry_set.order_by("-date_added")
        context = {"topic": topic, "entries": entries}
        return render(request, "learning_logs/topic.html", context)


@login_required
def new_topic(request):
    """Adiciona um novo assunto."""
    if request.method != "POST":
        # Nenhum dado submetido cria um formulário em branco
        form = TopicForm()
    else:
        # Dados de POST submetidos
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            form.save()
            return HttpResponseRedirect(reverse("topics"))

    context = {"form": form}
    return render(request, "learning_logs/new_topic.html", context)


@login_required
def new_entry(request, topic_id):
    """Adiciona uma nova anotação"""
    topic = Topic.objects.get(id=topic_id)

    if topic.owner != request.user:
        return render(request, "learning_logs/page_404.html")
    else:
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


@login_required
def edit_entry(request, entry_id):
    """Edita uma anotação"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if topic.owner != request.user:
        return render(request, "learning_logs/page_404.html")

    else:
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


@login_required
def delete_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if topic.owner != request.user:
        return render(request, "learning_logs/page_404.html")
    else:
        if request.method == "POST":
            entry.delete()
            return HttpResponseRedirect(reverse("topic", args=[topic.id]))

        context = {"entry": entry, "topic": topic}
        return render(request, "learning_logs/delete_entry.html", context)

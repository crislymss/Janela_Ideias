from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Startup, MembroEquipe, RedesSociais, Contato
from .forms import StartupForm, ContatoForm, RedesSociaisForm, MembroEquipeFormSet
from django.shortcuts import render, redirect
from django.http import HttpResponse

def pagina_inicial(request):
    return HttpResponse("<h1>Projeto rodando...</h1>")
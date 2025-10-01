from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Startup, MembroEquipe, RedesSociais, Contato
from .forms import StartupForm, ContatoForm, RedesSociaisForm, MembroEquipeFormSet
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Noticia
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import NoticiaForm

def pagina_inicial(request):
    noticias = Noticia.objects.all().order_by('-data_publicacao')[:9]  
    return render(request, 'home.html', {'noticias': noticias})

class NoticiaListView(ListView):
    model = Noticia
    template_name = 'inova/noticia_list.html'  
    context_object_name = 'noticias'
    paginate_by = 9

class NoticiaDetailView(DetailView):
    model = Noticia
    template_name = 'inova/noticia_detail.html'

class NoticiaCreateView(LoginRequiredMixin, CreateView):
    model = Noticia
    form_class = NoticiaForm
    template_name = 'inova/noticia_form.html'
    success_url = reverse_lazy('noticia_list')

    def form_valid(self, form):
        form.instance.administrador = self.request.user
        return super().form_valid(form)

class NoticiaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Noticia
    form_class = NoticiaForm
    template_name = 'inova/noticia_form.html'
    success_url = reverse_lazy('noticia_list')

    def test_func(self):
        noticia = self.get_object()
        return noticia.administrador == self.request.user or self.request.user.is_superuser

class NoticiaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Noticia
    template_name = 'inova/noticia_confirm_delete.html'
    success_url = reverse_lazy('noticia_list')

    def test_func(self):
        noticia = self.get_object()
        return noticia.administrador == self.request.user or self.request.user.is_superuser
    


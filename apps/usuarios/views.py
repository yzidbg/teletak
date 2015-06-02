# -*- encoding: utf-8 -*-
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.utils.decorators import method_decorator
from django.views.generic import View, CreateView,TemplateView, ListView, DetailView, FormView
from .forms import LoginForm, RegistrarTrabajadorForm, EditarTrabajadorForm
from .models import User
from django.contrib.messages.views import SuccessMessageMixin


class LoginRequiredMixin(object):
    u"""Ensures that user must be authenticated in order to access view."""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class Login(View):
    form_class = LoginForm
    template_name = 'login/index.html'
    user_check_failure_path = '/login'

    def get(self, request):
        print request.user.is_authenticated
        if request.user.is_authenticated():
            return redirect('/')
        form = self.form_class()
        return render(request, self.template_name, {'form':form })

    def post(self,request):
        form = self.form_class(request.POST)

        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            if user.is_active:
                login(request, user)
                if request.GET:
                    return redirect(request.GET['next'])
                return redirect('/')
            return render(request, self.template_name, {'form': form, 'error': 'La cuenta esta deshabilitada'})

        else:
            return render(request, self.template_name, {'form': form, 'error': 'Verifique los datos ingresados'})



class Logout(View):

    def get(self,request):
            logout(request)
            return redirect('/login')


class Configuracion(TemplateView):
    template_name = 'configuracion/index.html'

class RegistrarTrabajador(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    model = User
    template_name = 'configuracion/nuevo_trabajador.html'
    form_class = RegistrarTrabajadorForm
    success_url = '/usuarios'
    success_message = 'El registro se realizó correctamente'

class ListarTrabajadores(LoginRequiredMixin,ListView):
    queryset = User.objects.filter(is_staff=False)
    template_name = 'configuracion/listar_trabajadores.html'


class EditarTrabajador(DetailView):
    model = User
    template_name = 'configuracion/editar_trabajador.html'

    def get_context_data(self, **kwargs):
        context = super(EditarTrabajador, self).get_context_data(**kwargs)
        context['form'] = EditarTrabajadorForm
        return context

class EditarTrabajadorFormView(FormView):
    form_class = EditarTrabajadorForm
    success_url = '/usuarios/list'









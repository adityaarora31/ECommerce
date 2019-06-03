from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.views.generic.base import View
from master.forms import ContactQueryForm
from .models import ContactQuery


def home(request):
    return render(request, "master/homepage.html")


def register(request):
    return render(request, "master/register.html")


def login(request):
    return render(request, "master/login.html")


def render_login_form(request):
    return render(request, 'master/login.html')


# def contact_us(request):
#     return render(request, 'contact_us.html')
#
#
# class ContactQuery(FormView):
#
#     form_class = ContactQueryForm
#     template_name = 'contact_us.html'
#
#     def form_valid(self, form):
#         form.save()
#         # return render(request, 'contact_us.html', 'form': form)
#
#     def form_invalid(self, form):
#         return render(self.request, self.template_name, {'form': form, 'error': form.errors})


# class ContactView(View):
#
#     def get(self, request):
#         form = ContactQueryForm()
#         context = {'form': form}
#         return render(request, 'contact_us.html', context)
#
#     def post(self, request):
#         form = ContactQueryForm(request.POST)
#         if form.is_valid():
#             form.save()
#             form = ContactQueryForm()
#             return render(request, 'contact_us.html', {'form': form})
#         return render(request, 'contact_us.html', {'form': form})
#
def contact_us(request):
    form = ContactQueryForm()
    if request.method == 'POST':
        form = ContactQueryForm(request.POST)
        if form.is_valid():

            # import pdb;pdb.set_trace()
            form.save()

            return HttpResponseRedirect('/contact/')

        else:
            form = ContactQueryForm()
    return render(request, 'contact_us.html', {'form': form})

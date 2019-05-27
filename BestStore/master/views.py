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

def contact_us(request):
    form = ContactQueryForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            text = form.cleaned_data['query']

            new_query = ContactQuery()
            new_query.name = name
            new_query.email = email
            new_query.subject = subject
            new_query.query = text
            new_query.save()

            return HttpResponseRedirect('/contact/')

        else:
            form = ContactQueryForm()
    return render(request, 'contact_us.html', {'form': form})

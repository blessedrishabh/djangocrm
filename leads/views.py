from typing import Any, Dict
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import lead, Agent, Category
from django.http import HttpResponse
from .forms import LeadForm, LeadModelForm, CustomUserCreationForm, AssignAgentForm
from django.views.generic import TemplateView, CreateView, DetailView, DeleteView, ListView, UpdateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganizerAndLoginRequiredMixin
from django.core.mail import send_mail

# Create your views here.
class SignupView(CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm
    def get_success_url(self):
        return reverse('login')

#class based landing_page view
class LandingPage(TemplateView):
    template_name = "landing_page.html"

# def landing_page(request):
#     return render(request, 'landing_page.html')

#class based List View
class LeadListView(LoginRequiredMixin,ListView):

    template_name = "leads\leads_list.html"
    context_object_name = "lead"

    def get_queryset(self):
        user = self.request.user

        if user.is_organizer:
            queryset = lead.objects.filter(organization = user.userprofile, agent__isnull = False)
        else:
            queryset = lead.objects.filter(organization= user.agent.organization, agent__isnull = False)
            queryset = lead.objects.filter(agent__user = user)
        return queryset
    def get_context_data(self, **kwargs):
        context =  super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organizer:
            queryset = lead.objects.filter(organization = user.userprofile, agent__isnull = True)
            context.update({
                "unassigned_leads":queryset
            })
        return context
    # def leads_list(request):
#     leads = lead.objects.all() 
#     context = {
#         "lead": leads
#     }
#     return render(request, 'leads\leads_list.html', context)


class LeadDetailView(LoginRequiredMixin,DetailView):
    template_name="leads\leads_details.html"
    context_object_name="lead"

    def get_queryset(self):
        user = self.request.user

        if user.is_organizer:
            queryset = lead.objects.filter(organization = user.userprofile)
        else:
            queryset = lead.objects.filter(organization= user.agent.organization)
            queryset = lead.objects.filter(agent__user = user)
        return queryset
# def leads_details(request, pk):
#     leads = lead.objects.get(id=pk)
#     context = {
#         "lead": leads
#     }
#     return render(request, 'leads\leads_details.html', context)
class LeadCreateView(OrganizerAndLoginRequiredMixin,CreateView):
    template_name = "leads\lead_form.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return "/leads/leads"
    
    def form_valid(self, form):
        lead = form.save(commit =False)
        lead.organization = self.request.user.userprofile
        lead.save()
        send_mail(
            subject = "A lead has been created",
            message = "Go to the site to see the new lead",
            from_email= "test123@gmail.com",
            recipient_list=['receiver@gmail.com'],

        )
        
        return super(LeadCreateView, self).form_valid(form)

# def lead_model_form(request):
#     if(request.method == 'POST'):
#         form = LeadModelForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('/leads')
#     context = {
#         'LeadForm': LeadModelForm()
#     }
#     return render(request,'leads\lead_form.html', context)

class LeadUpdateView(OrganizerAndLoginRequiredMixin,UpdateView):
    template_name= "leads\lead_update.html"
    form_class = LeadModelForm
    def get_success_url(self):
        return "/leads/leads"
    def get_queryset(self):
        user = self.request.user

        if user.is_organizer:
            queryset = lead.objects.filter(organization = user.userprofile)
        return queryset

# def lead_update(request, pk):
#     leads = lead.objects.get(id=pk)
#     form = LeadModelForm(instance=leads)
#     if(request.method == 'POST'):
#         form = LeadModelForm(request.POST, instance=leads)
#         if form.is_valid():
#             form.save()
#             return redirect("/leads")
#     context = {
#         "form": form,
#     }
#     return render(request, "leads\lead_update.html", context)
class LeadDeleteView(OrganizerAndLoginRequiredMixin,DeleteView):
    template_name = "leads/lead_delete.html"
    
    def get_success_url(self):
        return "/leads/leads"
    def get_queryset(self):
        user = self.request.user

        if user.is_organizer:
            queryset = lead.objects.filter(organization = user.userprofile)
        return queryset

    

# def lead_delete(request, pk):
#     leads = lead.objects.get(id=pk)
#     leads.delete()
#     return "/leads/leads"


class AssignAgent(OrganizerAndLoginRequiredMixin, FormView):
    template_name = "leads/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgent, self).get_form_kwargs(**kwargs)

        kwargs.update({
            "request":self.request
        })
        return kwargs
    
    def get_success_url(self):
        return reverse('leads:leads-list')
    
    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        leads = lead.objects.get(id = self.kwargs["pk"])
        leads.agent = agent
        leads.save()
        return super(AssignAgent, self).form_valid(form)

# def leads_form(request):

#     if(request.method == 'POST'):
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             agent = Agent.objects.first()
#             lead.objects.create(
#                 first_name=first_name,
#                 last_name=last_name,
#                 age=age,
#                 agent = agent,
#             )
#             print("Lead has been created")
#             return redirect('/leads')
#     context = {
#         'LeadForm': LeadForm()
#     }
#     return render(request,'leads/lead_form.html', context)

class CategoryListView(LoginRequiredMixin, ListView):
    template_name = "leads/category_list.html"
    context_object_name = "category_list"

    def get_context_data(self, **kwargs):
        context =  super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organizer:
            queryset = lead.objects.filter(organization = user.userprofile)
        else:
            queryset = lead.objects.filter(organization= user.agent.organization)

        context.update({
            "unassigned_leads_count": queryset.filter(category__isnull=True).count()
        })
        return context



    def get_queryset(self):
        user = self.request.user

        if user.is_organizer:
            queryset = Category.objects.filter(organization = user.userprofile)
        else:
            queryset = Category.objects.filter(organization= user.agent.organization)
        return queryset
    
class CategoryDetailView(LoginRequiredMixin, DetailView):
    template_name = "leads/category_detailview.html"
    context_object_name = "category"

    # def get_context_data(self, **kwargs):
    #     context =  super(CategoryDetailView, self).get_context_data(**kwargs)
    #     leads = self.get_object().leads.all()

    #     context.update({
    #         "lead":leads
    #     })
    #     return context

    def get_queryset(self):
        user = self.request.user

        if user.is_organizer:
            queryset = Category.objects.filter(organization = user.userprofile)
        else:
            queryset = Category.objects.filter(organization= user.agent.organization)
        return queryset
    


    
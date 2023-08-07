from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from leads.models import Agent
from django.urls import reverse
from .forms import AgentCreateForm
from .mixins import OrganizerAndLoginRequiredMixin
from django.core.mail import send_mail
import random
# Create your views here.

class AgentListView(OrganizerAndLoginRequiredMixin, generic.ListView ):
    template_name = "agents/agent_list.html"

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization = organization)
    
class AgentCreateView(OrganizerAndLoginRequiredMixin, generic.CreateView):
    template_name = 'agents/agent_create.html'
    form_class = AgentCreateForm

    def get_success_url(self):
        return reverse('agents:agent-list')
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organizer = False
        #specific method of user that create the password and hash it
        user.set_password(f"{random.randint(9999999, 100000000)}") 
        user.save()
        Agent.objects.create(
            user = user,
            organization = self.request.user.userprofile,
        )

        send_mail(
            subject="You are invited as a agent to our CRM",
            message="You can currently login via the given credentials but don't forgot to  change the password",
            from_email="rishabhsharma5923@gmail.com",
            recipient_list= [user.email],
            fail_silently=False,
        )
        # agent.organization = self.request.user.userprofile
        # agent.save()
        return super(AgentCreateView, self).form_valid(form)
    
class AgentDetailView(OrganizerAndLoginRequiredMixin, generic.DetailView):
    template_name = 'agents/agent_detail.html'
    queryset = Agent.objects.all()
    context_object_name = 'agent'

class AgentUpdateView(OrganizerAndLoginRequiredMixin, generic.UpdateView):
    template_name = 'agents/agent_update.html'
    queryset = Agent.objects.all()
    form_class = AgentCreateForm

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization = organization)
    def get_success_url(self):
        return reverse('agents:agent-list')
    
class AgentDeleteView(OrganizerAndLoginRequiredMixin, generic.DeleteView):
    template_name = 'agents/agent_delete.html'
    queryset = Agent.objects.all()
    
    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization = organization)
    
    def get_success_url(self):
        return reverse('agents:agent-list')

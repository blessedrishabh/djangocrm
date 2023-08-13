from django.urls import path
from leads.views import LeadListView, LeadDetailView, LeadCreateView, LeadUpdateView, LeadDeleteView, AssignAgent, CategoryListView, CategoryDetailView

app_name = 'leads'

urlpatterns = [
    path('leads/', LeadListView.as_view(), name="leads-list"),
    path('<int:pk>/', LeadDetailView.as_view(), name="leads-details"),
    path('update/<int:pk>', LeadUpdateView.as_view(), name= "lead-update"),
    path('delete/<int:pk>/', LeadDeleteView.as_view(), name="lead-delete"),
    path('assign-agent/<int:pk>/', AssignAgent.as_view(), name = 'assign-agent'),
    path('category-list/', CategoryListView.as_view(), name = "category-list"),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name = 'category'),
    path('create/', LeadCreateView.as_view(), name="lead-model-form"),
]
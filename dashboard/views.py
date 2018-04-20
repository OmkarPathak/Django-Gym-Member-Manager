from django.shortcuts import render
from django.views.generic import TemplateView


class DashboardView(TemplateView):
    """Show dashboard."""
    template_name = 'dashboard.html'

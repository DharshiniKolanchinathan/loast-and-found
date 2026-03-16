from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from .models import LostItem, FoundItem, MatchResult
from .forms import LostItemForm, FoundItemForm
from .services import find_matches_for_lost_item, find_matches_for_found_item

class DashboardView(LoginRequiredMixin, ListView):
    template_name = 'items/dashboard.html'
    context_object_name = 'recent_lost'
    
    def get_queryset(self):
        return LostItem.objects.filter(is_active=True).order_by('-date_reported')[:5]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_found'] = FoundItem.objects.filter(is_active=True).order_by('-date_reported')[:5]
        context['user_lost'] = LostItem.objects.filter(user=self.request.user)
        # Get matches where user is either the loser or the finder
        user_matches = MatchResult.objects.filter(
            Q(lost_item__user=self.request.user) | Q(found_item__user=self.request.user)
        ).distinct().order_by('-similarity_score')
        context['matches'] = user_matches
        return context

class LostItemListView(ListView):
    model = LostItem
    template_name = 'items/lost_list.html'
    context_object_name = 'items'
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        cat = self.request.GET.get('category')
        objs = LostItem.objects.filter(is_active=True)
        if query:
            objs = objs.filter(Q(name__icontains=query) | Q(description__icontains=query))
        if cat:
            objs = objs.filter(category=cat)
        return objs

class FoundItemListView(ListView):
    model = FoundItem
    template_name = 'items/found_list.html'
    context_object_name = 'items'
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        cat = self.request.GET.get('category')
        objs = FoundItem.objects.filter(is_active=True)
        if query:
            objs = objs.filter(Q(name__icontains=query) | Q(description__icontains=query))
        if cat:
            objs = objs.filter(category=cat)
        return objs

class ReportLostView(LoginRequiredMixin, CreateView):
    model = LostItem
    form_class = LostItemForm
    template_name = 'items/report_item.html'
    success_url = reverse_lazy('dashboard')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        # Trigger matching service
        find_matches_for_lost_item(self.object)
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Report Lost Item"
        return context

class ReportFoundView(LoginRequiredMixin, CreateView):
    model = FoundItem
    form_class = FoundItemForm
    template_name = 'items/report_item.html'
    success_url = reverse_lazy('dashboard')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        # Trigger matching service
        find_matches_for_found_item(self.object)
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Report Found Item"
        return context

class LostItemDetailView(DetailView):
    model = LostItem
    template_name = 'items/lost_detail.html'
    context_object_name = 'item'

class FoundItemDetailView(DetailView):
    model = FoundItem
    template_name = 'items/found_detail.html'
    context_object_name = 'item'

class LostItemDeleteView(LoginRequiredMixin, DeleteView):
    model = LostItem
    template_name = 'items/item_confirm_delete.html'
    success_url = reverse_lazy('dashboard')
    
    def get_queryset(self):
        # Ensure only the owner can delete
        return self.model.objects.filter(user=self.request.user)

class FoundItemDeleteView(LoginRequiredMixin, DeleteView):
    model = FoundItem
    template_name = 'items/item_confirm_delete.html'
    success_url = reverse_lazy('dashboard')
    
    def get_queryset(self):
        # Ensure only the owner can delete
        return self.model.objects.filter(user=self.request.user)

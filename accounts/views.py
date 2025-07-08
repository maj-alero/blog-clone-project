from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from Main_Blog.models import Post  # Assuming you have a Post model in Main_Blog
from .forms import CustomUserCreationForm  # Assuming you have a custom form for user creation

class SignUpView(CreateView):
    form_class = CustomUserCreationForm # Use your custom user creation form
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')  # or wherever you want to redirect
    
    def form_valid(self, form):
        user = form.save()
        username = form.cleaned_data.get('username')
        login(self.request, user)  # Auto-login after signup
        messages.success(self.request, f'Welcome {username}!')
        return redirect('/')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Sign Up'
        return context

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Profile'
        context['user'] = self.request.user
        context['user_posts'] = Post.objects.filter(author=self.request.user).order_by('-published_date')
        return context
    

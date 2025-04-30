from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.forms import UserCreationForm

from django.urls import reverse_lazy, reverse
from .models import Post,Comment
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostForm, CommentForm
# Create your views here.

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte= timezone.now()).order_by('-published_date')
    
class PostDetailView(DetailView):
    model = Post

class CreatePostView(LoginRequiredMixin,CreateView):
    model = Post
    login_url = 'login'
    redirect_field_name = 'Main_Blog/post_detail.html'
    form_class = PostForm

class PostUpdateView(LoginRequiredMixin,UpdateView):
    model = Post
    form_class = PostForm
    login_url = '/login/'
    redirect_field_name = 'Main_Blog/post_detail.html'

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')
    login_url = '/login/'
    redirect_field_name = 'Main_Blog/post_list.html'


class DraftListView(LoginRequiredMixin,ListView):
    model = Post
    # template_name = 'Main_Blog/post_draft_list.html'
    login_url = '/login/'
    redirect_field_name = 'Main_Blog/post_draft__list.html'

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('-created_date')
    


@login_required
def add_comment_to_post(request,pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
         
    else:
        form = CommentForm()
    return render(request,'Main_Blog/comment_form.html',{'form':form})

@login_required
def approve_comment(request,pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)
        
@login_required
def delete_comment(request,pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk) 

@login_required
def publish_post(request,pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

def search_view(request):
    query = request.GET.get("q", "")
    results = Post.objects.filter(title__icontains=query) if query else []
    return render(request, "search_results.html", {"query": query, "results": results})
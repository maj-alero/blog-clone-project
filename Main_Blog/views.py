from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import (TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.contrib.auth.forms import UserCreationForm

from django.urls import reverse_lazy, reverse
from .models import Post,Comment
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.http import Http404
from django.db.models import Q 
from .forms import PostForm, CommentForm
# Create your views here.



class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = Post
    paginate_by = 10  # Number of posts to display per page

    def get_queryset(self):
        return Post.objects.filter(published_date__lte= timezone.now()).order_by('-published_date')
    
class PostDetailView(DetailView):
    model = Post

class CreatePostView(LoginRequiredMixin,CreateView):
    model = Post
    login_url = 'login'
    redirect_field_name = 'Main_Blog/post_detail.html'
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user # Set the author to the current user
        messages.success(self.request, 'Post created successfully!') # Show a success message after the post is created
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UpdateView):
    model = Post
    form_class = PostForm
    login_url = 'login'
    redirect_field_name = 'Main_Blog/post_detail.html'

    def form_valid(self, form):
        if form.instance.author != self.request.user: # Check if the author of the post is the current user
            raise Http404("You are not allowed to edit this post.")
        messages.success(self.request, 'Post updated successfully!')
        return super().form_valid(form) 

class PostDeleteView(LoginRequiredMixin,DeleteView, UserPassesTestMixin):
    model = Post
    success_url = reverse_lazy('post_list') # Redirect to the post list after deletion
    login_url = 'login'
    
    # This method is used to check if the user has permission to delete the post
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Post deleted successfully!')
        return super().delete(request, *args, **kwargs) # Call the parent class's delete method to handle the deletion


class DraftListView(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'Main_Blog/post_draft_list.html'
    login_url = 'login'
    paginate_by = 10  # Number of drafts to display per page`

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Drafts'
        context['drafts'] = Post.objects.filter(published_date__isnull=True, author=self.request.user).order_by('-created_date')
        return context
    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True, author = self.request.user).order_by('-created_date')
    


@login_required
def add_comment_to_post(request,pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.success(request, 'Comment added successfully!')
            # Redirect to the post detail page after adding the comment
            return redirect('post_detail', pk=post.pk)
         
    else:
        form = CommentForm()
    return render(request,'Main_Blog/comment_form.html',{'form':form})

@login_required
def approve_comment(request,pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.post.author:
        # If the comment author is not the post author is also not the
        raise Http404("You are not allowed to approve this comment.")
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)
        
@login_required
def delete_comment(request,pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    if comment.author != request.user and request.user != comment.post.author:
        # If the comment author is not the current user and the post author is also not the
        raise Http404("You are not allowed to delete this comment.")
    comment.delete()
    messages.success(request, 'Comment deleted successfully!')
    # Redirect to the post detail page after deleting the comment
    return redirect('post_detail', pk=post_pk) 

@login_required
def publish_post(request,pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.error(request, 'You are not allowed to publish this post.')
        return redirect('post_detail', pk=pk)
    post.publish()
    messages.success(request, 'Post published successfully!')
    # Redirect to the post detail page after publishing
    return redirect('post_detail', pk=pk)

def search_view(request):
    query = request.GET.get("q", "")
    results = []
    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) | Q(text__icontains=query),
            published_date__lte=timezone.now()
        ).order_by('-published_date')
    
    return render(request, "Main_Blog/search_results.html", {
        "query": query, 
        "results": results
    })
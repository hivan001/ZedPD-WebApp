from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

def home(request):

    return render(request,'news/home.html')


class PostListView(ListView):
      model = Post
      template_name = 'news/main.html'
      context_object_name = 'posts'
      ordering = ['-date_posted']
      paginate_by = 10


class UserPostListView(ListView):
      model = Post
      template_name = 'news/user_posts.html'
      context_object_name = 'posts'
      paginate_by = 10

      def get_queryset(self):
           user = get_object_or_404(User, username=self.kwargs.get('username'))
           return Post.objects.filter(author=user).order_by('-date_posted')
           

class PostDetailView(DetailView):
      model = Post
      context_object_name = 'post'

class PostCreateView(LoginRequiredMixin,CreateView):
      model = Post
      context_object_name = 'post'
      fields = ['title', 'content']

#overides the form_valid method to set the author of the post
      def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
      

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
      model = Post
      context_object_name = 'post'
      fields = ['title', 'content']

#overides the form_valid method to set the author of the post
      def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
      
      def test_func(self):
           post = self.get_object()
           if self.request.user == post.author:
                return True
           return False
      

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
      model = Post
      context_object_name = 'post'
      success_url = '/main'

      def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def news(request):
        context = {
        'posts': Post.objects.all()
    }
        return render(request,'news/main.html', context)

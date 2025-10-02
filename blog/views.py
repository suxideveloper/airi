from django.shortcuts import render, get_object_or_404, redirect 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Post, Category,Tag, Comment, PostView
from .forms import CommentForm



def post_list(request):
    
    posts = Post.objects.filter(status = "published").select_related('author', 'category').prefetch_related('tags')
    print(posts)

    # Search functionslatiy 
    search_query = request.GET.get('search')
    if search_query:
        posts = posts.filter(
            Q(title__icontains = search_query) |
            Q(content_icontains = search_query) |
            Q(excerpt__icontains = search_query)
      )
        

    # Category filtering 
    category_slug = request.GET.get('category')
    if category_slug:
        posts = posts.filter(category__slug = category_slug)
    

    # Tag filtering
    tag_slug = request.GET.get('tag')
    if tag_slug:
        posts = posts.filter(tag__slug = tag_slug)

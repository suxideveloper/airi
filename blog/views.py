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
# from .forms import CommentForm



def post_list(request):
    
    posts = Post.objects.filter(status = "published").select_related('author', 'category').prefetch_related('tags')
    print(posts)

    # Search functionslatiy 
    search_query = request.GET.get('search')
    if search_query:
        posts = posts.filter(
            Q(title__icontains = search_query) |
            Q(content__icontains = search_query) |
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

    # Author filtering
    author_username = request.GET.get('author')
    if author_username:
        posts = posts.filter(author__username = author_username)

    # Pagination 
    paginator = Paginator(posts, 6)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    # Get categories and tags for sidebars 
    categories = Category.objects.annotate(
        post_count = Count('posts', filter=Q(posts__status = 'published'))
    ).filter(post_count__gt = 0)

    tags = Tag.objects.annotate(
        post_count = Count('posts', filter = Q(posts__status = 'published'))
    ).filter(post_count__gt = 0)
    
    recent_posts = Post.objects.filter(status = 'published').select_related('author')[:5]

    context = {
        'posts': posts,
        'categories': categories,
        'tags': tags,
        'recent_posts': recent_posts,
        'search_query': search_query,
        'current_category':category_slug,
        'current_tag': tag_slug,
        'current_author': author_username,
    }

    return render(request, 'blog/post_list.html', context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    
    # Track view
    ip_address = request.META.get('REMOTE_ADDR')
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    
    # Only create view record if it doesn't exist for this IP and post
    PostView.objects.get_or_create(
        post=post,
        ip_address=ip_address,
        defaults={'user_agent': user_agent}
    )
    
    # Get related posts
    related_posts = Post.objects.filter(
        status='published',
        category=post.category
    ).exclude(id=post.id)[:3]
    
    # Get comments
    comments = post.comments.filter(is_approved=True, parent=None)
    
    context = {
        'post': post,
        'related_posts': related_posts,
        'comments': comments,
    }
    
    return render(request, 'blog/post_detail.html', context)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(
        status='published',
        category=category
    ).select_related('author', 'category').prefetch_related('tags')
    
    # Pagination
    paginator = Paginator(posts, 6)
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    context = {
        'category': category,
        'posts': posts,
    }
    
    return render(request, 'blog/category_detail.html', context)


def tag_detail(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(
        status='published',
        tags=tag
    ).select_related('author', 'category').prefetch_related('tags')
    
    # Pagination
    paginator = Paginator(posts, 6)
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    context = {
        'tag': tag,
        'posts': posts,
    }
    
    return render(request, 'blog/tag_detail.html', context)
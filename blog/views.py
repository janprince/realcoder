from django.shortcuts import render
from .models import *
from django.db.models import Q
from .forms import *
from django.contrib import messages
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage


# Create your views here.

# global stuff
popular_posts = Post.objects.filter(popular=True, featured=True)
categories = Category.objects.all()
tags = Tag.objects.filter(popular=True)


def index(request):
    posts = Post.objects.filter(featured=True)

    # Pagination - My most impressive implementation
    paginator = Paginator(posts, 3)
    num_pages = [i for i in range(1, paginator.num_pages)]
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        post_list = paginator.page(1)
    except EmptyPage:
        # if page is out of range, deliver last page of results
        post_list = paginator.page(paginator.num_pages)

    context = {
        "posts": post_list,
        "num_pages": num_pages,

        "popular_tags": tags,
        "popular_posts": popular_posts,
        "categories": categories,
    }
    return render(request, "blog/index.html", context)


def detail(request, post_slug):
    post = Post.objects.get(slug=post_slug)
    comments = post.comments.filter(active=True)
    post_tags = post.tags.all()

    new_comment = None
    # comment posted
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            # Create a comment but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
            messages.success(request, "Your comment is awaiting moderation.")
    else:
        comment_form = CommentForm()


    context = {
        "post": post,
        "comments": comments,
        "post_tags": post_tags,
        "new_comment": new_comment,
        # sidebars
        "categories": categories,
        "popular_posts": popular_posts,
        "popular_tags": tags,
    }
    return render(request, "blog/detail.html", context)


def category(request, cat_slug):
    cat = Category.objects.get(slug=cat_slug)
    posts = cat.posts.filter(featured=True)

    context = {
        "posts": posts,
        "category": cat,

        # sidebar
        "popular_posts": popular_posts,
        "categories": categories,
        "popular_tags": tags,
    }
    return render(request, "blog/category.html", context)


def tag(request, tag_slug):
    tag_ = Tag.objects.get(slug=tag_slug)
    posts = tag_.posts.filter(featured=True)

    context = {
        "posts": posts,
        "tag": tag_,

        # sidebar
        "popular_posts": popular_posts,
        "categories": categories,
        "popular_tags": tags,
    }
    return render(request, "blog/tag.html", context)


def contact(request):

    # message sent
    if request.method == "POST":
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            messages.success(request, "Message Sent.")
    else:
        contact_form = CommentForm()

    return render(request, "blog/contact.html")


def about(request):
    context = {
        "popular_posts": popular_posts,
        "popular_tags": tags,
        "categories": categories,
    }
    return render(request, "blog/about.html", context)


def robots(request):
    return render(request, "blog/robots.txt", content_type="text/plain")


def ads(request):
    return render(request, "blog/ads.txt", content_type="text/plain")


# View to handle Search
def search(request):
    if request.GET.get('q'):
        query = request.GET.get('q')
        # query.split() # Todo
        query_list = Post.objects.filter(Q(title__icontains=query), featured=True)   # Note: two underscores
        context = {
            'posts': query_list,
            'query_count': len(query_list),
            'q': query,

            # sidebar
            "popular_posts": popular_posts,
            "categories": categories,
            "popular_tags": tags,
        }
        return render(request, 'blog/search.html', context)
    else:
        return render(request, "blog/search.html", {
            'categories': categories,
        })

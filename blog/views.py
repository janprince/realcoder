from django.shortcuts import render

# Create your views here.


def index(request):
    context = {

    }
    return render(request, "blog/index.html", context)


def detail(request, post_slug):
    context = {

    }
    return render(request, "blog/detail.html", context)


def category(request, cat_slug):
    context = {

    }
    return render(request, "blog/category.html", context)


def contact(request):
    return render(request, "blog/contact.html")


def about(request):
    return render(request, "blog/about.html")


def robots(request):
    return render(request, "blog/robots.txt", content_type="text/plain")


def ads(request):
    return render(request, "blog/ads.txt", content_type="text/plain")

from django.contrib.sitemaps import Sitemap
from .models import Post, Category
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return ["blog:index"]

    def location(self, obj):
        return reverse(obj)


class PostSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.9

    def items(self):
        return Post.objects.filter(featured=True)

    def lastmod(self, obj):
        return obj.pub_date


class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority =  0.8

    def items(self):
        return Category.objects.all()
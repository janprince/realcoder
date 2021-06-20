from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
    path("", views.index, name="index"),
    path("post/<slug:post_slug>/", views.detail, name="detail"),
    path("category/<slug:cat_slug>/", views.category, name="category"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),

    path("robots.txt", views.robots, name="robots"),
    path("ads.txt", views.ads, name="ads"),
]
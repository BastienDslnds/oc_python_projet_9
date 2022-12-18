"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import review.views
import users.views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("home", users.views.login_page, name='login'),
    path("signup", users.views.signup_page, name='signup'),
    path("feed", review.views.feed, name='feed'),
    path("posts", review.views.posts, name='posts'),
    path("feed/add-review", review.views.add_review, name='add_review'),
    path(
        "feed/tickets/<int:ticket_id>/add-review",
        review.views.add_review_to_ticket,
        name='add_ticket_review',
    ),
    path("feed/add-ticket", review.views.add_ticket, name='add_ticket'),
    path(
        "posts/reviews/<int:review_id>/change",
        review.views.change_review,
        name='change_review',
    ),
    path(
        "posts/ticket/<int:ticket_id>/change",
        review.views.change_ticket,
        name='change_ticket',
    ),
    path(
        "posts/reviews/<int:review_id>/delete",
        review.views.delete_review,
        name='change_review',
    ),
    path(
        "posts/ticket/<int:ticket_id>/delete",
        review.views.delete_ticket,
        name='delete_ticket',
    ),
    path("logout", users.views.logout_page, name='logout'),
]

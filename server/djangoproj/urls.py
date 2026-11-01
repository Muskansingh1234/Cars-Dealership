from django.contrib import admin
from django.urls import include, path

from djangoapp import pages, views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("djangoapp/", include("djangoapp.urls")),
    # Convenience alias for the sentiment service: /analyze/<text>
    path("analyze/<str:text>", views.analyze_review),
    # Frontend pages
    path("", pages.home, name="home"),
    path("dealers/", pages.home, name="dealers"),
    path("about/", pages.about, name="about"),
    path("contact/", pages.contact, name="contact"),
    path("login/", pages.login_page, name="login-page"),
    path("register/", pages.register_page, name="register-page"),
    path("dealer/<int:dealer_id>/", pages.dealer_page, name="dealer-page"),
    path("postreview/<int:dealer_id>/", pages.post_review_page, name="postreview-page"),
]

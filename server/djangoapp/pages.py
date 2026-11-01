"""Serve the static frontend pages (server/frontend/static/*.html)."""
from django.conf import settings
from django.http import Http404, HttpResponse


def _page(filename):
    path = settings.FRONTEND_DIR / "static" / filename
    if not path.exists():
        raise Http404(f"{filename} not found")
    return HttpResponse(path.read_text(encoding="utf-8"), content_type="text/html; charset=utf-8")


def home(request):
    return _page("Home.html")


def about(request):
    return _page("About.html")


def contact(request):
    return _page("Contact.html")


def login_page(request):
    return _page("Login.html")


def register_page(request):
    return _page("Register.html")


def dealer_page(request, dealer_id):
    return _page("Dealer.html")


def post_review_page(request, dealer_id):
    return _page("PostReview.html")

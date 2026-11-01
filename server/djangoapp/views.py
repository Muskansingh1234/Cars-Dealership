import datetime
import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from .models import CarModel, Dealer, Review
from .sentiment import analyze


def _json_body(request):
    try:
        data = json.loads(request.body or b"{}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None
    return data if isinstance(data, dict) else None


def _bad_request(message="Invalid JSON body"):
    return JsonResponse({"status": 400, "message": message}, status=400)


# ----------------------------------------------------------------- auth
@csrf_exempt
@require_POST
def login_user(request):
    data = _json_body(request)
    if data is None:
        return _bad_request()
    username = data.get("userName", "")
    user = authenticate(username=username, password=data.get("password", ""))
    if user is None:
        return JsonResponse({"userName": username, "status": "Invalid credentials"}, status=401)
    login(request, user)
    return JsonResponse({"userName": username, "status": "Authenticated"})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def logout_user(request):
    logout(request)
    return JsonResponse({"userName": ""})


@csrf_exempt
@require_POST
def registration(request):
    data = _json_body(request)
    if data is None:
        return _bad_request()
    username = str(data.get("userName", "")).strip()
    password = str(data.get("password", ""))
    first_name = str(data.get("firstName", "")).strip()
    last_name = str(data.get("lastName", "")).strip()
    email = str(data.get("email", "")).strip()
    if not (username and password and first_name and last_name and email):
        return _bad_request("All five fields are required")
    if len(password) < 8:
        return _bad_request("Password must be at least 8 characters")
    if User.objects.filter(username__iexact=username).exists():
        return JsonResponse({"userName": username, "error": "Already Registered"}, status=409)
    user = User.objects.create_user(
        username=username, password=password, first_name=first_name,
        last_name=last_name, email=email,
    )
    login(request, user)
    return JsonResponse({"userName": username, "status": "Authenticated"})


@require_GET
def current_user(request):
    if request.user.is_authenticated:
        return JsonResponse({"userName": request.user.username})
    return JsonResponse({"userName": ""})


# -------------------------------------------------------------- dealers
@require_GET
def get_dealers(request, state=None):
    dealers = Dealer.objects.all()
    if state:
        dealers = dealers.filter(Q(state__iexact=state) | Q(st__iexact=state))
    return JsonResponse({"status": 200, "dealers": [d.to_dict() for d in dealers.order_by("id")]})


@require_GET
def get_dealer_details(request, dealer_id):
    try:
        dealer = Dealer.objects.get(pk=dealer_id)
    except Dealer.DoesNotExist:
        return JsonResponse({"status": 404, "message": "Dealer not found"}, status=404)
    return JsonResponse({"status": 200, "dealer": [dealer.to_dict()]})


@require_GET
def get_dealer_reviews(request, dealer_id):
    if not Dealer.objects.filter(pk=dealer_id).exists():
        return JsonResponse({"status": 404, "message": "Dealer not found"}, status=404)
    reviews = Review.objects.filter(dealership_id=dealer_id).order_by("id")
    return JsonResponse({"status": 200, "reviews": [r.to_dict() for r in reviews]})


@csrf_exempt
@require_POST
def add_review(request):
    if not request.user.is_authenticated:
        return JsonResponse({"status": 401, "message": "Login required"}, status=401)
    data = _json_body(request)
    if data is None:
        return _bad_request()
    text = str(data.get("review", "")).strip()
    if not text:
        return _bad_request("Review text is required")
    try:
        dealer = Dealer.objects.get(pk=int(data.get("dealership")))
    except (TypeError, ValueError, Dealer.DoesNotExist):
        return _bad_request("Unknown dealership")

    purchase_date = None
    if data.get("purchase_date"):
        try:
            purchase_date = datetime.date.fromisoformat(str(data["purchase_date"]))
        except ValueError:
            return _bad_request("purchase_date must be YYYY-MM-DD")
    try:
        car_year = int(data["car_year"]) if data.get("car_year") not in (None, "") else None
    except (TypeError, ValueError):
        return _bad_request("car_year must be a number")

    label, _ = analyze(text)
    review = Review.objects.create(
        dealership=dealer,
        user=request.user,
        name=str(data.get("name") or request.user.get_full_name() or request.user.username),
        review=text,
        purchase=bool(data.get("purchase", False)),
        purchase_date=purchase_date,
        car_make=str(data.get("car_make", "")),
        car_model=str(data.get("car_model", "")),
        car_year=car_year,
        sentiment=label,
    )
    return JsonResponse({"status": 200, "review": review.to_dict()})


# ----------------------------------------------------------- cars / ML
@require_GET
def get_cars(request):
    models = CarModel.objects.select_related("car_make").order_by("car_make__name", "name")
    cars = [
        {"CarModel": m.name, "CarMake": m.car_make.name, "Type": m.type, "Year": m.year}
        for m in models
    ]
    return JsonResponse({"CarModels": cars})


@require_GET
def analyze_review(request, text):
    label, score = analyze(text)
    return JsonResponse({"text": text, "sentiment": label, "score": score})

# Cars Dealership — Full-Stack Capstone

| | |
|---|---|
| **Project name** | Cars Dealership – Full-Stack Developer Capstone |
| **Repository name** | `xrwvm-fullstack-developer-capstone` *(change this line if your GitHub repo has a different name)* |

A responsive web app for a national U.S. car retailer: browse dealership branches, filter by state, read customer
reviews with sentiment labels, and post your own review after logging in.

## Stack
- **Backend:** Django 4.2+ / SQLite (dealers, reviews, car makes & models, auth), JSON APIs under `/djangoapp/`
- **Frontend:** responsive HTML/CSS/JS pages in `server/frontend/static`, React sign-up component in `server/frontend/src/components/Register/Register.jsx`
- **Sentiment analysis:** dependency-free lexicon analyser (`server/djangoapp/sentiment.py`), exposed at `/djangoapp/analyze/<text>`
- **DevOps:** Dockerfile, GitHub Actions CI (`.github/workflows/ci.yml`), Render blueprint (`render.yaml`)

## Run locally
```bash
python3 -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cd server
python manage.py migrate
python manage.py seed            # sample dealers, reviews, car makes/models + demo accounts
python manage.py runserver       # http://127.0.0.1:8000/
```
Run the tests with `python manage.py test`.

### Demo accounts (created by `seed`)
| User | Password | Notes |
|---|---|---|
| `root` | `Root@12345` | admin at `/admin/` — set `ROOT_PASSWORD` to change |
| `demo` | `Demo@12345` | normal customer — set `DEMO_PASSWORD` to change |

**Change both passwords (environment variables) on any public deployment.**

## Pages
| URL | Page |
|---|---|
| `/` , `/dealers/` | Dealer list with state filter (`/dealers/?state=Kansas`) |
| `/dealer/<id>/` | Dealer details + reviews |
| `/postreview/<id>/` | Post a review (login required) |
| `/about/`, `/contact/` | About Us, Contact Us |
| `/login/`, `/register/` | Login, React sign-up |
| `/admin/` | Django admin |

## API
| Method & path | Purpose |
|---|---|
| `POST /djangoapp/login` `{"userName","password"}` | log in |
| `GET /djangoapp/logout` | log out |
| `POST /djangoapp/register` | create account (5 fields) |
| `GET /djangoapp/get_dealers` / `get_dealers/<state>` | all dealers / by state |
| `GET /djangoapp/dealer/<id>` | one dealer |
| `GET /djangoapp/reviews/dealer/<id>` | reviews for a dealer |
| `POST /djangoapp/add_review` | add a review (login required) |
| `GET /djangoapp/get_cars` | all car makes and models |
| `GET /djangoapp/analyze/<text>` | sentiment of a text |

## Docker
```bash
docker build -t cars-dealership .
docker run -p 8000:8000 -e ROOT_PASSWORD='choose-a-strong-one' cars-dealership
```

## Deploy and collect evidence
See [`DEPLOYMENT.md`](DEPLOYMENT.md) and [`SUBMISSION_GUIDE.md`](SUBMISSION_GUIDE.md).

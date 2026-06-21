# AI & Data Science Career Tracker

A web platform for evaluating student career readiness for AI, Data
Science, Machine Learning, and Software Engineering roles — skill
analysis, career scoring, and a personalized learning roadmap.

> **Build status: in progress (Stage 2 of 6 complete).**
> This README only documents what is actually built and runnable today.
> See [Roadmap / What's Not Built Yet](#roadmap--whats-not-built-yet) for
> everything still planned. Do not assume features described in the
> original spec (resume parsing, GitHub analytics, ML placement
> prediction, admin dashboard, frontend) exist yet — they don't.

---

## What's working right now

- **Authentication** — register, login, JWT access + refresh tokens,
  bcrypt password hashing, logout, change password
- **Student Profile** — name, branch, academic year, CGPA, social/coding
  profile links, plus full CRUD on skills, projects, certifications, and
  internships
- **Career Readiness Score** — weighted score out of 100 (Skills 40%,
  Projects 25%, Certifications 15%, Internships 10%, CGPA 10%), with a
  Beginner / Intermediate / Placement Ready status and historical
  snapshots for progress tracking
- **Skill Gap Analysis** — compares a student's skills against a curated
  industry skill list, returns existing/missing/recommended-next skills
- **Learning Roadmap Generator** — builds a 6-month milestone plan from
  missing skills, with per-milestone progress tracking

There is **no frontend yet**. Everything above is a REST API, tested via
curl/Postman or the sample requests below.

---

## Tech stack (current)

- **Backend:** Flask 3, Python 3.12
- **Database:** SQLite (dev), PostgreSQL-ready via `DATABASE_URL`
- **ORM:** SQLAlchemy + Flask-Migrate
- **Auth:** Flask-JWT-Extended (access + refresh tokens), Flask-Bcrypt
- **Rate limiting:** Flask-Limiter
- **CORS:** Flask-CORS

Pandas, NumPy, scikit-learn, pdfplumber, python-docx, and Plotly are
listed in `requirements.txt` for upcoming stages (job analytics, resume
parsing, placement prediction) but aren't used by any code yet.

---

## Project structure

```
career-tracker/
├── PROGRESS.md              # stage-by-stage build log
├── README.md                 # this file
├── backend/
│   ├── app/
│   │   ├── __init__.py        # Flask app factory
│   │   ├── config.py          # dev/test/prod config
│   │   ├── extensions.py      # db, jwt, bcrypt, limiter instances
│   │   ├── models/            # 16 SQLAlchemy models (full schema, see below)
│   │   ├── routes/            # auth, profile, score, skills, roadmap
│   │   ├── services/          # score_service, skill_gap_service, roadmap_service
│   │   ├── utils/             # validators, response helpers, decorators, activity log
│   │   └── ml/                # empty — reserved for Stage 4 (placement prediction)
│   ├── data/                  # empty — reserved for seed datasets
│   ├── ml_models/             # empty — reserved for trained model artifacts
│   ├── static/uploads/resumes/ # empty — reserved for Stage 3 (resume upload)
│   ├── seed.py                 # populates industry skills + sample accounts
│   ├── run.py                  # entry point
│   ├── requirements.txt
│   └── .env.example
└── frontend/                   # folder structure only — no code yet (Stage 5)
```

The database schema already includes all 16 tables for the full
12-module spec (job postings, GitHub stats, resume analyses, placement
predictions, etc.), even though the routes/services for most of them
don't exist yet. This was intentional, so later stages won't require
schema migrations that break earlier data.

---

## Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python seed.py                  # creates tables + sample data
python run.py
```

The API runs at `http://localhost:5000`. Health check: `GET /api/health`.

> **Note:** This was built in a sandboxed environment with no internet
> access, so I could not run `pip install` or boot the server myself to
> confirm it works end to end. Every file has been syntax-checked and
> the model/route/import graph has been manually traced for
> correctness, but please treat the first run on your machine as the
> real test — open an issue or flag it back to me if anything errors.

### Sample accounts (created by `seed.py`)

| Email | Password | Notes |
|---|---|---|
| `admin@careertracker.com` | `Admin@12345` | Admin role (no admin endpoints exist yet) |
| `priya.sharma@example.com` | `Student@123` | Strong profile — 9 skills, 3 projects, 1 completed cert, 1 internship |
| `arjun.verma@example.com` | `Student@123` | Beginner profile — 2 skills, 1 project, 1 in-progress cert |

---

## API overview

The backend exposes a REST API covering five areas so far: authentication,
student profile management, career readiness scoring, skill gap analysis,
and the learning roadmap generator. All responses share a consistent JSON
envelope (`success`, `message`, `data`), and protected routes require a
JWT bearer token obtained at login.

Endpoint-level details (exact paths, request bodies, status codes) aren't
listed in this README — they're documented as docstrings directly in each
file under `backend/app/routes/`, which is the authoritative source as the
API evolves.

---

## Roadmap / what's NOT built yet

These are in the original spec but have no code yet — no routes, no
services, no frontend. Listed here so expectations are accurate:

- **Job Market Analytics** — trending skills, salary/role distribution, charts
- **Project Recommendation Engine** — the `RecommendedProject` table and
  seed data exist, but there's no endpoint matching them to a student yet
- **Certification Tracker UI/endpoints** — certifications can be CRUD'd via
  `/api/profile/certifications`, but there's no dedicated progress/badge view
- **Placement Prediction (Random Forest)** — no model trained, no endpoint
- **GitHub Analytics** — `GitHubStats` table exists, no fetching logic yet
- **Resume Analyzer** — upload folder exists, no parsing logic yet
- **Admin Dashboard** — `role="admin"` exists on the User model, no
  admin-only endpoints or UI yet
- **Entire frontend** — React + Tailwind, dark/light mode, charts, all of it
- **Deployment guide, install guide (polished), sample datasets as files**

See `PROGRESS.md` for the stage-by-stage build log.

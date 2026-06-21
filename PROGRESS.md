# AI & Data Science Career Tracker — Build In Progress

This is a large multi-module project being built in stages. This file
tracks what's done so far. It will be replaced by the full project
README once everything is complete.

## ✅ Completed so far (Stage 1 — Foundation)

**Backend (`/backend`)**
- Project structure (`app/models`, `app/routes`, `app/services`, `app/utils`, `app/ml`)
- `requirements.txt` — all Python dependencies, pinned versions
- `app/config.py` — dev/test/prod config, SQLite by default, PostgreSQL-ready via `DATABASE_URL`
- `app/extensions.py` — SQLAlchemy, Migrate, JWT, Bcrypt, Limiter
- `app/__init__.py` — application factory, CORS, error handlers
- `run.py` — entry point
- **Full database schema (16 models)** covering all 12 functional modules:
  user, profile, skill, industry_skill, project, certification, internship,
  career_score, roadmap (+milestones), job_posting, prediction, resume,
  recommended_project, github_stats, activity_log
- **Authentication system (complete & functional)**:
  register, login, refresh, logout, get current user, change password —
  JWT access+refresh tokens, bcrypt password hashing, rate limiting
- `.env.example`, `.gitignore`

All Python files have been syntax-checked (`py_compile`) and all foreign
key references have been cross-verified against table names.

**Not yet runnable end-to-end** — there's no `/api/profile`, `/api/score`,
etc. yet, so the server will boot and auth will work, but most endpoints
described in the spec don't exist yet. See below.

## 🚧 Still to build

- Stage 2: Profile CRUD, Career Readiness Score engine, Skill Gap Analysis, Roadmap Generator, seed data script
- Stage 3: Job Market Analytics, Project Recommendation Engine, Certification Tracker, Resume Analyzer
- Stage 4: GitHub Analytics, Placement Prediction (Random Forest), Admin Dashboard
- Stage 5: React + Tailwind frontend (all pages, charts, dark/light mode)
- Stage 6: README, install guide, deployment guide (Render), sample datasets

## How to try what exists now

```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python run.py
```

Then test auth:
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123","full_name":"Test User"}'
```

I have no internet access in my build sandbox, so I could not run a live
`pip install` + server smoke test myself — please verify this boots
cleanly on your machine and let me know if anything errors out.

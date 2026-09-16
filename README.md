# Skill Decay Tracker

## Overview
Skill Decay Tracker is a simple personal learning dashboard that helps users track their technical skills, daily practice sessions, learning streaks, skill health, and progress toward target goals. The app is designed to keep the focus on consistency rather than perfection.

The application stores learning history, calculates streaks and decay, and uses a simple AI-style summary to turn recorded activity into a short, encouraging progress note.

## Features
- Skill tracking
- Daily learning sessions
- Learning streak monitoring
- Skill decay detection
- Progress tracking
- AI learning summaries
- AI progress projections
- Personalized learning recommendations

## Tech Stack
Frontend:
- React
- Vite
- JavaScript
- CSS

Backend:
- Python
- Django
- Django REST Framework

Database:
- PostgreSQL (production-ready)
- SQLite for local development

AI:
- Simple LLM API integration through Django backend

Deployment:
- React on Vercel
- Django on Render or Railway
- PostgreSQL hosted database

## Project Structure

```text
Skill tracker with AI/
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── db.sqlite3
│   └── skill_decay_tracker_backend/
│       ├── __init__.py
│       ├── settings.py
│       ├── urls.py
│       └── wsgi.py
│   └── tracker/
│       ├── __init__.py
│       ├── apps.py
│       ├── models.py
│       ├── serializers.py
│       ├── tests.py
│       ├── urls.py
│       └── views.py
├── frontend/
│   ├── .env
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── App.jsx
│       ├── main.jsx
│       ├── styles.css
│       ├── components/
│       ├── pages/
│       └── services/
├── README.md
└── .venv/
```

## Requirements
Before starting, install:
- Python 3.11+
- Node.js 18+
- PostgreSQL (for production setup)
- An LLM API key for the backend summary feature

## Backend Setup
1. Open a terminal in the backend folder.
2. Create and activate a virtual environment.
3. Install dependencies:

```powershell
cd "d:\myresume_project\Skill tracker with AI\backend"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

This creates a Python environment and installs Django, DRF, and PostgreSQL support.

4. Create the database tables:

```powershell
python manage.py migrate
```

This applies the Django migrations and sets up the local database tables.

5. Run the backend server:

```powershell
python manage.py runserver 127.0.0.1:8000
```

This starts the API on http://127.0.0.1:8000.

## Frontend Setup
1. Open a terminal in the frontend folder.
2. Install dependencies:

```powershell
cd "d:\myresume_project\Skill tracker with AI\frontend"
npm install
```

This installs React and Vite dependencies for the app.

3. Start the app:

```powershell
npm run dev -- --host 0.0.0.0
```

This starts the frontend and makes it available in the browser at http://localhost:5173.

## PostgreSQL Setup
For production or hosted deployment, create a PostgreSQL database and set the DATABASE_URL environment variable.

Example in pgAdmin:
1. Open pgAdmin.
2. Create a new database named skill_decay_tracker.
3. Create a user if needed.
4. Add the database connection details in your Django environment variables.

Example connection string:

```text
postgresql://postgres:your_password@localhost:5432/skill_decay_tracker
```

## Environment Variables
Backend variables:
- SECRET_KEY: Django secret key for local development or deployment
- DEBUG: True or False
- DATABASE_URL: PostgreSQL or SQLite connection string
- LLM_API_KEY: API key for the external LLM provider

Frontend variable:
- VITE_API_URL: http://127.0.0.1:8000

## Running the Application
Run backend:

```powershell
cd "d:\myresume_project\Skill tracker with AI\backend"
.\.venv\Scripts\Activate.ps1
python manage.py runserver 127.0.0.1:8000
```

Run frontend:

```powershell
cd "d:\myresume_project\Skill tracker with AI\frontend"
npm run dev -- --host 0.0.0.0
```

Then open:
- http://localhost:5173

## Deployment
Frontend deployment:
- Deploy the React app to Vercel.

Backend deployment:
- Deploy the Django API to Render or Railway.
- Set environment variables there.

Database deployment:
- Use a hosted PostgreSQL service and set DATABASE_URL accordingly.

LLM API deployment:
- Keep the LLM key in the Django backend only.
- Do not expose it in the React frontend.

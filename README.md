# Skill Decay Tracker

## Overview
Skill Decay Tracker is a personal learning dashboard that helps users track their technical skills, daily practice, learning streaks, and progress. It also identifies skills that haven't been practiced for a while and provides AI-generated insights and recommendations to help users stay consistent.

## Key Features
- Track technical skills and learning progress.
- Record daily learning activities.
- Monitor learning streaks.
- Identify skills that may be getting rusty.
- Generate AI-powered progress summaries.
- Predict future progress based on learning activity.
- Get personalized learning recommendations.

## Tech Stack

- **Frontend:** React, Vite, JavaScript, CSS
- **Backend:** Python, Django, Django REST Framework
- **Database:** PostgreSQL, SQLite
- **AI:** LLM API integration
- **Deployment:** Vercel, Render / Railway

## Project Structure

```text
Skill-Decay-Tracker/
├── backend/
│   ├── tracker/
│   ├── skill_decay_tracker_backend/
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## Local Setup

**Backend**

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**Frontend**

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` to access the application.

## Environment Variables

**Backend**
- `SECRET_KEY`
- `DEBUG`
- `DATABASE_URL`
- `LLM_API_KEY`

**Frontend**
- `VITE_API_URL`

## Deployment

- Frontend hosted on Vercel.
- Django backend hosted on Render or Railway.
- PostgreSQL used for production data storage.
- LLM API key securely managed through backend environment variables.

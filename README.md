# Job Application Tracker

A full-stack web application built with Flask and SQLite to track job applications, monitor their status, and visualize application statistics on a dashboard.

## Features

- User registration and login with secure password hashing
- Add, edit, and delete job applications
- Track company name, role, status, applied date, job link, and notes
- Filter applications by status (Applied, Interview, Offer, Rejected)
- Dashboard with live statistics using SQL aggregation
- Active filter highlighting based on current URL state

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Database | SQLite |
| Authentication | Werkzeug (password hashing), Flask sessions |
| Frontend | HTML, Jinja2, Bootstrap 5 |

## Project Structure

```
job_tracker/
├── app.py                   # Flask app, routes
├── auth.py                  # Register, login, logout, login_required
├── models.py                # Database schema, queries, stats aggregation
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html       # Stats cards + filter buttons + table
│   └── application_form.html
├── static/
│   └── style.css
├── tests/
│   └── test_models.py
├── requirements.txt
├── .env.example
└── README.md
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/stephenraj26/Job-Application-Tracker.git
cd Job-Application-Tracker
```

### 2. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Generate a secret key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Paste the generated key into `.env` as `SECRET_KEY`.

### 5. Run the application

```bash
python app.py
```

Open your browser at `http://127.0.0.1:5001`

### 6. Run tests

```bash
python -m pytest tests/
```

## How It Works

1. User registers an account and logs in
2. User adds job applications with company, role, status, and applied date
3. Dashboard displays stats (Total, Interviews, Offers, Rejected) using SQL `GROUP BY` and `COUNT`
4. User clicks filter buttons to view applications by status — uses `request.args` to read URL query parameters
5. The active filter button highlights based on the current filter state

## Database Schema

```
users          → id, username, email, password_hash, created_at
applications   → id, user_id, company_name, role, status, applied_date, notes, job_link, created_at
```

## Author

**Stephen Raj G**
- GitHub: [@stephenraj26](https://github.com/stephenraj26)
- LinkedIn: [stephen-raj-g](https://linkedin.com/in/stephen-raj-g)
